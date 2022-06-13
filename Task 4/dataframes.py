import pandas as pd
import json
from extract_data import popular_product, ads_product, organic_data

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
        final_series = pd.concat([final_series,series2[i]])

    final_series['Index'] = index_ver
    final_series = final_series.set_index("Index")
    final_series = final_series.rename(columns={0: 'Fields', 1: 'Values'})

    return final_series


def horizantal_df(path_to_json, file):

    data = json.load(open(path_to_json + "\\" + file))
    all_data = pd.json_normalize(data["data"])
    required_data = []

    popular = popular_product(all_data)
    ads = ads_product(all_data)
    organic = organic_data(all_data)

    required_data.extend(popular)
    required_data.extend(ads)
    required_data.extend(organic)

    hor_df = pd.DataFrame(required_data)

    index_list = [file] * len(hor_df)
    hor_df['Index'] = index_list
    hor_df = hor_df.set_index("Index")
    hor_df.index.names = ['File Name']

    return hor_df
