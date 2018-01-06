import donuts_interview as di
import dash
from dash.dependencies import Input, Output
#import dash_core_components2 as dcc2
import dash_core_components as dcc
import dash_html_components as html
import interview_descriptions as ides
import frequency_word_chart as fwc
import input as inp
import glassdoor_chart as gc
import pickle
import chart_ratings as cr

p = "BJRI_gd_"

dict_ben = pickle.load(open(p + "dict_ben.p", "rb"))

benefits_layout =   \
    html.Div([
        html.Div([dcc.Graph(id='benefits_chart', figure=cr.fig_ben, config={'displayModeBar': False},
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



