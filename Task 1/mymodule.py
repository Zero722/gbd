from cmath import nan
import json, os, csv
from numpy import NaN
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Declare file path
csvfiles = os.path.dirname(os.path.abspath(__file__)) + "\csv"
path_to_json = os.path.dirname(os.path.abspath(__file__)) + "\json"
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
json_files = sorted(json_files, key=lambda files: int(files.split(".")[0]))

# Create required  folder if it doesn't exist
def check_folder():
    if(not os.path.isdir(csvfiles)):
        os.mkdir(csvfiles)

# Convert json file to horizantal dataframe
def horizantal_df(file):
    index_hor=[]
    data = json.load(open(path_to_json + "\\" + file))
    df = pd.json_normalize(data["data"])
    df = pd.DataFrame(df)

    # Extract title
    title_df = df[df['element'] == "TH"]
    title_df = title_df[["text"]]
    title_ser = title_df['text'].squeeze()
    titles = title_ser.tolist()
    titles.append("")

    # Extract required data
    df2 = df[df['element'].str.contains('TD') & df['attributes.class'].str.contains('SH30Lb') & df['y']!=0]
    unique_y = df2['y'].unique()
    x = file

    # Process for empty table
    if (len(df2) == 0):
        df_new = pd.DataFrame(columns=titles)
        df_new.loc[0] = ["NA"] * len(titles)
        index_hor.append(str(x))

    # Process for non-empty table
    else:
        l = len(unique_y)
        df_split = [None] * l
        series = [None] * l

        for i in range(l):
            df_split[i] = df2[df2['y'] == unique_y[i]]
            df_split[i] = df_split[i][["text"]]
            df_split[i] = df_split[i].reset_index(drop=True)
            series[i] = df_split[i]['text'].squeeze()
            index_hor.append(str(x))

        df_new = pd.concat(series, axis=1).T
        df_new = df_new.reset_index(drop=True)
        df_new.head()

        df_new = df_new.iloc[:, :5]
        df_new.columns = titles

        # Clean data
        df_new["Sold by"] = df_new["Sold by"].str.split('Opens in a new window').str[0]
        df_new["Total price"] = df_new["Total price"].str.split('Item').str[0]
    df_new = df_new.iloc[:, :-1]

    # Process Empty cell
    for i in range(df_new.shape[0]):  # iterate over rows
        for j in range(df_new.shape[1]):  # iterate over columns
            if df_new.loc[i][j] == "":
                df_new.loc[i][j] = "NA"
    
    df_new['Index'] = index_hor
    df_new = df_new.set_index("Index")
    df_new.index.names = ['File Name']

    return df_new

# Convert horizantal dataframe to vertical dataframe
def vertical_df(mapper, df):
    index_ver = []
    df = df.reset_index(drop = True)

    total_col = len(df.columns)
    series2 = [None] * total_col
    x= mapper
    index_ver.clear()

    for i in range(total_col):
        series2[i] = df.iloc[:, i]
        title_list = [series2[i].name] * len(df)
        series_title = pd.Series(title_list)
        series2[i].name = None
        series2[i] = pd.concat([series_title, series2[i]], axis=1)

        # Indexing
        for j in range(len(df)):
            index_ver.append(str(x) + '.' + str(j+1) + '.' + str(i+1))

    final_series = pd.DataFrame()
    for i in range(total_col):
        final_series = final_series.append(series2[i])

    final_series['Index'] = index_ver
    final_series = final_series.set_index("Index")
    final_series = final_series.rename(columns={0: 'Fields', 1: 'Values'})

    return final_series


def convert_one_file_hor(file, df):
    x = file.split(".")
    x = x[0]
    x_to_csv = x + "_hor.csv"
    df.to_csv(csvfiles + '\\' + x_to_csv)


def convert_one_file_ver(mapper, df):
    df_to_csv = str(mapper) + "_ver.csv"
    df.to_csv(csvfiles + '\\' + df_to_csv)

# Convert all file to 1 horizantal csv
def all_hor(json_files):
    final_df0 = pd.DataFrame()

    for file in (json_files):
        df = horizantal_df(file)
        final_df0 = final_df0.append(df)

    final_df0.to_csv(csvfiles + '\\' + "final_horizantal.csv")

# Convert all file to 1 vertical csv
def all_ver(json_files):
    final_df = pd.DataFrame()
    mapper = mapping(json_files)
    for file in (json_files):
        df = vertical_df(mapper[file], horizantal_df(file))
        final_df = final_df.append(df)

    final_df.to_csv(csvfiles + '\\' + "final_vertical.csv")


def mapping(json_files):
    dict = {}
    for i in range(len(json_files)):
        dict[json_files[i]] = i+1

    with open(csvfiles + '\dict.csv', 'w', newline='') as csv_file:  
        writer = csv.writer(csv_file)
        writer.writerow(["FN", "Index"])
        for key, value in dict.items():
            writer.writerow([key, value])

    return dict
