import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Event
import plotly.graph_objs as go



# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server
# -> This part is important for Heroku deployment
server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')




# Our main function
if __name__ == '__main__':
    app.run_server()
