import pandas as pd
import os

csvfiles = os.path.dirname(os.path.abspath(__file__)) + "\csv"

index = []
indexlist = []
# horizantal_df = pd.read_csv('recipe.csv') 
# print(horizantal_df)

def check_folder():
    if(not os.path.isdir(csvfiles)):
        os.mkdir(csvfiles)


def vertical_df(file):
    file1 = file
    df_new = pd.read_csv(file)
    # df_new = df.iloc[:, :-1]
    total_col = len(df_new.columns)
    series2 = [None] * total_col
    x = file1.split(".")
    x = x[0]
    indexlist.clear()

    for i in range(total_col):
        series2[i] = df_new.iloc[:, i]
        # series2[i].to_frame()
        title_list = [series2[i].name] * len(df_new)
        series_title = pd.Series(title_list)
        series2[i].name = None
        series2[i] = pd.concat([series_title, series2[i]], axis=1)

        for j in range(len(df_new)):
            indexlist.append(str(x) + '.' + str(i+1) + '.' + str(j+1))

    final_series = pd.DataFrame()
    for i in range(total_col):
        final_series = final_series.append(series2[i], ignore_index=True)

    # print(final_series)
    return final_series

def convert_one_file_ver(file):
    check_folder()
    df = vertical_df(file)
    print(len(index))
    # if len(index) != 0:
    df['index'] = indexlist
    df = df.set_index("index")
    df = df.rename(columns={0: 'Fields', 1: 'Values'})
    x = file.split(".")
    x = x[0]
    x_to_csv = x + "a.csv"
    df.to_csv(csvfiles + '\\' + x_to_csv)

convert_one_file_ver('recipe.csv')