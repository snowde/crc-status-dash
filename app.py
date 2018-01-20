# coding: utf-8
import dash
from dash.dependencies import Input, Output
#import dash_core_components2 as dcc2
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from plotly import graph_objs as go
from datetime import datetime as dt
import json

import pandas as pd
import os
from flask import Flask
from six.moves import cPickle as pickle #for performance
from os import listdir
from os.path import isfile, join
import numpy as np


import processing.input as inp

import layout.multiple_charts as mc
import layout.polar_figure as pf
import layout.polar_figure_2 as pf2
import layout.charting_words as cw
import layout.frequency_word_chart as fwc
import layout.glassdoor_chart as gc
import layout.chart_ratings as cr
import layout.language_layout as ll
import layout.compensation_layout as cl
import layout.infograph_layout as inl
import layout.treemap as tm
from processing.stock_narration import describe
import processing.frames as fm
from layout.figures import figs
import layout.donuts_interview as di
import layout.employee_layout as el
from flask_caching import Cache


### It is important to note that there is no target firm. This is dynamic.

    #To Give Orientation

# Initialize the Dash app #
app = dash.Dash(__name__)

cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache'
})


server = app.server
# -> This part is important for Heroku deployment
server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')


## Loading input fields
my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "../input_fields.csv")

input_fields = pd.read_csv("input_fields.csv")
from datetime import datetime, timedelta

now = datetime.now()


###############

r = 5
if r > 4:
    employee_sentiment = "happy"
else:
    employee_sentiment = "unhappy"


dict = {

    "title": "BJ’s Restaurant & Brewhouse",
    "location": "Jacksonville",
    "employees": "Employees are " + employee_sentiment + "." + "The company then bought 26.",
    "customers": "Customers are happy. The company then bought 26.",
    "shareholders": "Shareholders are happy. The company then bought 26.",
    "management": "Management is performing well. The company then bought 26."

}
#
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

my_path = os.path.abspath(os.path.dirname('__file__'))

path = os.path.join(my_path, "data/cpickle/")

first_dict = pickle.load(open(path + "first_page.p", "rb"))


figure = pf.figs_polar(first_dict["code_start"], "bench", first_dict["code_start"])

comp_plot_output = figure

fig = figs(first_dict["code_start"], first_dict["the_benchmark"])
stock_plot_output = fig

df_perf_summary = first_dict["df_perf_summary_output"]


def make_dash_table(df):
    ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table


modifed_perf_table = make_dash_table(df_perf_summary)

modifed_perf_table.insert(
    0, html.Tr([
        html.Td([]),
        html.Td(['Company'], colSpan=4, style={'text-align': "center"}),
        html.Td(['Benchmark'], colSpan=4, style={'text-align': "center"})
    ], style={'background': 'white', 'font-weight': '600'}
    )
)
mgmt_perf_output = modifed_perf_table

mgmt_perf_output_1 = modifed_perf_table


#path = os.path.join(my_path, "data/cpickle/")

#dict_all_coll = pickle.load(open(path + "dict_all_coll.p", "rb"))

@cache.memoize()
def roll():
    my_path = os.path.abspath(os.path.dirname('__file__'))

    path = os.path.join(my_path, "data/cpickle/")

    dict_all_coll = pickle.load(open(path + "dict_all_coll.p", "rb"))
    return dict_all_coll

dict_all_coll = roll()



app.config['suppress_callback_exceptions']=True
# Describe the layout, or the UI, of the app
app.layout = html.Div([

    # Hidden div inside the app that stores the intermediate value
    html.Div(id='intermediate-value', style={'display': 'none'}),

    html.Div([  # page 1

        html.A(['Print PDF'],
               className="button no-print",
               style={'position': "absolute", 'top': '-40', 'right': '0'}),

        html.Div([  # subpage 1

            # Row 1 (Header)

            html.Div([

                html.Div([
                    #html.H5(
                    ##
                    #    dict["title"] + " 4-D Report lo"),
                    html.H5(first_dict["title_output"], id='title'),

                    html.H6(first_dict["location_output"], id='location',
                            style={'color': '#7F90AC'}),
                    html.Div([


                        html.Div([
                            dcc.Dropdown(
                                id='locas',
                                options=first_dict["locas_output"],
                                value="All",
                                clearable=False,
                                className="dropper",
                                placeholder="Type Location",


                            )
                        ], style={'background-color':'#a9a9a9','color':'rgb(217, 224, 236)','float':'left', 'padding-right': '0cm', 'width': '20%'}),

                        html.Div([
                            html.Button('SWAP', id='button_swap', n_clicks=0, style={'height': '3.3em', 'float': 'center', 'color':'rgb(217, 224, 236)'})
                        ], style={'padding-left': '0.8cm', 'padding-right': '0.8cm','float':'left'}),

                        html.Div([
                            dcc.Dropdown(
                                id='benchy',
                                #value=bench_start,
                                options=first_dict["benchy_output"],
                                clearable=False,
                                className="dropper",
                                placeholder="Select Benchmark"

                            )
                        ], style={'background-color':'#a9a9a9','color':'rgb(217, 224, 236)','width': '80%','float':'left','width': '20%'}),
                        html.Div([html.H3('3.6/5')],style={'padding-left': '1.2cm','float':'left'})
                        # , 'float': 'right', 'display': 'inline-block'
                    ], style={'padding-top': '0.3cm', 'padding-left': '0cm'},
                        className="double_drop"),

                ], className="nine columns padded"),

                html.Div([
                    html.H1(
                        [html.Span(str(now.month), style={'opacity': '0.5'}), html.Span(str(now.year)[2:])]),
                    html.H6('Monthly Interactive Update')
                ], className="three columns gs-header gs-accent-header padded", style={'float': 'right'}),

            ], className="row gs-header gs-text-header"),


            html.Br([]),

            html.Div([

                    html.Div([html.H6(["Executive Summary"], style={"float":"left","padding-right":"0.2cm"}),
                    html.A("info", href='http://4d.readthedocs.io/en/latest/text/executive_summary.html#executive-summary', target="_blank")
                        ],className="gs-header gs-table-header padded"),

                      html.P(inp.exec, style={"padding-top":"1mm"})]),


            # Row 2

            html.Div([

                html.Div([

                    html.H6(first_dict["profile_output"], id="profile",className="gs-header gs-text-header padded"),

                    html.Strong("Employees pg 4"),
                    html.P(dict["employees"],
                           className='blue-text'),

                    html.Strong(
                        'Customers pg 6'),
                    html.P(dict["customers"],
                           className='blue-text'),

                    html.Strong('Shareholders pg 8'),
                    html.P(dict["shareholders"],
                           className='blue-text'),

                    html.Strong('Management pg 10'),
                    html.P(dict["management"],
                           className='blue-text'),

                ], className="four columns"),

                html.Div([
                    html.H6(["Shareholder Performance"],
                            className="gs-header gs-table-header padded"),
                    #html.Iframe(src="https://plot.ly/~snowde/36.embed?modebar=false&link=false&autosize=true", \
                    #            seamless="seamless", style={'border': '0', 'width': "100%", 'height': "250"}),

                dcc.Graph(figure = stock_plot_output,
                    id='stock_plot',style={'border': '0', 'width': "100%", 'height': "250"},
                    config={'displayModeBar': False}
                )
                ], className="eight columns"),
            ], className="row "),

            # Row 2.5, s

            html.Div([

                html.Div([


                    html.H6('Stakeholder Metrics',
                            className="gs-header gs-text-header padded"),
                    html.Table(make_dash_table(first_dict["s_metrics_df_output"]), id="s_metrics_df", style={'marginBottom': 5},
                               className='tiny-header'),
                    html.P("E - Employees; C - Customer; S - Shareholders; M - Management; A - Average; BA - Benchmark Average", style={'font-size': '60%', 'marginTop': 5}),
                    html.H6('Company Metrics',
                            className="gs-header gs-text-header padded"),
                    html.Table(make_dash_table(first_dict["c_metrics_df_output"]), id="c_metrics_df", style={'marginBottom': 5},
                               className='tiny-header'),
                ], className="four columns"),



                html.Div([
                    html.P(first_dict["stock_plot_desc_output"],id='stock_plot_desc', style={"padding-top":"1.2mm"}),
                ], className="eight columns"),
                html.Div([

                    html.H6("Financial Performance",
                            className="gs-header gs-table-header padded"),
                    html.Table(mgmt_perf_output,id="mgmt_perf", className="reversed")
                ], className="eight columns"),

            ], className="row "),

            # Row 3##


        ], className="subpage"),

    ], className="page"),

    html.Div([  # page 5

            html.A(['Print PDF'],
                   className="button no-print",
                   style={'position': "absolute", 'top': '-40', 'right': '0'}),

            html.Div([  # subpage 2

                # Row 1 (Header)

                html.Div([
                    html.H6(["Executive Advice"],
                            className="gs-header gs-table-header padded"),

                        ]),

        ], className="subpage"),

    ], className="page"),

    html.Div([  # page 1

            html.A(['Print PDF'],
                   className="button no-print",
                   style={'position': "absolute", 'top': '-40', 'right': '0'}),

            html.Div([  # subpage 1

                # Row 1 (Header)

                html.Br([]),

                html.Div([html.H6(["Trend Analysis"],
                                className="gs-header gs-table-header padded"),
                          html.P(inp.exec, style={"padding-top":"1mm"}),

                            html.Div([
                                dcc.Tabs(
                                    tabs=[{'label':"Overall" , 'value':"Overall" },
                                          {'label':"Employee" , 'value':"Employee" },
                                          {'label':"Management" , 'value':"Management" },
                                          {'label':"Shareholders" , 'value':"Shareholders" },
                                          {'label':"Customers" , 'value':"Customers" },
                                          {'label':"Search" , 'value':"Search" },
                                    ],
                                    value="Overall",
                                    id='tabs'
                                ),
                                html.Div(id='tab-output')
                            ], style={
                                'width': '100%',
                                'fontFamily': 'Sans-Serif',
                                'margin-left': 'auto',
                                'margin-right': 'auto'
                            })

                         ]),

                # Row 2
                # Row 2.5, s

                html.Div([

                    html.Div([


                        html.H6('Stakeholder Metrics',
                                className="gs-header gs-text-header padded"),
                        html.Table( id="s_metrics_df_1", style={'marginBottom': 5},
                                   className='tiny-header'),
                        html.P("E - Employees; C - Customer; S - Shareholders; M - Management; A - Average; BA - Benchmark Average", style={'font-size': '60%', 'marginTop': 5}),
                        html.H6('Financial Metrics',
                                className="gs-header gs-text-header padded"),
                        html.Table(id="c_metrics_df_1", style={'marginBottom': 5},
                                   className='tiny-header'),
                    ], className="four columns"),


                    html.Div([

                        html.H6("Management Performance",
                                className="gs-header gs-table-header padded"),
                        html.Table(id="mgmt_perf_1", className="reversed")
                    ], className="eight columns"),

                ], className="row "),

                # Row 3#


        ], className="subpage"),

    ], className="page"),

    html.Div([  # page 5

                html.A(['Print PDF'],
                       className="button no-print",
                       style={'position': "absolute", 'top': '-40', 'right': '0'}),

                html.Div([  # subpage 2

                    # Row 1 (Header)

                    html.Div([
                        html.H6(["Sensitivity and Valuation Analysis"],
                                className="gs-header gs-table-header padded"),

                            ]),

        ], className="subpage"),

    ], className="page"),


    html.Div([  # page 3

        html.A(['Print PDF'],
               className="button no-print",
               style={'position': "absolute", 'top': '-40', 'right': '0'}),

        html.Div([  # subpage 2

            # Row 1 (Header)

            html.Div([
                    html.H6(["Competitor Analysis"],
                            className="gs-header gs-table-header padded") ]),

            dcc.Graph(config={'displayModeBar': False}, id='comp_plot',style={'border': '0', 'width': "100%", 'height': "250"}),


        ], className="subpage"),

            # Row 2

            html.Div(html.P(inp.exec, style={"padding-top":"1mm"}))

    ], className="page"),

    html.Div([  # page 5

        html.A(['Print PDF'],
               className="button no-print",
               style={'position': "absolute", 'top': '-40', 'right': '0'}),

        html.Div([  # subpage 2

            # Row 1 (Header)

            html.Div([
                html.H6(["Employee Analysis"],
                        className="gs-header gs-table-header padded")]),

            html.Br([]),

            html.Div([
                dcc.Tabs(
                    tabs=[{'label':"Interview" , 'value':"Interview" },
                          {'label':"Sentiment" , 'value':"Sentiment" },
                          {'label':"Compensation" , 'value':"Compensation" },
                          {'label':"Jobs Map" , 'value':"Jobs Map" },
                          {'label':"Search" , 'value':"Search" },
                    ],
                    value="Interview",
                    id='tabs-employee'
                ),
                html.Div(id='tab-output-employee'),

                    ], style={
                        'width': '100%',
                        'fontFamily': 'Sans-Serif',
                        'margin-left': 'auto',
                        'margin-right': 'auto'
                    }),


        ], className="subpage"),

    ], className="page"),

html.Div([  # page 5

        html.A(['Print PDF'],
               className="button no-print",
               style={'position': "absolute", 'top': '-40', 'right': '0'}),

        html.Div([  # subpage 2

            # Row 1 (Header)

            html.Div([
                html.H6(["Customer Analysis"],
                        className="gs-header gs-table-header padded")]),

            html.Br([]),

            html.Div([
                dcc.Tabs(
                    tabs=[{'label':"Infographic" , 'value':"Infographic" },
                          {'label':"Map" , 'value':"Map" },
                          {'label':"Sentiment" , 'value':"Sentiment" },
                    ],
                    value="Infographic",
                    id='tabs-customer'
                ),
                html.Div(id='tab-output-customer'),

                    ], style={
                        'width': '100%',
                        'fontFamily': 'Sans-Serif',
                        'margin-left': 'auto',
                        'margin-right': 'auto'
                    }),


        ], className="subpage"),

    ], className="page"),

    html.Div([  # page 5

        html.A(['Print PDF'],
               className="button no-print",
               style={'position': "absolute", 'top': '-40', 'right': '0'}),

        html.Div([  # subpage 2

            # Row 1 (Header)

            html.Div([
                html.H6(["Shareholder Analysis"],
                        className="gs-header gs-table-header padded"),

                    ]),

        ], className="subpage"),

    ], className="page"),

    html.Div([  # page 5

        html.A(['Print PDF'],
               className="button no-print",
               style={'position': "absolute", 'top': '-40', 'right': '0'}),

        html.Div([  # subpage 2

            # Row 1 (Header)

            html.Div([
                html.H6(["Management Analysis"],
                        className="gs-header gs-table-header padded"),

            ]),

        ], className="subpage"),

    ], className="page"),

    html.Div([  # page 5

        html.A(['Print PDF'],
               className="button no-print",
               style={'position': "absolute", 'top': '-40', 'right': '0'}),

        html.Div([  # subpage 2

            # Row 1 (Header)

            html.Div([
                html.H6(["Dimensional Analysis"],
                        className="gs-header gs-table-header padded"),

            ]),

        ], className="subpage"),

    ], className="page"),

    html.Div([  # page 5

        html.A(['Print PDF'],
               className="button no-print",
               style={'position': "absolute", 'top': '-40', 'right': '0'}),

        html.Div([  # subpage 2

            # Row 1 (Header)

            html.Div([
                html.H6(["Appendix Analysis"],
                        className="gs-header gs-table-header padded"),

            ]),

        ], className="subpage"),

    ], className="page"),

    html.Div([  # page 3

        html.A(['Print PDF'],
               className="button no-print",
               style={'position': "absolute", 'top': '-40', 'right': '0'}),

        html.Div([  # subpage 2

            # Row 1 (Header)

            html.Div([

                # Data tables on this page:
                # ---
                # df_fund_info = pd.read_csv('https://plot.ly/~jackp/17544/.csv')
                # df_fund_characteristics = pd.read_csv('https://plot.ly/~jackp/17542/.csv')
                # df_fund_facts = pd.read_csv('https://plot.ly/~jackp/17540/.csv')
                # df_bond_allocation = pd.read_csv('https://plot.ly/~jackp/17538/')

                # Column 1

                html.Div([
                    html.H6('Financial Information',
                            className="gs-header gs-text-header padded"),
                    html.Table(id="df_fund_info"),

                    html.H6('Fund Characteristics',
                            className="gs-header gs-text-header padded"),
                    html.Table(id="df_fund_characteristics"),

                    html.H6('Fund Facts',
                            className="gs-header gs-text-header padded"),
                    html.Table(id="df_fund_facts"),

                ], className="four columns"),

                # Column 2##

                html.Div([
                    html.H6('Sector Allocation (%)',
                            className="gs-header gs-table-header padded"),
                    html.Iframe(src="https://plot.ly/~jackp/17560.embed?modebar=false&link=false&autosize=true", \
                                seamless="seamless", style={'border': '0'}, width="100%", height="300"),

                    html.H6('Country Bond Allocation (%)',
                            className="gs-header gs-table-header padded"),
                    html.Table(id="df_bond_allocation"),

                ], className="four columns"),

                # Column 3

                html.Div([
                    html.H6('Top 10 Currency Weights (%)',
                            className="gs-header gs-table-header padded"),
                    html.Iframe(src="https://plot.ly/~jackp/17555.embed?modebar=false&link=false&autosize=true", \
                                seamless="seamless", style={'border': '0'}, width="100%", height="300"),

                    html.H6('Credit Allocation (%)',
                            className="gs-header gs-table-header padded"),
                    html.Iframe(src="https://plot.ly/~jackp/17557.embed?modebar=false&link=false&autosize=true", \
                                seamless="seamless", style={'border': '0'}, width="100%", height="300"),

                ], className="four columns"),

            ], className="row"),

        ], className="subpage"),

    ], className="page"),
####
    html.Div([  # page 2

            html.A(['Print PDF'],
                   className="button no-print",
                   style={'position': "absolute", 'top': '-40', 'right': '0'}),

            html.Div([  # subpage 2

                # Row 1 (Header)

                html.Div([
                        html.H6(["Company Financials"],
                                className="gs-header gs-table-header padded")]),

                mc.layout,

                # Row ##

                html.Div([html.P(inp.exec, style={"padding-top":"1mm"}),

                          html.Div([dcc.Graph(
                              id='first_tree',
                              config={'displayModeBar': False},
                              style={'autosize': 'False', 'margin-top': '-100px', 'padding-right': '4cm', 'border': '0',
                                     'width': "20%", 'height': "20%"})

                          ], style={'background-color': '#a9a9a9', 'color': 'rgb(217, 224, 236)', 'float': 'left',
                                    'padding-right': '4cm', 'width': "20%", 'height': "20%"}),

                          html.Div([dcc.Graph(
                              id='third_tree',
                              config={'displayModeBar': False},
                              style={'autosize': 'False', 'margin-top': '-100px', 'padding-top': '0cm',
                                     'padding-left': '4cm', 'border': '0', 'width': "20%", 'height': "20%"})

                          ], style={'background-color': '#a9a9a9', 'color': 'rgb(217, 224, 236)', 'float': 'left',
                                    'padding-right': '0cm', 'width': "20%", 'height': "20%"}),
                          ],style={'z-index':'3'}),


        ], className="subpage" ),

    ],className="page")

])

if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })

#'https://codepen.io/chriddyp/pen/bWLwgP.css',##
# If you upload css you have to reapload it after github to git raw.
# fuckit i JUST STORED IT IN KERAS
#https://github.com/snowde/keras/blob/master/just.css

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                #"https://www.dropbox.com/s/7zx0pqn3eqql7b1/this.css?dl=1"
                "https://cdn.rawgit.com/snowde/keras/c59812f7/just.css",
                #"https://cdn.rawgit.com/plotly/dash-app-stylesheets/5047eb29e4afe01b45b27b1d2f7deda2a942311a/goldman-sachs-report.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

external_js = [
               "https://code.jquery.com/jquery-3.2.1.min.js",
               "https://cdn.rawgit.com/snowde/keras/2b7d6742/new_java.js",
               "https://cdn.rawgit.com/plotly/dash-app-stylesheets/a3401de132a6d0b652ba11548736b1d1e80aa10d/dash-goldman-sachs-report-js.js",
                ]

for js in external_js:
    app.scripts.append_script({"external_url": js})


#
# Call Backs




@app.callback(Output('intermediate-value', 'children'),
      [dash.dependencies.Input('locas', 'value'),
     dash.dependencies.Input('benchy', 'value'),
     dash.dependencies.Input('button_swap', 'n_clicks')],
    [dash.dependencies.State('intermediate-value', 'children')])

def clean_data(the_location, the_benchmark, clicks,riffy):
     # some expensive clean data step

     code_start = input_fields[input_fields["starting"] == 1]["code_or_ticker"].reset_index(drop=True)[0]

     code_start_small = input_fields[input_fields["code_or_ticker"]==code_start]["yelp_name"].reset_index(drop=True)[0]

     bench_start = input_fields[input_fields["starting"] == 2]["code_or_ticker"].reset_index(drop=True)[0]

     bench_start_small = input_fields[input_fields["code_or_ticker"]==bench_start]["yelp_name"].reset_index(drop=True)[0]

     ## Starting here

     #location_start = "2231 State Hwy 6, Sugar Land, TX 77478"

     #small_loc = "Sugar-Land"
     #first_option_coy.title()

     if clicks % 2 == 0:
         if not all((the_benchmark, the_location)):
             the_location = first_dict["first_option_coy_output"].title()
             the_benchmark = bench_start

         else:
             the_benchmark = the_benchmark

     else:
         temp = code_start  # The old switcheroo.#
         code_start = the_benchmark
         the_benchmark = temp
         code_start_small = input_fields[input_fields["code_or_ticker"] == code_start]["yelp_name"].reset_index(drop=True)[0]
     temp_df = pd.DataFrame()
     temp_df["available_locations"] = dict_all_coll[code_start]["Full Address"]
     temp_df["a_small_names"] = dict_all_coll[code_start]["Adapted Small Name"]

     if clicks == 1:
         the_location = temp_df["a_small_names"][0]


     brad = 0
     if clicks > 0:
         riffy = json.loads(riffy)
         brad = riffy["clicks"] - clicks

     if brad != 0:
         the_location = temp_df["a_small_names"][0]


     long_addy = temp_df[temp_df["a_small_names"] == the_location]["available_locations"].reset_index(drop=True)[0]

     temp_df = pd.DataFrame()
     temp_df["available_locations"] = dict_all_coll[code_start]["Available Benchmark"]
     temp_df["a_small_names"] = dict_all_coll[code_start]["Available Benchmark Small Name"]

     ##bench_small = temp_df[temp_df["available_locations"] == the_benchmark]["a_small_names"].reset_index(drop=True)[0]
     ##  "bench_small":bench_small,
     diffy = {'long_addy':long_addy,'bench_start_small':bench_start_small,"code_start_small":code_start_small,'the_location':the_location, 'the_benchmark':the_benchmark, 'code_start':code_start, 'clicks':clicks}

     return json.dumps(diffy)




@app.callback(Output('locas', 'options'),
     [dash.dependencies.Input('intermediate-value', 'children'),
      dash.dependencies.Input('button_swap', 'n_clicks')
     ])

def dadr(diffy, clicks):
    diffy = json.loads(diffy)

    available_locations = dict_all_coll[diffy["code_start"]]["Full Address"]
    a_small_names = dict_all_coll[diffy["code_start"]]["Adapted Small Name"]

    return [{'label': r, 'value': i} for r,i in zip(available_locations,a_small_names)]

#############  This can change the benchmark dropdown.
"""
@app.callback(Output('benchy', 'options'),
     [dash.dependencies.Input('intermediate-value', 'children'),
     ])

def dadr(diffy):
    diffy = json.loads(diffy)
    available_locations = dict_all_coll[diffy["code_start"]]["Available Benchmark"]
    a_small_names = dict_all_coll[diffy["code_start"]]["Available Benchmark Small Name"]

    return [{'label': r, 'value': i} for r,i in zip(a_small_names,available_locations)]
"""


# Tables#
@app.callback(Output('s_metrics_df', 'children'),
     [dash.dependencies.Input('locas', 'value'),
      dash.dependencies.Input('intermediate-value', 'children'),
     ])
def dadr(locas, diffy):
    diffy = json.loads(diffy)
    s_metrics_df = dict_all_coll[diffy["code_start"]]["Stakeholder Metrics"]
    return make_dash_table(s_metrics_df)

@app.callback(Output('s_metrics_df_1', 'children'),
     [dash.dependencies.Input('locas', 'value'),
      dash.dependencies.Input('intermediate-value', 'children'),
     ])
def dadr(locas, diffy):
    diffy = json.loads(diffy)
    s_metrics_df = dict_all_coll[diffy["code_start"]]["Stakeholder Metrics"]
    return make_dash_table(s_metrics_df)



@app.callback(Output('c_metrics_df', 'children'),
     [dash.dependencies.Input('intermediate-value', 'children'),
     ])
def dadr(diffy):
    diffy = json.loads(diffy)
    c_metrics_df = dict_all_coll[diffy["code_start"]]["Company Metrics"]
    return make_dash_table(c_metrics_df)


@app.callback(Output('c_metrics_df_1', 'children'),
     [dash.dependencies.Input('intermediate-value', 'children'),
     ])
def dadr(diffy):
    diffy = json.loads(diffy)
    c_metrics_df = dict_all_coll[diffy["code_start"]]["Company Metrics"]
    return make_dash_table(c_metrics_df)


@app.callback(Output('df_fund_info', 'children'),
     [dash.dependencies.Input('intermediate-value', 'children'),
     ])
def dadr(diffy):
    df_fund_info = pd.read_csv('https://plot.ly/~jackp/17544/.csv')

    return make_dash_table(df_fund_info)


@app.callback(Output('df_fund_characteristics', 'children'),
              [dash.dependencies.Input('intermediate-value', 'children'),
               ])
def dadr(diffy):
    df_fund_characteristics = pd.read_csv('https://plot.ly/~jackp/17542/.csv')

    return make_dash_table(df_fund_characteristics)


@app.callback(Output('df_fund_facts', 'children'),
              [dash.dependencies.Input('intermediate-value', 'children'),
               ])
def dadr(diffy):
    df_fund_facts = pd.read_csv('https://plot.ly/~jackp/17540/.csv')

    return make_dash_table(df_fund_facts)


@app.callback(Output('df_bond_allocation', 'children'),
              [dash.dependencies.Input('intermediate-value', 'children'),
               ])
def dadr(diffy):
    df_bond_allocation = pd.read_csv('https://plot.ly/~jackp/17538/')

    return make_dash_table(df_bond_allocation)


@app.callback(Output('comp_plot', 'figure'),
     [dash.dependencies.Input('intermediate-value', 'children'),
     ])
def dadr(diffy):
    diffy = json.loads(diffy)
    figure=pf.figs_polar(diffy["code_start"], "bench", diffy["code_start"])

    return figure


@app.callback(
    dash.dependencies.Output('stock_plot', 'figure'),
    [dash.dependencies.Input('intermediate-value', 'children')
     ])
def dadr(diffy):
    diffy = json.loads(diffy)
    fig = figs(diffy["code_start"], diffy["the_benchmark"])
    return fig


@app.callback(
    dash.dependencies.Output('stock_plot_desc', 'children'),
    [dash.dependencies.Input('intermediate-value', 'children')
     ])

def dadr(diffy):
    diffy = json.loads(diffy)
    desc = describe(diffy["code_start"], diffy["the_benchmark"])
    return desc


@app.callback(
    dash.dependencies.Output('title', 'children'),
    [dash.dependencies.Input('intermediate-value', 'children')
     ])

def dadr(diffy):
    diffy = json.loads(diffy)
    title = str(diffy["code_start_small"]) + " 4-D Report"
    return title


@app.callback(
    dash.dependencies.Output('location', 'children'),
    [dash.dependencies.Input('intermediate-value', 'children')
     ])

def dadr(diffy):
    diffy = json.loads(diffy)
    #print(diffy["dict_comp"])
    #print(diffy["the_location"])
    title = str(diffy["long_addy"]) + " Location"

    return title



@app.callback(
    dash.dependencies.Output('profile', 'children'),
    [dash.dependencies.Input('intermediate-value', 'children')
     ])

def dadr(diffy):
    diffy = json.loads(diffy)
    title = str(diffy["the_location"]) + " Profile"

    return title
###


@app.callback(
    dash.dependencies.Output('mgmt_perf', 'children'),
    [dash.dependencies.Input('intermediate-value', 'children')
     ])
def dadr(diffy):
    diffy = json.loads(diffy)
    df_perf_summary = fm.fin_met(diffy["the_benchmark"], diffy["code_start"])

    def make_dash_table(df):
        ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
        table = []
        for index, row in df.iterrows():
            html_row = []
            for i in range(len(row)):
                html_row.append(html.Td([row[i]]))
            table.append(html.Tr(html_row))
        return table

    modifed_perf_table = make_dash_table(df_perf_summary)

    modifed_perf_table.insert(
        0, html.Tr([
            html.Td([]),
            html.Td(['Company'], colSpan=4, style={'text-align': "center"}),
            html.Td(['Benchmark'], colSpan=4, style={'text-align': "center"})
        ], style={'background': 'white', 'font-weight': '600'}
        )
    )
    return modifed_perf_table
#

@app.callback(
    dash.dependencies.Output('mgmt_perf_1', 'children'),
    [dash.dependencies.Input('intermediate-value', 'children')
     ])
def dadr(diffy):
    diffy = json.loads(diffy)
    df_perf_summary = fm.fin_met(diffy["the_benchmark"], diffy["code_start"])
    def make_dash_table(df):
        ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
        table = []
        for index, row in df.iterrows():
            html_row = []
            for i in range(len(row)):
                html_row.append(html.Td([row[i]]))
            table.append(html.Tr(html_row))
        return table

    modifed_perf_table = make_dash_table(df_perf_summary)

    modifed_perf_table.insert(
        0, html.Tr([
            html.Td([]),
            html.Td(['Company'], colSpan=4, style={'text-align': "center"}),
            html.Td(['Benchmark'], colSpan=4, style={'text-align': "center"})
        ], style={'background': 'white', 'font-weight': '600'}
        )
    )
    return modifed_perf_table

@app.callback(
    Output('filtered-content', 'children'),
    [dash.dependencies.Input('intermediate-value', 'children'),
     Input('category-filter', 'value'),
     Input('request', 'value'),
     Input('study', 'value'),
     Input('bench', 'value')])
def filter(diffy ,var, req, stu, ben):
    diffy = json.loads(diffy)
    dict_frames = dict_all_coll[diffy["code_start"]]["Stock Dictionary"]
    df = dict_frames[ben, req, stu]

    highlight = list(df.drop("year",axis=1).columns.values)

    if stu in ["Normalised", "Original"]:
        highlight = list(df.ix[:, :5].columns.values)

    highlight = highlight + var
    figure = mc.create_figure(highlight,df,req, stu)

    for trace in figure['data']:
        trace['hoverinfo'] = 'text'

    return dcc.Graph(
        id='filtered-graph',
        figure=figure,config={'displayModeBar': False}
    )
###
@app.callback(
    Output('category-filter', 'options'),
    [dash.dependencies.Input('intermediate-value', 'children'),
     Input('request', 'value'),
     Input('study', 'value'),
     Input('bench', 'value')])
def filter(diffy,req, stu, ben):
    # print(per, req, stu, ben)
    diffy = json.loads(diffy)
    dict_frames =  dict_all_coll[diffy["code_start"]]["Stock Dictionary"]
    df = dict_frames[ben, req, stu]
    highlight = list(df.drop("year", axis=1).columns.values)

    return [{'label': i, 'value': i} for i in highlight]


@app.callback(
    Output('first_tree', 'figure'),
    [dash.dependencies.Input('intermediate-value', 'children'),
     Input('request', 'value'),
     ])
def filter(diffy, req):
    diffy = json.loads(diffy)
    dict_frames =  dict_all_coll[diffy["code_start"]]["Stock Dictionary"]
    df = dict_frames["BJRI", req, "Original"]
    return tm.treemap(df)
###
@app.callback(
    Output('third_tree', 'figure'),
    [dash.dependencies.Input('intermediate-value', 'children'),
    Input('request', 'value'),
     ])
def filter(diffy, req):
    diffy = json.loads(diffy)
    bench_start = diffy["the_benchmark"]
    dict_frames = dict_all_coll[diffy["code_start"]]["Stock Dictionary"]
    df = dict_frames[bench_start, req, "Original"]
    return tm.treemap(df)

@app.callback(
    Output('graphed', 'figure'),
    [Input('goo_ba', 'value'),
     Input('time', 'value'),
     Input('many', 'value'),
     Input('norm', 'value'),
     Input('bencher', 'value')])
def filter2( goo, time, many, norm, bench):
    #print(per, req, stu, ben)

    figure = gc.chart_gd(goo, time, many, norm, bench)

###
    return figure

@app.callback(
    Output('text_sum', 'value'),
    [Input('goo_ba', 'value'),
     Input('time', 'value'),
     Input('many', 'value'),
     Input('norm', 'value'),
     Input('bencher', 'value')])
def filter2( goo, time, many, norm, bench):
    #print(per, req, stu, ben)

    figure = gc.sum_gd(goo, time, many, norm, bench)
    return figure
####


@app.callback(Output('tab-output', 'children'),
              [Input('intermediate-value', 'children'),
               Input('tabs', 'value')])
def display_content(diffy ,value):
    diffy = json.loads(diffy)
    code_start = diffy["code_start"]
    d = cr.dic(code_start)
    layout = html.Div([dcc.Graph(id='rating_chart', figure=d["fig_overall"], config={'displayModeBar': False},
                                 style={"margin-top": "0mm"})])
    if value == "Overall":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=d["fig_overall"], config={'displayModeBar': False},
                                     style={"margin-top": "0mm"})])
    elif value == "Employee":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=d["fig_emp"], config={'displayModeBar': False},
                                     style={"margin-top": "0mm"})])
    elif value == "Management":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=d["fig_mgm"], config={'displayModeBar': False},
                                     style={"margin-top": "0mm"})])
    elif value == "Shareholders":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=d["fig_sha"], config={'displayModeBar': False},
                                     style={"margin-top": "0mm"})])
    elif value == "Customers":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=d["fig_cus"], config={'displayModeBar': False},
                                     style={"margin-top": "0mm"})])
    elif value == "Search":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=d["fig_search"], config={'displayModeBar': False},
                                     style={"margin-top": "0mm"})])


    return layout


@app.callback(Output('tab-output-employee', 'children'),
              [Input('intermediate-value', 'children'),
                Input('tabs-employee', 'value')])
def display_content(diffy, value):
    diffy = json.loads(diffy)
    code_start = diffy["code_start"]
    d = el.dic(code_start)
    l = ll.dic(code_start)
    c = cl.dic(code_start)
    cra = cr.dic(code_start)
    layout = d["interview_layout"]

    if value== "Interview":
        layout = d["interview_layout"]
    elif value== "Sentiment":
        layout = l["language layout"]
    elif value== "Compensation":
        layout = c["compensation_layout"]
    elif value== "Job Map":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=cra["fig_cus"], config={'displayModeBar': False},
                        style={"margin-top": "0mm"})])
    elif value== "Search":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=cra["fig_search"], config={'displayModeBar': False},
                        style={"margin-top": "0mm"})])



    return layout

## Here

@app.callback(Output('tab-output-customer', 'children'),
              [Input('intermediate-value', 'children'),
               Input('tabs-customer', 'value')])
def display_content(diffy, value):

    diffy = json.loads(diffy)
    code_start = diffy["code_start"]
    d = el.dic(code_start)
    l = ll.dic(code_start)
    c = cl.dic(code_start)

    layout = inl.info_layout

    if value== "Infographic":
        layout = inl.info_layout
    elif value== "Map":
        layout = l["language_layout"]
    elif value== "Sentiment":
        layout = c["compensation_layout"]


    return layout



@app.callback(Output('tab-output-interview-bottom', 'children'),
              [Input('intermediate-value', 'children'),
              Input('tabs-interview-bottom', 'value')])
def display_content(diffy, value):
    diffy = json.loads(diffy)
    code_start = diffy["code_start"]
    d = el.dic(code_start)
    layout = d["interview_layout_accepted"]

    if value== "Accepted":
        layout = d["interview_layout_accepted"]
    elif value== "Positive":
        layout = d["interview_layout_positive"]
    elif value== "Negative":
        layout = d["interview_layout_negative"]
    elif value== "Difficult":
        layout = d["interview_layout_difficult"]
    elif value== "Easy":
        layout = d["interview_layout_easy"]

    return layout

@app.callback(Output('tab-output-language', 'children'),
              [Input('intermediate-value', 'children'),
               Input('tabs-language', 'value')])
def display_content(diffy, value):
    diffy = json.loads(diffy)
    code_start = diffy["code_start"]
    d = el.dic(code_start)
    l = ll.dic(code_start)
    c = cl.dic(code_start)

    layout = l["four_figs_layout"]

    if value== "Noun":
        layout = l["four_figs_layout"]
    elif value== "Phrase":
        layout = l["phrase_layout"]
    elif value== "Sentiment":
        layout = d["interview_layout_negative"]
    elif value== "Map":
        layout = d["interview_layout_easy"]

    return layout

@app.callback(Output('tab-output-compensation', 'children'),
              [Input('intermediate-value', 'children'),
               Input('tabs-compensation', 'value')])
def display_content(diffy, value):
    diffy = json.loads(diffy)
    code_start = diffy["code_start"]
    l = ll.dic(code_start)
    c = cl.dic(code_start)

    layout = l["four_figs_layout"]

    if value== "Benefits":
        layout = c["benefits_layout"]
    elif value== "Salaries":
        layout = c["benefits_layout"]
    elif value== "Third":
        layout = c["benefits_layout"]


    return layout




# Our main function
if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server()