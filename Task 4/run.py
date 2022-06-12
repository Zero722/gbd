import os, json
import pandas as pd
from module import check_folder, popular_product, ads_product, organic_data, mapping, vertical_df, horizantal_df

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

        # data = json.load(open(path_to_json + "\\" + file))
        # all_data = pd.json_normalize(data["data"])

        # popular = popular_product(all_data)
        # ads = ads_product(all_data)
        # organic = organic_data(all_data)

        # required_data.extend(popular)
        # required_data.extend(ads)
        # required_data.extend(organic)

        # hor_df = pd.DataFrame(required_data)

        # index_list = [file] * len(hor_df)
        # hor_df['Index'] = index_list
        # hor_df = hor_df.set_index("Index")
        # hor_df.index.names = ['File Name']
        hor_df = horizantal_df(path_to_json, file)
        ver_df = vertical_df(mapper[file], hor_df)

        final_hor_df = pd.concat([final_hor_df, hor_df])
        final_ver_df = pd.concat([final_ver_df, ver_df])
    
    final_hor_df.to_csv(csvfiles + "\\hor.csv")
    final_ver_df.to_csv(csvfiles + "\\ver.csv")


  
if __name__ == '__main__':
    main()

