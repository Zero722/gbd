import os, csv, json
import pandas as pd
import pprint
from itertools import cycle

def check_folder(files):
    if(not os.path.isdir(files)):
        os.mkdir(files)


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


def price_filtering(price_block):
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
        return ("N/A")
    else:
        return price_list[0]
            

def to_dict(data_value):

    headers = ["Title", "Price", "Rating", "Rating Count", "Links", "Category"]
    dictionary = {}
    for i in range(len(headers)):
        dictionary[headers[i]] = data_value[i]

    return dictionary


def popular_product(df):

    block = df[df['parentNode'] == "DIV.gXGikb.wTrwWd"]
    block_list = block["x"].squeeze().tolist()

    if type(block_list) != list:
        block_list = [block_list]
    dict_list = []

    for x in block_list:
        title_df = df[(df['attributes.class'] == "sjNxlc PZOoVe Ru28Ob") & (df['x'] == (x+12))]["text"]
        # price_df = df[(df['attributes.class'] == "Ca9OG") & (df['x'] == (x+12))]["text"]
        # if price_df.empty:
        #     price_df = df[(df['attributes.class'] == "vy5bA") & (df['x'] == (x+12))]["text"]
        price_df = df[(df['attributes.jsname'] == "HWyexd") & (df['x'] == (x+12))]["text"]
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
            next_y = y + 315

        title_df = df[(df['attributes.class'] == "q8U8x MBeuO ynAwRc oewGkc LeUQr") & (df['y'] > y) & (df['y'] < next_y)]["text"]
        links_df = df[(df['attributes.class'] == "cz3goc BmP5tf") & (df['y'] == y)]["attributes.href"]
        rating_df = df[(df['attributes.class'] == "z3HNkc") & (df['y'] > y) & (df['y'] < next_y)]["attributes.aria-label"]
        rating_count_df = df[(df['attributes.class'] == "HypWnf YrbPuc") & (df['y'] > y) & (df['y'] < next_y)]["text"]
        price_df = df[(df['attributes.class'] == "jC6vSe") & (df['y'] > y) & (df['y'] < next_y)]["text"]

        df_list = [title_df, price_df, rating_df, rating_count_df, links_df]
        split_key = ","

        data_value = data_cleaning(df_list, split_key, "Organic")
                
        if data_value[1] != "N/A":
            data_value[1] = price_filtering(data_value[1])


        dictionary = to_dict(data_value)
        dict_list.append(dictionary)

    # for i in dict_list:
    #     pprint.pprint(i)
    #     print()
    return dict_list


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


def mapping(json_files, folder):
    dict = {}
    for i in range(len(json_files)):
        dict[json_files[i]] = i+1

    with open(folder + '\dict.csv', 'w', newline='') as csv_file:  
        writer = csv.writer(csv_file)
        writer.writerow(["FN", "Index"])
        for key, value in dict.items():
            writer.writerow([key, value])

    return dict

