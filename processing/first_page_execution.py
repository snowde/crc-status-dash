import _pickle as pickle
import os
import pandas as pd
import layout.polar_figure as pf
import json


from processing.stock_narration import describe
import processing.frames as fm
from layout.figures import figs

my_path = os.path.abspath(os.path.dirname('__file__'))

path = os.path.join(my_path, "../data/cpickle/")

dict_all_coll = pickle.load(open(path + "dict_all_coll.p", "rb"))

## Loading input fields
my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "../input_fields.csv")

input_fields = pd.read_csv(path)
from datetime import datetime, timedelta

code_start = input_fields[input_fields["starting"] == 1]["code_or_ticker"].reset_index(drop=True)[0]

code_start_small = input_fields[input_fields["code_or_ticker"] == code_start]["yelp_name"].reset_index(drop=True)[0]

bench_start = input_fields[input_fields["starting"] == 2]["code_or_ticker"].reset_index(drop=True)[0]

bench_start_small = input_fields[input_fields["code_or_ticker"] == bench_start]["yelp_name"].reset_index(drop=True)[0]

available_locations = dict_all_coll[code_start]["Full Address"]
a_small_names = dict_all_coll[code_start]["Adapted Small Name"]

first_option_coy_output = a_small_names[0].title()

the_location = first_option_coy_output
the_benchmark = bench_start

temp_df = pd.DataFrame()
temp_df["available_locations"] = dict_all_coll[code_start]["Full Address"]
temp_df["a_small_names"] = dict_all_coll[code_start]["Adapted Small Name"]

long_addy = temp_df[temp_df["a_small_names"] == the_location]["available_locations"].reset_index(drop=True)[0]

temp_df = pd.DataFrame()
temp_df["available_locations"] = dict_all_coll[code_start]["Available Benchmark"]
temp_df["a_small_names"] = dict_all_coll[code_start]["Available Benchmark Small Name"]

##bench_small = temp_df[temp_df["available_locations"] == the_benchmark]["a_small_names"].reset_index(drop=True)[0]
##  "bench_small":bench_small,
diffy = {'long_addy': long_addy, 'bench_start_small': bench_start_small, "code_start_small": code_start_small,
         'the_location': the_location, 'the_benchmark': the_benchmark, 'code_start': code_start}

available_locations = dict_all_coll[diffy["code_start"]]["Full Address"]
a_small_names = dict_all_coll[diffy["code_start"]]["Adapted Small Name"]

locas_output = [{'label': r, 'value': i} for r, i in zip(available_locations, a_small_names)]

available_locations = dict_all_coll[diffy["code_start"]]["Available Benchmark"]
a_small_names = dict_all_coll[diffy["code_start"]]["Available Benchmark Small Name"]

benchy_output = [{'label': r, 'value': i} for r, i in zip(a_small_names, available_locations)]

s_metrics_df_output = dict_all_coll[diffy["code_start"]]["Stakeholder Metrics"]

s_metrics_df_1_output = dict_all_coll[diffy["code_start"]]["Stakeholder Metrics"]


c_metrics_df_output = dict_all_coll[diffy["code_start"]]["Company Metrics"]


c_metrics_df_output_1 = dict_all_coll[diffy["code_start"]]["Company Metrics"]

df_fund_info_output = pd.read_csv('https://plot.ly/~jackp/17544/.csv')


df_fund_characteristics_output = pd.read_csv('https://plot.ly/~jackp/17542/.csv')


df_fund_facts_output = pd.read_csv('https://plot.ly/~jackp/17540/.csv')


##df_bond_allocation = pd.read_csv('https://plot.ly/~jackp/17538/')

##df_bond_allocation_output = make_dash_table(df_bond_allocation)


desc = describe(diffy["code_start"], diffy["the_benchmark"])
stock_plot_desc_output = desc

title = str(diffy["code_start_small"]) + " 4-D Report"
title_output = title

title = str(diffy["long_addy"]) + " Location"

location_output = title

title = str(diffy["the_location"]) + " Profile"

profile_output = title




df_perf_summary_output = fm.fin_met(diffy["the_benchmark"], diffy["code_start"])

df_perf_summary_output = fm.fin_met(diffy["the_benchmark"], diffy["code_start"])




first_dict = {}
first_dict["locas_output"] = locas_output
first_dict["benchy_output"] = benchy_output
first_dict["first_option_coy_output"] = first_option_coy_output
first_dict["code_start"] = code_start
first_dict["the_benchmark"] = the_benchmark

first_dict["s_metrics_df_output"] = s_metrics_df_output
first_dict["c_metrics_df_output"] = c_metrics_df_output


first_dict["stock_plot_desc_output"] = stock_plot_desc_output

first_dict["title_output"] = title_output
first_dict["location_output"] = location_output
first_dict["profile_output"] = profile_output
first_dict["df_perf_summary_output"] = df_perf_summary_output


my_path = os.path.abspath(os.path.dirname(__file__))

path = os.path.join(my_path, "../data/cpickle/")
print(first_dict)
pickle.dump(first_dict, open(path + "first_page.p", "wb"))

