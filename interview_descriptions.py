
import pickle
import pandas as pd

p = "BJRI_gd_"

rents = pickle.load(open(p+"rents.p", "rb"))

neg_que = rents["Negative", "questions"]

neg_com = rents["Negative", "comments"]