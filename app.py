import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Event
import plotly.graph_objs as go
import pymongo
import os


# For a cluster, query, filter, and return the data needed by plotly
def fill_x_y_lists(db, cluster, x, y, limit):
    cursor = db['status'].find({'cluster': cluster}).sort('_id', pymongo.DESCENDING).limit(limit)
    counter = 0
    for item in reversed(list(cursor)):
        x[counter] = item['time']
        y[counter] = 100 * item['allocated'] / item['total']
        counter += 1
        if counter == limit:
            return [cluster, item['allocated'], item['total']]


# Generate the table which prints the cluster, allocated and total cores
# -> I had a hard time figuring out how to write an additional list comprehension
# ->  to deal with the loop over each cluster
def generate_table():
    return html.Table(
        # Header
        [html.Tr([
            html.Th(x) for x in ["Cluster", "Allocated Cores", "Total Cores"]
        ])] +
        # Body
        [html.Tr([
            html.Td(x) for x in get_table_entry('smp')
        ])] +
        [html.Tr([
            html.Td(x) for x in get_table_entry('gpu')
        ])] +
        [html.Tr([
            html.Td(x) for x in get_table_entry('mpi')
        ])] +
        [html.Tr([
            html.Td(x) for x in get_table_entry('htc')
        ])] +
        [html.Tr([
            html.Td(x) for x in get_table_entry('ib')
        ])]
    )


# For the table, I only need one entry from the database
def get_table_entry(cluster):
    cursor = db['status'].find({'cluster': cluster}).sort('_id', pymongo.DESCENDING).limit(1)
    for item in list(cursor):
        return cluster, item['allocated'], item['total']


# Get all the data to build our plot, also clean out any data points
# -> which are not shared by each cluster
def generate_figure():
    # A list of lists
    items = []

    # SMP x,y and append to list of lists
    smp_x = [0] * limit
    smp_y = [0] * limit
    items.append(fill_x_y_lists(db, 'smp', smp_x, smp_y, limit))

    # GPU x,y and append to list of lists
    gpu_x = [0] * limit
    gpu_y = [0] * limit
    items.append(fill_x_y_lists(db, 'gpu', gpu_x, gpu_y, limit))

    # MPI x,y and append to list of lists
    mpi_x = [0] * limit
    mpi_y = [0] * limit
    items.append(fill_x_y_lists(db, 'mpi', mpi_x, mpi_y, limit))

    # HTC x,y and append to list of lists
    htc_x = [0] * limit
    htc_y = [0] * limit
    items.append(fill_x_y_lists(db, 'htc', htc_x, htc_y, limit))

    # MPI_IB x,y and append to list of lists
    ib_x = [0] * limit
    ib_y = [0] * limit
    items.append(fill_x_y_lists(db, 'ib', ib_x, ib_y, limit))

    # Sometimes we get data which screws up our plot
    smp_diff = [x for x in smp_x if (x not in gpu_x) or
                                    (x not in mpi_x) or
                                    (x not in htc_x) or
                                    (x not in ib_x)]
    gpu_diff = [x for x in gpu_x if (x not in smp_x) or
                                    (x not in mpi_x) or
                                    (x not in htc_x) or
                                    (x not in ib_x)]
    mpi_diff = [x for x in mpi_x if (x not in gpu_x) or
                                    (x not in smp_x) or
                                    (x not in htc_x) or
                                    (x not in ib_x)]
    htc_diff = [x for x in htc_x if (x not in gpu_x) or
                                    (x not in mpi_x) or
                                    (x not in smp_x) or
                                    (x not in ib_x)]
    ib_diff = [x for x in ib_x if (x not in gpu_x) or
                                  (x not in mpi_x) or
                                  (x not in htc_x) or
                                  (x not in smp_x)]
                                    
    # Clean out the garbage
    for diff in smp_diff:
        index = smp_x.index(diff) 
        del smp_x[index]
        del smp_y[index]
    for diff in gpu_diff:
        index = gpu_x.index(diff) 
        del gpu_x[index]
        del gpu_y[index]
    for diff in mpi_diff:
        index = mpi_x.index(diff) 
        del mpi_x[index]
        del mpi_y[index]
    for diff in htc_diff:
        index = htc_x.index(diff) 
        del htc_x[index]
        del htc_y[index]
    for diff in ib_diff:
        index = ib_x.index(diff) 
        del ib_x[index]
        del ib_y[index]

    # Generate the Traces
    traces = [
        go.Scatter(
            x=smp_x,
            y=smp_y,
            name='smp',
            mode='lines+markers'
        ),
        go.Scatter(
            x=gpu_x,
            y=gpu_y,
            name='gpu',
            mode='lines+markers'
        ),
        go.Scatter(
            x=mpi_x,
            y=mpi_y,
            name='mpi',
            mode='lines+markers'
        ),
        go.Scatter(
            x=htc_x,
            y=htc_y,
            name='htc',
            mode='lines+markers'
        ),
        go.Scatter(
            x=ib_x,
            y=ib_y,
            name='ib',
            mode='lines+markers'
        ),
    ]
    layout = go.Layout(
        title='CRC Status',
        titlefont={'size': 18},
        yaxis={'ticksuffix': '%', 'title': 'Percent Utilization',
               'titlefont': {'size': 18}, 'tickfont': {'size': 18}},
        xaxis={'title': 'Date (MM/DD/YY-HH:MM)', 'nticks': 4,
               'titlefont': {'size': 18}, 'tickfont': {'size': 18}},
        legend={'font': {'size': 18}}
    )
    return {'data': traces, 'layout': layout}


# The layout function, this allows for the page updates when navigating to the site
def generate_layout():
    return html.Div(children = [
            #html.H1(children = 'CRC Status'),
            dcc.Graph(
                id = 'crc-graph',
                figure = generate_figure()
            ),
            html.Table(
                id = 'crc-table',
                children = generate_table(),
            ),
            dcc.Interval(
                id = 'interval-component',
                interval = 5 * 60 * 1000
            )
        ]
    )


# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server
# -> This part is important for Heroku deployment
server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')

# Ready the database
uri = 'mongodb://readonly:36677ee5c75a174cf07b6f88b816a5c4@ds157320.mlab.com:57320/crc-status'
client = pymongo.MongoClient(uri)
db = client.get_default_database()

# The limit of datapoints to return
# -> I don't want more than 24 points at a time
limit = db['status'].find({'cluster': 'smp'}).count()
if limit > 24:
    limit = 24

# The app layout w/ custom CSS for the table
app.layout = generate_layout
app.css.append_css({'external_url': "https://codepen.io/anon/pen/LjQejb.css"})

# Update the plot every interval tick
@app.callback(Output('crc-graph', 'figure'),
              events=[Event('interval-component', 'interval')])
def update_crc_graph():
    return generate_figure()

# Update the table every interval tick
@app.callback(Output('crc-table', 'children'),
              events=[Event('interval-component', 'interval')])
def update_crc_table():
    return generate_table()

# Our main function
if __name__ == '__main__':
    app.run_server()
