
from datetime import datetime, timedelta
import pandas as pd
import inflect
import processing.input
import os

my_path = os.path.abspath(os.path.dirname(__file__))
path_2 = os.path.join(my_path, "../input_fields.csv")
path_in = os.path.join(my_path, "../data/stock/")

#input_fields = pd.read_csv(path)
#tick  = [x for x in input_fields[input_fields["ticker"]!="PE"].ticker]

#for t in tick:


def describe(code_start,bench_start):

    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "../input_fields.csv")

    input_fields = pd.read_csv(path)

    company = input_fields[input_fields["code_or_ticker"]==code_start]["short_name"].reset_index(drop=True)[0]

    company_org = input_fields[input_fields["code_or_ticker"]==code_start]["short_name"].reset_index(drop=True)[0]


    tick = " (" + input_fields[input_fields["code_or_ticker"]==code_start]["ticker"].reset_index(drop=True)[0] + ") "


    path = os.path.join(my_path, "../data/stock/")

    #for value in codes:

    #    ben_frs_dict[value] =

    df_com = pd.read_csv(path + code_start + "_tick_df.csv")
    df_ben = pd.read_csv(path + bench_start + "_tick_df.csv")

    date_old_str = df_ben["date"].head(1).values[0]

    s = str(date_old_str)
    days = datetime.now() - datetime(year=int(s[0:4]), month=int(s[5:7]), day=int(s[8:10]))

    years_i = round(days.days / 365)

    df_ben["date"] = pd.to_datetime(df_ben["date"], format="%Y-%m-%d")
    df_com["date"] = pd.to_datetime(df_com["date"], format="%Y-%m-%d")

    p = inflect.engine()
    years_s = p.number_to_words(years_i)



    close_comp = df_ben["close"].tail(1).values[0]
    open_comp = df_ben["close"].head(1).values[0]
    cagr_comp = ((close_comp / open_comp) ** (1 / (days.days / 365)) - 1) * 100

    close_tick = df_com["close"].tail(1).values[0]
    open_tick = df_com["close"].head(1).values[0]
    cagr_tick = ((close_tick / open_tick) ** (1 / (days.days / 365)) - 1) * 100

    now = datetime.now()


    def past_ret(days):

        last_year = now - timedelta(days=days)

        # last_year.strftime("%Y-%m-%d")

        #tick_df["date"] = pd.to_datetime(tick_df["date"], format="%Y-%m-%d")

        diff = (df_com.date - last_year)

        indexmax = (diff[(diff < pd.to_timedelta(0))].idxmax())

        last_year_price_tick = df_com["close"].ix[[indexmax]].values[0]

        ret_y_tick = ((close_tick - last_year_price_tick) / last_year_price_tick) * 100

        df_ben["date"] = pd.to_datetime(df_ben["date"], format="%Y-%m-%d")

        last_year_price_comp = df_ben["close"].ix[[indexmax]].values[0]

        ret_y_comp = ((close_comp - last_year_price_comp) / last_year_price_comp) * 100

        return ret_y_tick, ret_y_comp, last_year_price_tick, last_year_price_comp


    ret_y_tick, ret_y_comp, last_year_price_tick, last_year_price_comp = past_ret(365)

    _, _, last_m_price_tick, last_m_price_comp = past_ret(30)

    ### Month
    m_ret_tick = (close_tick - last_m_price_tick) / last_m_price_tick
    m_ret_comp = (close_comp - last_m_price_comp) / last_m_price_comp

    m_ret_tick - m_ret_comp

    _, _, last_q_price_tick, last_q_price_comp = past_ret(90)

    ### Qtr
    q_ret_tick = (close_tick - last_q_price_tick) / last_q_price_tick
    q_ret_comp = (close_comp - last_q_price_comp) / last_q_price_comp

    q_ret_tick - q_ret_comp

    line = {}
    line[0] = "In the last " + years_s + " years the compounded annual return for "
    line[0.5] = company_org
    line[0.6] = tick + " is "
    line[1] = "negative " if cagr_tick < 0 else "positive "
    line[2] = str(round(abs(cagr_tick), 2)) + "%, compared to the "

    line[3.1] = str(round(abs(cagr_comp), 2)) + "% "
    line[3.5] = "negative " if cagr_comp < 0 else "positive "
    line[4.15] = "return of the benchmark (" + bench_start + "). "
    line[5] = company + " year on year return is "
    line[6] = "negative " if ret_y_tick < 0 else "positive "
    line[7] = str(round(abs(ret_y_tick), 2)) + "% against the benchmark's "
    line[8] = "negative " if ret_y_comp < 0 else "positive "
    line[9] = "return of " + str(round(abs(ret_y_comp), 2)) + "%. "

    if (ret_y_comp < 0) & ((cagr_tick - cagr_comp) > (ret_y_tick - ret_y_comp)):
        line[10] = company + " year on year benchmark adjusted performance has however"
        line[11] = " worsened as measured against the last " + years_s + " year's adjusted return."

    if (ret_y_comp < 0) & ((cagr_tick - cagr_comp) < (ret_y_tick - ret_y_comp)):
        line[10] = company + " year on year benchmark adjusted performance has"
        line[11] = " improved as measured against the last " + years_s + " year's adjusted return."

    if (ret_y_comp > 0) & ((cagr_tick - cagr_comp) > (ret_y_tick - ret_y_comp)):
        line[10] = company + " year on year benchmark adjusted performance has"
        line[11] = " worsened as measured against the last " + years_s + " year's adjusted return."

    if (ret_y_comp > 0) & ((cagr_tick - cagr_comp) < (ret_y_tick - ret_y_comp)):
        line[10] = company + " year on year benchmark adjusted performance has however"
        line[11] = " improved as measured against the last " + years_s + " year's adjusted return."

    # Loop the words instead of all the text, faster more efficient

    line[13] = " In more recent times " + company_org + " has"
    line[14] = " underperformed " if q_ret_tick - q_ret_comp < 0  else " outperformed "
    line[14.4] = "the benchmark on a quarter to quarter basis "

    line[14.5] = "with a quarterly return of " + str(round(q_ret_tick*100,2)) + "% against the " + str(round(q_ret_comp*100,2)) + "% of the benchmark. "


    if (q_ret_tick - q_ret_comp < 0) & (m_ret_tick - m_ret_comp < 0):
        line[14.6] = company_org + " has also"
        line[14.7] = " underperformed the benchmark in the last month."

    if (q_ret_tick - q_ret_comp > 0) & (m_ret_tick - m_ret_comp > 0):
        line[14.6] = company_org + " has also"
        line[14.7] = " outperformed the benchmark in the last month."

    if (q_ret_tick - q_ret_comp < 0) & (m_ret_tick - m_ret_comp > 0):
        line[14.6] = "However, " + company_org + " has"
        line[14.7] = " outperformed the benchmark in the last month."

    if (q_ret_tick - q_ret_comp < 0) & (m_ret_tick - m_ret_comp < 0):
        line[14.6] = "However, " + company_org + " has"
        line[14.7] = " underperformed the benchmark in the last month."

    line[14.8] = " with a monthly return of " + str(round(m_ret_tick*100,2)) + "% against the " + str(round(m_ret_comp*100,2)) + "% of the benchmark."


    final_text = ""
    for i in line.values():
        final_text = final_text + i
    return final_text
