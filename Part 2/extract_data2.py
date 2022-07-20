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


# Done
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
        y = block['y'].squeeze().tolist()
        y = (list(set(y)))[0]
        
        if type(block_list) != list:
            block_list = [block_list]
        
        block_list = list(set(block_list))
        block_list.sort()

        for x in block_list:
            df = df[(df['y'] >= y) & (df['y'] < (y+500))]

            title_df = df[(df['attributes.role'] == "heading") & (df['x'] == (x+12))]["text"]
            price_df = df[(df['element'] == "SPAN") & (df['x'] == (x+12)) & (df['price'] == df['price'])]["price"]
            rating_and_count_df = df[(df['height'] == 32) & (df['attributes.aria-label'] == df['attributes.aria-label']) & (df['x'] == (x+12))]
            rating_df = rating_and_count_df["attributes.aria-label"]
            rating_count_df = rating_and_count_df["text"]
            links_df = df[(df['element'] == "A") & (df['width'] == 128) & (df['x'] == (x+12))]["attributes.href"]

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


# Done
def ads_product(df):

    headers = ["Title", "Price", "Rating", "ReviewCount", "Links"]
    dict_list = []
    block = df[(df['element'] == "G-INNER-CARD") & (df['y'] == 213)]

    if block.empty:
        df_list = [pd.DataFrame] * len(headers)
        data_value = data_cleaning(df_list)
        dictionary = to_dict(data_value, headers)
        dict_list.append(dictionary)
        
    else:
        block_list = block["x"].squeeze().tolist()
        y = block['y'].squeeze().tolist()
        y = (list(set(y)))[0]

        if type(block_list) != list:
            block_list = [block_list]
        
        block_list = list(set(block_list))
        block_list.sort()
        

        for x in block_list:
            df = df[(df['y'] >= y) & (df['y'] < (y+500))]

            title_df = df[(df['element'] == "H4") & (df['x'] == (x+12))]["text"]
            price_df = df[(df['price'] == df['price']) & (df['height'] == 30) & (df['x'] == (x+12))]["price"]
            rating_df = df[(df['element'] == "SPAN") & (df['attributes.aria-label'] == df['attributes.aria-label']) & (df['width'] == 68) & (df['x'] == (x+12))]["attributes.aria-label"]
            rating_count_df = df[(df['element'] == "SPAN") & (df['attributes.aria-label'] == df['attributes.aria-label']) & (df['height'] == 24) & (df['x'] == (x+82))]["text"]
            links_df = df[(df['element'] == "A") & (df['y'] == 213) & (df['x'] == x)]["attributes.href"]

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
    

# Block done others left
def organic_data(df):
    
    headers = ["Title", "Price", "Rating", "ReviewCount", "Links"]
    dict_list = []
    block = df[(df['element'] == 'A') & (df['width'] > 1033) & (df['width'] < 1037) & ((df['height'] == 84) | (df['height'] == 110))]
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

            title_df = df[(df['width'] > 1001) & (df['width'] < 1005) & (df['attributes.role'] == "link") & (df['y'] > y) & (df['y'] < next_y)]["text"]
            links_df = block[block['y'] == y]["attributes.href"]
            rating_df = df[(df['element'] == "SPAN") & (df['attributes.role'] == "img") & (df['width'] == 68) & (df['attributes.aria-label'] == df['attributes.aria-label']) & (df['y'] > y) & (df['y'] < next_y)]["attributes.aria-label"]
            rating_count_df = df[(df['element'] == "SPAN") & (df['height'] == 16)  & (df['text'].str.contains('\(')) & (df['x'] > 109) & (df['x'] < 150) & (df['y'] > y) & (df['y'] < next_y)]["text"]
            # price_df = df[((df['element'] == "DIV") & (df['height'] == 20)) & (df['width'] > 1001)  & (df['width'] < 1005)  & (df['attributes.data-content-feature'] != (df['attributes.data-content-feature'] )) & (df['x'] == 16) & (df['x'] == 16) & (df['y'] > y) & (df['y'] < next_y)]["text"]
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


# Done
def map_data(df):

    headers = ["Title", "OpeningClosing", "Rating", "ReviewCount", "Address"]
    dict_list = []
    block = df[(df['element'] == 'A') & (df['width'] == 895)]
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

            title_df = df[(df['width'] == 879) & (df['y'] == y + 13) & (df['attributes.role'] == "heading")]["text"]
            rating_df = df[(df['element'] == "SPAN") & (df['attributes.role'] == "img") & (df['attributes.aria-label'] == df['attributes.aria-label']) & (df['y'] > y) & (df['y'] < next_y)]["attributes.aria-label"]
            rating_count_df = df[(df['element'] == "SPAN") & (df['attributes.role'] == "text") & (df['attributes.aria-label'] == df['attributes.aria-label']) & (df['y'] == y + 35)]["text"]
            address_df = df[(df['height'] == 18) & (df['width'] == 879) & (df['y'] == y + 53)]["text"]
            opening_closing_df = df[(df['height'] == 18) & (df['width'] == 879) & (df['y'] == y + 71)]["text"]

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


# Done
def related_search_data(df):

    headers = ["Title", "Link"]
    dict_list = []
    block = df[(df['element'] == 'A') & (df['width'] == 1003) & (df['height'] == 48)]
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

        for y in block_list:

            title_df = block[block['y'] == y]["text"]
            links_df = block[block['y'] == y]["attributes.href"]
            
            df_list = [title_df, links_df]

            data_value = data_cleaning(df_list)
                    
            dictionary = to_dict(data_value, headers)
            dict_list.append(dictionary)

    # for i in dict_list:
    #     pprint.pprint(i)
    #     print()
    return dict_list
