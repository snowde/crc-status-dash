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


four_figs_layout = html.Div([  # subpage 2

            # Row 1 (Header)


            dcc.Graph(figure=fwc.four_figs(), id='words_one', config={'displayModeBar': False},
                      style={'padding-left': '0cm','margin-right': '100px','border': '0', 'width': "100%", 'height': "550"}),

            html.Div(html.P(inp.exec, style={"padding-top": "1mm"}))


        ],)

        # Row 2

phrase_layout = html.Div([  # subpage 2

                # Row 1 (Header)

                        gc.layout

        ],)


language_layout = html.Div([

            html.Div([
                dcc.Tabs(
                    tabs=[{'label':"Noun" , 'value':"Noun" },
                          {'label':"Phrase" , 'value':"Phrase" },
                          {'label':"Sentiment" , 'value':"Sentiment" },
                          {'label':"Jobs Map" , 'value':"Map" },
                    ],
                    value="Noun",
                    id='tabs-language'
                ),
                html.Div(four_figs_layout, id='tab-output-language')
                    ], style={
                        'width': '100%',
                        'fontFamily': 'Sans-Serif',
                        'margin-left': 'auto',
                        'margin-right': 'auto'
                    }),])



