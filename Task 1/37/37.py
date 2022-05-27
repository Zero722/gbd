import json
import pandas as pd

data = json.load(open('37.json'))
df = pd.json_normalize(data["data"])
df =pd.DataFrame(df)
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
df_new.to_csv("37a.csv")
# df.to_csv("37.csv")