import json
import pandas as pd

data = json.load(open('7.json'))
df = pd.json_normalize(data["data"])
df = pd.DataFrame(df)
# print(df)

title_df = df[df['element']=="TH"]
title_df = title_df[["text"]]
title_ser = title_df['text'].squeeze()
titles = title_ser.tolist()
titles.append("")

df2 = df[df['element'].str.contains('TD') & df['attributes.class'].str.contains('SH30Lb')]
unique_y = df2['y'].unique()

l = len(unique_y)
df_split = [None] * l
series = [None] * l

for i in range(l):
    df_split[i] = df2[df2['y'] == unique_y[i]]
    df_split[i] = df_split[i][["text"]]
    df_split[i] = df_split[i].reset_index(drop=True)
    df_split[i] = df_split[i].replace('Opens in a new window','', regex=True)
    series[i] = df_split[i]['text'].squeeze()
    # print("\n\n")
    # print(series[i])
df_new=pd.concat(series,axis=1).T

df_new = df_new.reset_index(drop=True)


df_new.columns = titles
df_new.head()

df_new["Total price"] = df_new["Total price"].str.split('Item').str[0]

# print(df_new["Total price"])
df_new.to_csv("7a.csv")
# df.to_csv("7.csv")
# ##################################################

# print(df_new)
pd.set_option('display.max_rows', 1000)

df_new = df_new.iloc[: , :-1]
total_col = len(df_new.columns)
series2 = [None] * total_col

for i in range(total_col):
    series2[i] = df_new.iloc[:,i]
    series2[i].to_frame()
    title_list = [series2[i].name] * len(df_new)
    series_title = pd.Series( title_list )
    # print(series2[i])
    # print(series_title)
    series2[i].name = None
    series2[i] = pd.concat([series_title, series2[i]], axis=1)
    # print(df2)

for i in range(1,total_col):
    series2[0] = pd.concat([series2[0], series2[i]], axis=0)

print(series2[0])
