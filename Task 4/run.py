import json
import os
from numpy import NaN
import pandas as pd


csvfiles = os.path.dirname(os.path.abspath(__file__)) + "\csv"
path_to_json = os.path.dirname(os.path.abspath(__file__)) + "\json"
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
json_files = sorted(json_files, key=lambda files: int(files.split(".")[0]))

def check_folder():
    if(not os.path.isdir(csvfiles)):
        os.mkdir(csvfiles)

check_folder()
file = "8.json"

data = json.load(open(path_to_json + "\\" + file))
df = pd.json_normalize(data["data"])
df = pd.DataFrame(df)

def popular_product(df):

    # block = df[df['attributes.class'] == "zj3nWc lJK4uc wOt4nf Wi7Vfd Nplhsf VoEfsd"]
    block = df[df['parentNode'] == "DIV.gXGikb.wTrwWd"]
    block_list = block["x"].squeeze().tolist()

    if type(block_list) != list:
        block_list = [block_list]
    dict_list = []

    for x in block_list:
        title_df = df[(df['attributes.class'] == "sjNxlc PZOoVe Ru28Ob") & (df['x'] == (x+12))]["text"]
        price_df = df[(df['attributes.class'] == "Ca9OG") & (df['x'] == (x+12))]["text"]
        rating_df = df[(df['attributes.class'] == "TskR3d") & (df['x'] == (x+12))]["text"]
        rating_count_df = df[(df['attributes.class'] == "TskR3d") & (df['x'] == (x+12))]["attributes.aria-label"]
        shop_name_df1 = df[(df['parentNode'] == "DIV.NemW5e") & pd.isnull(df['attributes.class']) & (df['x'] == (x+36))]["text"]
        shop_name_df2 = df[(df['attributes.class'] == "JwGc3b") & (df['x'] == (x+12))]["text"]

        df_list = [title_df, price_df, rating_df, rating_count_df]
        data_value = [None] * len(df_list)

        for i in range(len(df_list)):
            if df_list[i].empty:
                data_value[i] = "N/A"
            else:
                data_value[i] = df_list[i].squeeze()

        data_value.append(shop_name_df1.squeeze() + " " + shop_name_df2.squeeze())
        # title = title_df.squeeze()
        # price = price_df.squeeze()
        # rating = rating_df.squeeze()[1:-1]
        # rating_count = rating_count_df.squeeze().split(". Rated")[0]

        dict_list.append({"Title": data_value[0], "Price": data_value[1], "Rating": data_value[2][1:-1], "Shop Name": data_value[4].strip()})

    for i in dict_list:
        print(i)
    # print("Length: ",len(dict_list))

popular_product(df)

# for file in (json_files):
#     print(file)
#     data = json.load(open(path_to_json + "\\" + file))
#     df = pd.json_normalize(data["data"])
#     df = pd.DataFrame(df)
#     popular_product(df)

def ads_product(df):

    # block = df[df['attributes.class'] == "zj3nWc lJK4uc wOt4nf Wi7Vfd Nplhsf VoEfsd"]
    block = df[df['attributes.class'] == "pla-unit-container VoEfsd"]
    block_list = block["x"].squeeze().tolist()

    if type(block_list) != list:
        block_list = [block_list]

    if len(block_list)>0:
        print(file)
        print("Length: ",len(block_list))

    for x in block_list:
        title_df = df[(df['attributes.class'] == "bXPcId pymv4e") & (df['x'] == (x+12))]["text"]
        price_df = df[(df['attributes.class'] == "dOp6Sc") & (df['x'] == (x+12))]["text"]
        rating_count_df = df[(df['attributes.class'] == "z3HNkc") & (df['x'] == (x+12))]["attributes.aria-label"]
        print(rating_count_df)
        # rating_df = df[(df['attributes.class'] == "TskR3d") & (df['x'] == (x+12))]["text"]
        # shop_name_df1 = df[(df['parentNode'] == "DIV.NemW5e") & pd.isnull(df['attributes.class']) & (df['x'] == (x+36))]["text"]
        # shop_name_df2 = df[(df['attributes.class'] == "JwGc3b") & (df['x'] == (x+12))]["text"]

        # df_list = [title_df, price_df, rating_df, rating_count_df]
        # data_value = [None] * len(df_list)
        # dict_list = []


        # for i in range(len(df_list)):
        #     if df_list[i].empty:
        #         data_value[i] = "N/A"
        #     else:
        #         data_value[i] = df_list[i].squeeze()

        # data_value.append(shop_name_df1.squeeze() + " " + shop_name_df2.squeeze())

        # dict_list.append({"Title": data_value[0], "Price": data_value[1], "Rating": data_value[2][1:-1], "Shop Name": data_value[4].strip()})

    
# for file in (json_files):
#     # print(file)
#     data = json.load(open(path_to_json + "\\" + file))
#     df = pd.json_normalize(data["data"])
#     df = pd.DataFrame(df)
#     ads_product(df)
#     print()
    


# rWBhnc
