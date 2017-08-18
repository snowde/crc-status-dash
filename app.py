import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Event
import plotly.graph_objs as go
import pymongo
import os


def fill_x_y_lists(db, cluster, x, y, limit):
    cursor = db['status'].find({'cluster': cluster}).sort('_id', pymongo.DESCENDING).limit(limit)
    counter = 0
    for item in reversed(list(cursor)):
        x[counter] = item['time']
        y[counter] = 100 * item['allocated'] / item['total']
        counter += 1
        if counter == limit:
            return [cluster, item['allocated'], item['total']]


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


# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Ready the database
uri = 'mongodb://readonly:36677ee5c75a174cf07b6f88b816a5c4@ds157320.mlab.com:57320/crc-status'
client = pymongo.MongoClient(uri)
db = client.get_default_database()

# The limit of datapoints to return
limit = db['status'].find({'cluster': 'smp'}).count()
if limit > 24:
    limit = 24

app.layout = html.Div(children = [
    html.H1(children = 'CRC Status'),
    dcc.Graph(
        id = 'crc-status',
        figure = generate_figure()
    ),
    dcc.Interval(
        id = 'interval-component',
        interval = 15 * 60 * 1000
    )
])

@app.callback(Output('crc-status', 'figure'),
              events=[Event('interval-component', 'interval')])
def update_crc_status():
    return generate_figure()

if __name__ == '__main__':
    app.run_server()
