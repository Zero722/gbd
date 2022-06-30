import os
import json
import pandas as pd
csvfiles = os.path.dirname(os.path.abspath(__file__)) + "\csv"
path_to_json = os.path.dirname(os.path.abspath(__file__)) + "\json"
def check_folder():
    if(not os.path.isdir(csvfiles)):
        os.mkdir(csvfiles)

check_folder()

# data = json.load(open(path_to_json + "\\" + file))
# df = pd.json_normalize(data["data"])
# df = pd.DataFrame(df)
# df.to_csv("2.csv")
def convert(x):
    file = str(x) + ".json"

    data = json.load(open(path_to_json + "\\" + file))
    df = pd.json_normalize(data["data"])
    df = pd.DataFrame(df)
    df.to_csv(str(x) + ".csv")

convert(12)