import pandas as pd
import os

csvfiles = os.path.dirname(os.path.abspath(__file__)) + "\csv"
def check_folder():
    if(not os.path.isdir(csvfiles)):
        os.mkdir(csvfiles)

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


def convert_one_file_ver(mapper, df):
    df_to_csv = str(mapper) + "_ver.csv"
    df.to_csv(csvfiles + '\\' + df_to_csv)

check_folder()
df = pd.read_csv('recipe.csv')
convert_one_file_ver(1,vertical_df(1, df))