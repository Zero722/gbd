import os
import pandas as pd
from files_folders2 import check_folder, mapping, convert_to_csv
from dataframes2 import horizantal_df, vertical_df
def main ():

    csvfiles = os.path.dirname(os.path.abspath(__file__)) + "\csv"
    path_to_json = os.path.dirname(os.path.abspath(__file__)) + "\json"
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    json_files = sorted(json_files, key=lambda files: int(files.split(".")[0]))

    check_folder(csvfiles)
    mapper = mapping(json_files, csvfiles)
    
    final_hor_df = pd.DataFrame()
    final_ver_df = pd.DataFrame()
    y = pd.DataFrame()

    for file in json_files:
    # file = "4.json"

        # hor_df = horizantal_df(path_to_json, file)
        ver_df = vertical_df(mapper[file], path_to_json, file)

        # final_hor_df = pd.concat([final_hor_df, hor_df])
        final_ver_df = pd.concat([final_ver_df, ver_df])


    # convert_to_csv(final_hor_df, csvfiles, "hor.csv")
    convert_to_csv(final_ver_df, csvfiles, "ver.csv")


 
if __name__ == '__main__':
    main()

