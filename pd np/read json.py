import pandas as pd
import json

df = pd.read_json('data.json')
print(df.to_string()) 

with open('school_info.json','r') as f:
    data = json.loads(f.read())

    df2 = pd.json_normalize(data, record_path=['students'])
    df3 = pd.json_normalize(data, record_path=['students'], meta=['school_name', 'class'])


print(df2.to_string()) 
print(df3.to_string()) 


