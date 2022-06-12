import json
from operator import index
import os
from itertools import cycle
import pandas as pd
import pprint

csvfiles = os.path.dirname(os.path.abspath(__file__)) + "\csv"
path_to_json = os.path.dirname(os.path.abspath(__file__)) + "\json"
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
json_files = sorted(json_files, key=lambda files: int(files.split(".")[0]))

def check_folder():
    if(not os.path.isdir(csvfiles)):
        os.mkdir(csvfiles)

def data_cleaning(df_list, split_key, category):

    data_value = [None] * len(df_list)
    for i in range(len(df_list)):
        if df_list[i].empty:
            data_value[i] = "N/A"
        else:
            data_value[i] = df_list[i].squeeze()

        if (type(data_value[i]) != str):
            data_value[i] = data_value[i].to_list()[0]

    if (data_value[2] != "N/A"):
        data_value[2] = data_value[2].split(split_key)[0]

    if (data_value[3] != "N/A"):
        data_value[3] = data_value[3][1:-1]

    data_value.append(category)
    
    return data_value

def to_dict(data_value):
    headers = ["Title", "Price", "Rating", "Rating Count", "Links", "Category"]
    dictionary = {}
    for i in range(len(headers)):
        dictionary[headers[i]] = data_value[i]

    return dictionary

check_folder()
file = "12.json"

data = json.load(open(path_to_json + "\\" + file))
df = pd.json_normalize(data["data"])
df = pd.DataFrame(df)

# for file in (json_files):
#     print(file)
#     data = json.load(open(path_to_json + "\\" + file))
#     df = pd.json_normalize(data["data"])
#     df = pd.DataFrame(df)
#     ads_product(df)
#     print()

def popular_product(df):

    block = df[df['parentNode'] == "DIV.gXGikb.wTrwWd"]
    block_list = block["x"].squeeze().tolist()

    if type(block_list) != list:
        block_list = [block_list]
    dict_list = []

    for x in block_list:
        title_df = df[(df['attributes.class'] == "sjNxlc PZOoVe Ru28Ob") & (df['x'] == (x+12))]["text"]
        price_df = df[(df['attributes.class'] == "Ca9OG") & (df['x'] == (x+12))]["text"]
        rating_df = df[(df['attributes.class'] == "TskR3d") & (df['x'] == (x+12))]["attributes.aria-label"]
        rating_count_df = df[(df['attributes.class'] == "TskR3d") & (df['x'] == (x+12))]["text"]
        links_df = df[(df['attributes.class'] == "a-no-hover-decoration") & (df['x'] == (x+12))]["attributes.href"]
        
        df_list = [title_df, price_df, rating_df, rating_count_df, links_df]
        split_key = ". Rated"

        data_value = data_cleaning(df_list, split_key, "Popular")
        
        dictionary = to_dict(data_value)
        dict_list.append(dictionary)

    # for i in dict_list:
    #     pprint.pprint(i)
    #     print()
    return dict_list


def ads_product(df):

    block = df[df['attributes.class'] == "pla-unit-container VoEfsd"]
    block_list = block["x"].squeeze().tolist()

    if type(block_list) != list:
        block_list = [block_list]

    dict_list = []
    for x in block_list:
        title_df = df[(df['attributes.class'] == "bXPcId pymv4e") & (df['x'] == (x+12))]["text"]
        price_df = df[(df['attributes.class'] == "dOp6Sc") & (df['x'] == (x+12))]["text"]
        rating_df = df[(df['attributes.class'] == "z3HNkc") & (df['x'] == (x+12))]["attributes.aria-label"]
        rating_count_df = df[(df['attributes.class'] == "GhQXkc") & (df['x'] == (x+82))]["text"]
        # shop_name_df = df[(df['attributes.class'] == "hBvPxd zPEcBd") & (df['x'] == (x+12))]["text"]
        links_df = df[(df['attributes.class'] == "pla-unit") & (df['x'] == x)]["attributes.href"]

        df_list = [title_df, price_df, rating_df, rating_count_df, links_df]
        split_key = ","

        data_value = data_cleaning(df_list, split_key, "Advertisement")        
                
        dictionary = to_dict(data_value)
        dict_list.append(dictionary)

    # for i in dict_list:
    #     pprint.pprint(i)
    #     print()
    return dict_list
    

def organic_data(df):

    block = df[df['attributes.class'] == "mnr-c xpd O9g5cc uUPGi"]
    block_list = block["y"].squeeze().tolist()

    if type(block_list) != list:
        block_list = [block_list]

    block_list = list(set(block_list))
    block_list.sort()
    cycle_block_list = cycle(block_list)
    next_y = next(cycle_block_list)
    dict_list = []

    for y in block_list:
        next_y = next(cycle_block_list)
        if y == block_list[-1]:
            next_y = y + 1000

        title_df = df[(df['attributes.class'] == "q8U8x MBeuO ynAwRc oewGkc LeUQr") & (df['y'] > y) & (df['y'] < next_y)]["text"]
        links_df = df[(df['attributes.class'] == "cz3goc BmP5tf") & (df['y'] == y)]["attributes.href"]
        rating_df = df[(df['attributes.class'] == "z3HNkc") & (df['y'] > y) & (df['y'] < next_y)]["attributes.aria-label"]
        rating_count_df = df[(df['attributes.class'] == "HypWnf YrbPuc") & (df['y'] > y) & (df['y'] < next_y)]["text"]
        price_df = df[(df['attributes.class'] == "jC6vSe") & (df['y'] > y) & (df['y'] < next_y)]["text"]

        df_list = [title_df, price_df, rating_df, rating_count_df, links_df]
        split_key = ","

        data_value = data_cleaning(df_list, split_key, "Organic")
                
        # if price_df.empty:
        #     price = 'N/A'
        # else:
        #     price = (price_df.squeeze()).split('\xa0·\xa0')
        # print(price)

        dictionary = to_dict(data_value)
        dict_list.append(dictionary)

    # for i in dict_list:
    #     pprint.pprint(i)
    #     print()
    return dict_list
    
final = []    
popular = popular_product(df)
ads = ads_product(df)
organic = organic_data(df)

final.extend(popular)
final.extend(ads)
final.extend(organic)

# pprint.pprint(final)

df = pd.DataFrame(final)

index_list = [file] * len(df)
df['Index'] = index_list
df = df.set_index("Index")
df.index.names = ['File Name']

df.to_csv("hor.csv")
