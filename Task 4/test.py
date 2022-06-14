import os, json
import pandas as pd
from files_folders import check_folder, mapping, convert_to_csv
from dataframes import horizantal_df
from extract_data import popular_product, ads_product, organic_data


def vertical_df(mapper, path_to_json, file):

    data = json.load(open(path_to_json + "\\" + file))
    all_data = pd.json_normalize(data["data"])
    final_series = pd.DataFrame()

    required_data = []

    popular = popular_product(all_data)
    ads = ads_product(all_data)
    organic = organic_data(all_data)

    category_list = [popular, ads, organic]
    index_ver = []

    index_ver.clear()


    for idx, element in enumerate(category_list):
        df = pd.DataFrame(element)
        df = df.reset_index(drop = True)

        category = ["Popular", "Ads", "Organic"]

        total_col = len(df.columns)
        series2 = [None] * total_col
        x= mapper

        for i in range(total_col):
            series2[i] = df.iloc[:, i]
            title_list = [category[idx] + "_" + series2[i].name] * len(df)
            series_title = pd.Series(title_list)
            series2[i].name = None
            series2[i] = pd.concat([series_title, series2[i]], axis=1)

            # Indexing
            for j in range(len(df)):
                index_ver.append(str(x) + '.' + str(idx+1) + '.' + str(j+1) + '.' + str(i+1))

        for i in range(total_col):
            final_series = pd.concat([final_series,series2[i]])

    final_series['Index'] = index_ver
    final_series = final_series.set_index("Index")
    final_series = final_series.rename(columns={0: 'Fields', 1: 'Values'})

    return final_series

def main ():

    csvfiles = os.path.dirname(os.path.abspath(__file__)) + "\csv"
    path_to_json = os.path.dirname(os.path.abspath(__file__)) + "\json"
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    json_files = sorted(json_files, key=lambda files: int(files.split(".")[0]))
    
    check_folder(csvfiles)
    mapper = mapping(json_files, csvfiles)
    
    final_hor_df = pd.DataFrame()
    final_ver_df = pd.DataFrame()

    for file in json_files:

        hor_df = horizantal_df(path_to_json, file)
        ver_df = vertical_df(mapper[file], path_to_json, file)

        final_hor_df = pd.concat([final_hor_df, hor_df])
        final_ver_df = pd.concat([final_ver_df, ver_df])
    
    convert_to_csv(final_hor_df, csvfiles, "hor.csv")
    convert_to_csv(final_ver_df, csvfiles, "ver.csv")

 
if __name__ == '__main__':
    main()

