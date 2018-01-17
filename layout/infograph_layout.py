import layout.donuts_interview as di
import dash
from dash.dependencies import Input, Output
#import dash_core_components2 as dcc2
import dash_core_components as dcc
import dash_html_components as html
import processing.interview_descriptions as ides
import _pickle as pickle
import os

my_path = os.path.abspath(os.path.dirname(__file__))
path_2 = os.path.join(my_path, "../input_fields.csv")
path_in_ngrams = os.path.join(my_path, "../data/cpickle/")


coy = "BJRI"
city = "burbank"
bench = "CAKE"

figures_dict = pickle.load(open(path_in_ngrams + "figures_dict_"+coy+".p", "rb"))
fig_d = figures_dict[coy,city]
fig_b = figures_dict[coy,city]

#fig_d_n = figures_dict[coy]
#fig_b_n = figures_dict[bench]


male_female_ratio = fig_d["Male to Female"]

for_loc_ratio = fig_d["Foreign to Local"]

male_rate = fig_d["Male"]

female_rate =  fig_d["Female"]

local_rate  = fig_d["Local"]

foreign_rate = fig_d["Foreign"]

high_net_rate = fig_d["High Network"]

low_net_rate = fig_d["Low Network"]

high_mean_rate_rev = fig_d["Connoisseur"]

high_mean_rate_pho = fig_d["Food Aestheticist"]

patrons_rating = fig_d["Patrons"]

first_timers_rating = fig_d["First Visit"]

visual_index = fig_d["Visual Importance"]

fem_net_imp = fig_d["Female Importance"]

for_loc_reach = fig_d["Foreign Importance"]

network_num = fig_d["Average Customer Network"]

friend_num = fig_d["Total Network"]

unique_num = fig_d["Number of Reviewers"]


info_layout = html.Div([

    html.Div([

        html.Div([
            dcc.Dropdown(
                id='firm_location',
                options=[{'label': r, 'value': v} for r, v in
                         zip(["Calculations", "Income Statement", "Cash Flow Statement", "Balance Sheet"],
                             ["calculations", "income_statement", "cash_flow", "balance_sheet"])],
                value="calculations",
                clearable=False,
                className="dropper"
            )
        ], style={'background-color': "white", 'color': 'rgb(217, 224, 236)', 'float': 'left',
                  'padding-right': '1cm', 'width': '30%'}),

        html.Div([
            dcc.Dropdown(
                id='benchmark',
                options=[{'label': i, 'value': i} for i in ["Normalised", "Original", "Correlated Fundamentals"
                    , "Price Correlated", "Principal Component", "Better Than Bench", "Worse Than Bench", "Volatile",
                                                            "Stable"]],
                value="Normalised",
                clearable=False,
                className="dropper"
            )
        ], style={'background-color': 'white', 'padding-right': '1cm', 'color': 'rgb(217, 224, 236)', 'float': 'left',
                  'width': '35%'}),

        html.Div([
            dcc.Dropdown(
                id='bench_location',
                options=[{'label': r, 'value': v} for r, v in zip(["BJs", "Chipotle"], ["BJRI", "CMG"])],
                value="BJRI",
                clearable=False,
                className="dropper"
            )
        ], style={'background-color': 'white', 'color': 'rgb(217, 224, 236)', 'float': 'left',
                  'width': '30%'})
        # , 'float': 'right', 'display': 'inline-block'
    ], style={'background-color': 'white', 'padding-left': '1.8cm', 'clear': 'both', 'padding-top': '0.3cm'},
        className="double_drop"),


        html.Div([

            html.Div([

                html.Div([

                    html.H5("Description"),
                    html.Div([

                        html.Div([
                            html.Br([]),
                            html.Br([]),
                            html.H5("Reviewers", id='info_1',style={'margin-top':'8px'}),
                            html.H5("Network"),
                            html.H5("Patron"),
                            html.H5("Connoisseur")

                        ])

                    ],),
                ], style={'display': 'table-cell', 'width': '150px'}),

                html.Div([


                    html.H5("Local"),
                    html.Div([

                        html.Div([
                            html.H5("Company"),

                            html.H5("{:,}".format(unique_num),id='info_1'),
                            html.H5("{:,}".format(friend_num),id='info_1'),
                            html.H5(str(round(patrons_rating, 2))),
                            html.H5(str(round(high_mean_rate_rev, 2)))

                        ],style={'display': 'table-cell','width':'175px'}),

                        html.Div([
                            html.H5("Bench  "),
                            html.H5("{:,}".format(unique_num),id='info_1'),
                            html.H5("{:,}".format(friend_num),id='info_1'),
                            html.H5(str(round(patrons_rating, 2))),
                            html.H5(str(round(high_mean_rate_rev, 2))),

                        ],style={'display': 'table-cell'}),

                    ],style={'display': 'table'}),
                         ],style={'display': 'table-cell','width':'200px'}),

                    html.Div([


                    html.H5(""),
                    html.Div([

                        html.Div([
                            html.H5(""),
                            html.H5(""),

                        ],style={'display': 'table-cell','width':'175px'}),

                        html.Div([
                            html.H5(""),

                        ],style={'display': 'table-cell'}),

                    ],style={ 'display': 'table'}),
                         ],style={'display': 'table-cell','width':'40px'}),

                html.Div([

                    html.H5("National"),
                    html.Div([

                        html.Div([
                            html.H5("Company"),
                            html.H5("{:,}".format(unique_num),id='info_1'),
                            html.H5("{:,}".format(friend_num),id='info_1'),
                            html.H5(str(round(patrons_rating, 2))),
                            html.H5(str(round(high_mean_rate_rev, 2))),

                        ], style={'display': 'table-cell', 'width': '175px'}),

                        html.Div([
                            html.H5("Bench"),
                            html.H5("{:,}".format(unique_num),id='info_1'),
                            html.H5("{:,}".format(friend_num),id='info_1'),
                            html.H5(str(round(patrons_rating, 2))),
                            html.H5(str(round(high_mean_rate_rev, 2))),

                        ], style={'display': 'table-cell'}),

                    ], style={ 'display': 'table'}),
                        ],style={'display': 'table-cell'}),

                    ],style={'display': 'table'})

                ],style={'margin-top': '1.5cm'}),

            ])


interview_layout_accepted =   html.Div([
                dcc.Graph(id='offer_figs', figure=di.offer_fig, config={'displayModeBar': False},
                          style={'position': 'relative', 'top': '-14px','left': '-110px'})

                     ], style={'width': '100%', 'height': '430px', 'overflow': 'hidden'})


import pickle
import pandas as pd


rents = pickle.load(open(path_in_ngrams + coy+"_gd_rents.p", "rb"))

neg_que = rents["Negative", "questions"]

neg_com = rents["Negative", "comments"]

mkdwn = ""
fr = 0
for i in neg_que:
    fr = fr +1
    if fr <= 5:
        cos = "###### " +str(fr) +". " + i + "\n"
        mkdwn = mkdwn + cos

interview_layout_negative =   \
    html.Div([

        html.H5("Summary"),
        html.Div([dcc.Textarea(id='neg_int_sum', placeholder='Summary', value=neg_com, style={'width': '98%', 'height':'140px'}
                        )], style={'padding-top':'25px','clear':'both'}),
        html.H5("Top Questions", style={'padding-bottom':'25px'}),
        dcc.Markdown(mkdwn

        )

            ],style={'position': 'relative','left': '20px'})


## Positive

pos_que = rents["Positive", "questions"]

pos_com = rents["Positive", "comments"]

mkdwn = ""
fr = 0
for i in pos_que:
    fr = fr +1
    if fr <= 5:
        cos = "###### " +str(fr) +". " + i + "\n"
        mkdwn = mkdwn + cos

interview_layout_positive =   \
    html.Div([

        html.H5("Summary"),
        html.Div([dcc.Textarea(id='pos_int_sum', placeholder='Summary', value=pos_com, style={'width': '98%', 'height':'140px'}
                        )], style={'padding-top':'25px','clear':'both'}),
        html.H5("Top Questions", style={'padding-bottom':'25px'}),
        dcc.Markdown(mkdwn

        )

            ],style={'position': 'relative','left': '20px'})


# Difficult

dif_que = rents["Difficult", "questions"]

dif_com = rents["Difficult", "comments"]

mkdwn = ""
fr = 0
for i in dif_que:
    fr = fr +1
    if fr <= 5:
        cos = "###### " +str(fr) +". " + i + "\n"
        mkdwn = mkdwn + cos

interview_layout_difficult =   \
    html.Div([

        html.H5("Summary"),
        html.Div([dcc.Textarea(id='dif_int_sum', placeholder='Summary', value=dif_com, style={'width': '98%', 'height':'140px'}
                        )], style={'padding-top':'25px','clear':'both'}),
        html.H5("Top Questions", style={'padding-bottom':'25px'}),
        dcc.Markdown(mkdwn

        )

            ],style={'position': 'relative','left': '20px'})

# Easy

eas_que = rents["Easy", "questions"]

eas_com = rents["Easy", "comments"]

mkdwn = ""
fr = 0
for i in eas_que:
    fr = fr +1
    if fr <= 5:
        cos = "###### " +str(fr) +". " + i + "\n"
        mkdwn = mkdwn + cos

interview_layout_easy =   \
    html.Div([

        html.H5("Summary"),
        html.Div([dcc.Textarea(id='eas_int_sum', placeholder='Summary', value=eas_com, style={'width': '98%', 'height':'140px'}
                        )], style={'padding-top':'25px','clear':'both'}),
        html.H5("Top Questions", style={'padding-bottom':'25px'}),
        dcc.Markdown(mkdwn

        )

            ],style={'position': 'relative','left': '20px'})

