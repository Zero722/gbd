import json
import pandas as pd
data = json.load(open('json/1.json'))

df = pd.json_normalize(data["data"])
df = pd.DataFrame(df)
df.to_csv("1.csv")

# title = "sjNxlc PZOoVe Ru28Ob"
