from itertools import cycle
import pandas as pd
import pprint

def data_cleaning(df_list):

    data_value = [None] * len(df_list)
    for i in range(len(df_list)):
        if df_list[i].empty:
            data_value[i] = "N/A"
        else:
            data_value[i] = df_list[i].squeeze()

        if (type(data_value[i]) != str):
            data_value[i] = data_value[i].to_list()[0]
    
    return data_value


def split_and_clean(string, split_key):
    if (string != "N/A"):
        string = string.split(split_key)[0]
    return string


def bracket_remove(string):
    if (string != "N/A"):
        string = string[1:-1]
    return string


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


def opening_closing_filtering(op_cl_block):
    opening_closings = op_cl_block.split(" ⋅ ")
    timings = []
    for opening_closing in opening_closings:
        if "Opens" in opening_closing:
            timings.append(opening_closing)

    if not timings:
        return ("N/A")
    else:
        return timings[0]


def to_dict(data_value, headers):

    dictionary = {}
    for i in range(len(headers)):
        dictionary[headers[i]] = data_value[i]

    return dictionary


def popular_product(df):

    headers = ["Title", "Price", "Rating", "ReviewCount", "Links"]
    dict_list = []
    block = df[(df['element'] == "G-INNER-CARD") & (df['depth'] == 29)]

    if block.empty:
        df_list = [pd.DataFrame] * len(headers)
        data_value = data_cleaning(df_list)
        dictionary = to_dict(data_value, headers)
        dict_list.append(dictionary)
        
    else:
        block_list = block["x"].squeeze().tolist()

        if type(block_list) != list:
            block_list = [block_list]

        for x in block_list:
            title_df = df[(df['attributes.class'] == "sjNxlc PZOoVe Ru28Ob") & (df['x'] == (x+12))]["text"]
            price_df = df[(df['attributes.jsname'] == "HWyexd") & (df['x'] == (x+12))]["text"]
            rating_df = df[(df['attributes.class'] == "TskR3d") & (df['x'] == (x+12))]["attributes.aria-label"]
            rating_count_df = df[(df['attributes.class'] == "TskR3d") & (df['x'] == (x+12))]["text"]
            links_df = df[(df['attributes.class'] == "a-no-hover-decoration") & (df['x'] == (x+12))]["attributes.href"]
            
            df_list = [title_df, price_df, rating_df, rating_count_df, links_df]
            split_key = ". Rated"

            data_value = data_cleaning(df_list)
            data_value[2] = split_and_clean(data_value[2], split_key)
            data_value[3] = bracket_remove(data_value[3])

            dictionary = to_dict(data_value, headers)
            dict_list.append(dictionary)

    # for i in dict_list:
    #     pprint.pprint(i)
    #     print()
    return dict_list


def ads_product(df):

    headers = ["Title", "Price", "Rating", "ReviewCount", "Links"]
    dict_list = []
    block = df[df['attributes.class'] == "pla-unit-container VoEfsd"]

    if block.empty:
        df_list = [pd.DataFrame] * len(headers)
        data_value = data_cleaning(df_list)
        dictionary = to_dict(data_value, headers)
        dict_list.append(dictionary)
        
    else:
        block_list = block["x"].squeeze().tolist()

        if type(block_list) != list:
            block_list = [block_list]

        for x in block_list:
            title_df = df[(df['attributes.class'] == "bXPcId pymv4e") & (df['x'] == (x+12))]["text"]
            price_df = df[(df['attributes.class'] == "dOp6Sc") & (df['x'] == (x+12))]["text"]
            rating_df = df[(df['attributes.class'] == "z3HNkc") & (df['x'] == (x+12))]["attributes.aria-label"]
            rating_count_df = df[(df['attributes.class'] == "GhQXkc") & (df['x'] == (x+82))]["text"]
            # shop_name_df = df[(df['attributes.class'] == "hBvPxd zPEcBd") & (df['x'] == (x+12))]["text"]
            links_df = df[(df['attributes.class'] == "pla-unit") & (df['x'] == x)]["attributes.href"]

            df_list = [title_df, price_df, rating_df, rating_count_df, links_df]
            split_key = ","

            data_value = data_cleaning(df_list) 
            data_value[2] = split_and_clean(data_value[2], split_key)     
            data_value[3] = bracket_remove(data_value[3])
                    
            dictionary = to_dict(data_value, headers)        
            dict_list.append(dictionary)

    # for i in dict_list:
    #     pprint.pprint(i)
    #     print()
    return dict_list
    

def organic_data(df):
    
    headers = ["Title", "Price", "Rating", "ReviewCount", "Links"]
    dict_list = []
    block = df[df['attributes.class'] == "mnr-c xpd O9g5cc uUPGi"]
    if block.empty:
        df_list = [pd.DataFrame] * len(headers)
        data_value = data_cleaning(df_list)
        dictionary = to_dict(data_value, headers)
        dict_list.append(dictionary)
        
    else:
        block_list = block["y"].squeeze().tolist()

        if type(block_list) != list:
            block_list = [block_list]

        block_list = list(set(block_list))
        block_list.sort()
        cycle_block_list = cycle(block_list)
        next_y = next(cycle_block_list)

        for y in block_list:
            next_y = next(cycle_block_list)
            if y == block_list[-1]:
                next_y = y + 315

            title_df = df[(df['attributes.class'] == "q8U8x MBeuO ynAwRc oewGkc LeUQr") & (df['y'] > y) & (df['y'] < next_y)]["text"]
            links_df = df[(df['attributes.class'] == "cz3goc BmP5tf") & (df['y'] == y)]["attributes.href"]
            rating_df = df[(df['attributes.class'] == "z3HNkc") & (df['y'] > y) & (df['y'] < next_y)]["attributes.aria-label"]
            rating_count_df = df[(df['attributes.class'] == "HypWnf YrbPuc") & (df['y'] > y) & (df['y'] < next_y)]["text"]
            price_df = df[((df['attributes.class'] == "jC6vSe") | (df['attributes.class'] == "G1tICe")) & (df['y'] > y) & (df['y'] < next_y)]["text"]

            df_list = [title_df, price_df, rating_df, rating_count_df, links_df]
            split_key = ","

            data_value = data_cleaning(df_list)
            data_value[2] = split_and_clean(data_value[2], split_key)
            data_value[3] = bracket_remove(data_value[3])

                    
            if data_value[1] != "N/A":
                data_value[1] = price_filtering(data_value[1])

            dictionary = to_dict(data_value, headers)
            dict_list.append(dictionary)

    # for i in dict_list:
    #     pprint.pprint(i)
    #     print()
    return dict_list


def map_data(df):

    headers = ["Title", "OpeningClosing", "Rating", "ReviewCount", "Address"]
    dict_list = []
    block = df[df['attributes.class'] == "nitkue"]
    if block.empty:
        df_list = [pd.DataFrame] * len(headers)
        data_value = data_cleaning(df_list)
        dictionary = to_dict(data_value, headers)
        dict_list.append(dictionary)
        
    else:
        block_list = block["y"].squeeze().tolist()

        if type(block_list) != list:
            block_list = [block_list]

        block_list = list(set(block_list))
        block_list.sort()
        cycle_block_list = cycle(block_list)
        next_y = next(cycle_block_list)

        for y in block_list:
            next_y = next(cycle_block_list)
            if y == block_list[-1]:
                next_y = y + 315

            title_df = df[(df['attributes.class'] == "tNxQIb JIFdL rllt__wrap-on-expand lrl-obh") & (df['y'] == y + 13)]["text"]
            rating_df = df[(df['attributes.class'] == "z3HNkc") & (df['y'] > y) & (df['y'] < next_y)]["attributes.aria-label"]
            rating_count_df = df[(df['attributes.class'] == "HypWnf YrbPuc") & (df['y'] == y + 35)]["text"]
            address_df = df[(df['parentNode'] == "DIV.rllt__details") & (df['y'] == y + 53)]["text"]
            opening_closing_df = df[(df['parentNode'] == "DIV.rllt__details") & (df['y'] == y + 71)]["text"]

            df_list = [title_df, opening_closing_df, rating_df, rating_count_df, address_df]
            split_key = ","

            data_value = data_cleaning(df_list)
            data_value[2] = split_and_clean(data_value[2], split_key)
            data_value[3] = bracket_remove(data_value[3])

                    
            if data_value[1] != "N/A":
                data_value[1] = opening_closing_filtering(data_value[1])

            dictionary = to_dict(data_value, headers)
            dict_list.append(dictionary)

    # for i in dict_list:
    #     pprint.pprint(i)
    #     print()
    return dict_list


def related_search_data(df):

    headers = ["Title", "Link"]
    dict_list = []
    block = df[df['attributes.class'] == "iOJVmb"]
    if block.empty:
        df_list = [pd.DataFrame] * len(headers)
        data_value = data_cleaning(df_list)
        dictionary = to_dict(data_value, headers)
        dict_list.append(dictionary)
        
    else:
        block_list = block["y"].squeeze().tolist()

        if type(block_list) != list:
            block_list = [block_list]

        block_list = list(set(block_list))
        block_list.sort()
        cycle_block_list = cycle(block_list)
        next_y = next(cycle_block_list)

        for y in block_list:
            next_y = next(cycle_block_list)
            if y == block_list[-1]:
                next_y = y + 50

            title_df = df[(df['attributes.class'] == "iOJVmb") & (df['y'] >= y) & (df['y'] < next_y)]["text"]
            links_df = df[(df['attributes.class'] == "iOJVmb") & (df['y'] >= y) & (df['y'] < next_y)]["attributes.href"]
            
            df_list = [title_df, links_df]

            data_value = data_cleaning(df_list)
                    
            dictionary = to_dict(data_value, headers)
            dict_list.append(dictionary)

    # for i in dict_list:
    #     pprint.pprint(i)
    #     print()
    return dict_list
