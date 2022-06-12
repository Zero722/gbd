from module import mapping, to_dict, data_cleaning
import json, os, pprint
import pandas as pd
from itertools import cycle

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

        price_block = data_value[1]
                
        if price_block != "N/A":
            prices = price_block.split("\xa0·\xa0")
            price_list = []
            for price in prices:
                price = price.replace('\xa0', ' ')

                if ('(' in price and ')' in price):
                    ind1 = price.index('(') + 1
                    ind2 = price.index(')') - 1
                    if  not str.isdigit(price[ind1]) and str.isdigit(price[ind2]):
                        price_list.append(price)

                if (str.isdigit(price[-1]) and not str.isdigit(price[0])) or price == "Free":
                    price_list.append(price)

            if not price_list:
                data_value[1] = "N/A"
            else:
                data_value[1] = price_list[0]
            print(data_value[1])

        dictionary = to_dict(data_value)
        dict_list.append(dictionary)

    # for i in dict_list:
    #     pprint.pprint(i)
    #     print()
    return dict_list

csvfiles = os.path.dirname(os.path.abspath(__file__)) + "\csv"
path_to_json = os.path.dirname(os.path.abspath(__file__)) + "\json"
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
json_files = sorted(json_files, key=lambda files: int(files.split(".")[0]))

mapper = mapping(json_files, csvfiles)

final_hor_df = pd.DataFrame()
final_ver_df = pd.DataFrame()

for file in json_files:
    data = json.load(open(path_to_json + "\\" + file))
    all_data = pd.json_normalize(data["data"])
    required_data = []

    print()
    print(file)
    organic = organic_data(all_data)
    required_data.extend(organic)

    hor_df = pd.DataFrame(required_data)

    index_list = [file] * len(hor_df)
    hor_df['Index'] = index_list
    hor_df = hor_df.set_index("Index")
    hor_df.index.names = ['File Name']

