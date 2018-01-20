import dash_core_components as dcc
import dash_html_components as html
import pickle
import layout.chart_ratings as cr
import os
import pandas as pd

# NB never define any variable as path, that screws few things up.

my_path = os.path.abspath(os.path.dirname(__file__))
path_2 = os.path.join(my_path, "../input_fields.csv")
path_in_cpickle = os.path.join(my_path, "../data/interviews/")

#input_fields = pd.read_csv(path)

#code = input_fields["code_or_ticker"]#

def dic(code):

    p = code
    p = "BJRI"

    dict_ben = pickle.load(open(path_in_cpickle + p + "_benefits.p", "rb"))
    d = cr.dic(p)
    benefits_layout =   \
        html.Div([
            html.Div([dcc.Graph(id='benefits_chart', figure=d["fig_ben"], config={'displayModeBar': False},
                                    style={'position': 'relative', 'top': '-45px','bottom': '0px','left': '0px'})]
                     , style={'width': '100%', 'height': '430px', 'overflow': 'hidden'}),

            html.Div([

                html.H5("Positive Summary"),
                html.Div([dcc.Textarea(id='pos_int_sum', placeholder='Summary', value=dict_ben["positive"], style={'width': '100%', 'height':'115px'}
                                ),], style={'padding-top':'25px','clear':'both'}),

                html.H5("Negative Summary"),
                html.Div([dcc.Textarea(id='pos_int_sum', placeholder='Summary', value=dict_ben["negative"],
                                       style={'width': '100%', 'height': '115px'}
                                       ), ], style={'padding-top': '25px', 'clear': 'both'}),
                     ],style={'position': 'relative', 'top': '-65px','bottom': '0px','left': '0px'})

                ])


    compensation_layout = html.Div([

                html.Div([
                    dcc.Tabs(
                        tabs=[{'label':"Benefits" , 'value':"Benefits" },
                              {'label':"Salaries" , 'value':"Salaries" },
                              {'label':"Third" , 'value':"Third" },
                        ],
                        value="Benefits",
                        id='tabs-compensation'
                    ),
                    html.Div(benefits_layout, id='tab-output-compensation')
                        ], style={
                            'width': '100%',
                            'fontFamily': 'Sans-Serif',
                            'margin-left': 'auto',
                            'margin-right': 'auto'
                        }),])

    dic["benefits_layout"] = benefits_layout
    dic["compensation_layout"] = compensation_layout

    return dic


