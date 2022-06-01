from cmath import nan
import json
import os
from numpy import NaN
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


csvfiles = os.path.dirname(os.path.abspath(__file__)) + "\csv"
path_to_json = os.path.dirname(os.path.abspath(__file__)) + "\json"
json_files = [pos_json for pos_json in os.listdir(
    path_to_json) if pos_json.endswith('.json')]
indexlist = []
index = []


def check_folder():
    if(not os.path.isdir(csvfiles)):
        os.mkdir(csvfiles)


def horizantal_df(file):
    file1 = file
    data = json.load(open(path_to_json + "\\" + file))
    df = pd.json_normalize(data["data"])
    df = pd.DataFrame(df)
    # df.to_csv(csvfiles + '\\' + "80.csv")

    title_df = df[df['element'] == "TH"]
    title_df = title_df[["text"]]
    title_ser = title_df['text'].squeeze()
    titles = title_ser.tolist()
    titles.append("")

    df2 = df[df['element'].str.contains(
        'TD') & df['attributes.class'].str.contains('SH30Lb')]
    unique_y = df2['y'].unique()
    index.clear()
    x = file1.split(".")
    x = x[0]

    if (len(df2) == 0):
        df_new = pd.DataFrame(columns=titles)
        df_new.loc[0] = ["NA"] * len(titles)
        index.append(str(x))

    else:
        l = len(unique_y)
        df_split = [None] * l
        series = [None] * l

        for i in range(l):
            df_split[i] = df2[df2['y'] == unique_y[i]]
            df_split[i] = df_split[i][["text"]]
            df_split[i] = df_split[i].reset_index(drop=True)
            df_split[i] = df_split[i].replace(
                'Opens in a new window', '', regex=True)
            series[i] = df_split[i]['text'].squeeze()
            index.append(str(x))

        df_new = pd.concat(series, axis=1).T
        df_new = df_new.reset_index(drop=True)
        df_new.head()

        df_new = df_new.iloc[:, :5]
        df_new.columns = titles
        # df_new.head()

        df_new["Total price"] = df_new["Total price"].str.split('Item').str[0]

    for i in range(df_new.shape[0]):  # iterate over rows
        for j in range(df_new.shape[1]):  # iterate over columns
            if df_new.loc[i][j] == "":
                df_new.loc[i][j] = "NA"

    return df_new


def vertical_df(file):
    file1 = file
    df = horizantal_df(file)
    df_new = df.iloc[:, :-1]
    total_col = len(df_new.columns)
    series2 = [None] * total_col
    x = file1.split(".")
    x = x[0]
    indexlist.clear()

    for i in range(total_col):
        series2[i] = df_new.iloc[:, i]
        series2[i].to_frame()
        title_list = [series2[i].name] * len(df_new)
        series_title = pd.Series(title_list)
        series2[i].name = None
        series2[i] = pd.concat([series_title, series2[i]], axis=1)

        for j in range(len(df_new)):
            indexlist.append(str(x) + '.' + str(i+1) + '.' + str(j+1))

    final_series = pd.DataFrame()
    for i in range(total_col):
        final_series = final_series.append(series2[i], ignore_index=True)

    return final_series


def convert_one_file_hor(file):
    check_folder()
    df = horizantal_df(file)
    if len(index) != 0:
        df['index'] = index
        df = df.set_index("index")
        df.index.names = ['File name']
    x = file.split(".")
    x = x[0]
    x_to_csv = x + ".csv"
    df.to_csv(csvfiles + '\\' + x_to_csv)


def convert_one_file_ver(file):
    check_folder()
    df = vertical_df(file)
    if len(index) != 0:
        df['index'] = indexlist
        df = df.set_index("index")
        df = df.rename(columns={0: 'Fields', 1: 'Values'})
    x = file.split(".")
    x = x[0]
    x_to_csv = x + "a.csv"
    df.to_csv(csvfiles + '\\' + x_to_csv)


def all_hor():
    check_folder()
    final_df0 = pd.DataFrame()
    indexs = []
    for file in (json_files):
        df = horizantal_df(file)
        final_df0 = final_df0.append(df, ignore_index=True)
        indexs.extend(index)

    final_df0['index'] = indexs
    final_df0 = final_df0.set_index("index")
    final_df0.index.names = ['File name']
    final_df0.to_csv(csvfiles + '\\' + "final0.csv")


def all_ver():
    check_folder()
    final_df = pd.DataFrame()
    indexlists = []
    for file in (json_files):
        df = vertical_df(file)
        final_df = final_df.append(df, ignore_index=True)
        indexlists.extend(indexlist)

    final_df['index'] = indexlists
    final_df = final_df.set_index("index")
    final_df = final_df.rename(columns={0: 'Fields', 1: 'Values'})
    final_df.to_csv(csvfiles + '\\' + "final.csv")
