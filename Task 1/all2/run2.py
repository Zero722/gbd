from mymodule2 import *

def main ():

    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]  
    json_files = sorted(json_files, key=lambda files: int(files.split(".")[0]))
    check_folder()

    mapper = mapping(json_files)

    all_ver(json_files)
    all_hor(json_files)
    for i in range(0,len(json_files),4):
        convert_one_file_ver(mapper[json_files[i]], vertical_df(mapper[json_files[i]],  horizantal_df(json_files[i])))
        # convert_one_file_ver("36.json", vertical_df("36.json",  horizantal_df("36.json")))
        # convert_one_file_ver("40.json", vertical_df("40.json",  horizantal_df("40.json")))
        # convert_one_file_ver("80.json", vertical_df("80.json",  horizantal_df("80.json")))
        convert_one_file_hor(json_files[i], horizantal_df(json_files[i]))
        # convert_one_file_hor("36.json", horizantal_df("36.json"))
        # convert_one_file_hor("40.json", horizantal_df("40.json"))
        # convert_one_file_hor("80.json", horizantal_df("80.json"))
  
if __name__ == '__main__':
    main()




# 36
# 80