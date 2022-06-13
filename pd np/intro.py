import pandas as pd

data = {
    'fruits':['apple','banana','mango'],
    'color':['red','yellow','green']
}

con = pd.DataFrame(data)
x = [1,3,4]

print(con)

ser2 = pd.Series(x, index=["x","y","z"])
print(ser2)
print(ser2["y"])

#################################

print("\n\n\n\n")

weather = {
    "temp" : [34,32,33,36],
    "rain" : [2,3,4,5]
}

df = pd.DataFrame(weather)
print(df)
print(df.loc[[0,2]])

df2 = pd.DataFrame(weather, index = ["day1", "day2", "day3", "day4"])
print(df2)
print(df2.loc["day3"])
