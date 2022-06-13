import pandas as pd

df = pd.read_csv("university_records.csv")
# print(df.describe())
print(df.to_string())
print(df.query("branch == 'COE'"))
tutors = ['William', 'Henry', 'Michael', 'John', 
          'Messi', 'Ramana','Kumar','Vasu']
df2 = df.assign(TutorsAssigned=tutors)
print(df2.to_string())
df3 = df2.drop(columns=["TutorsAssigned"])
df3 = df2.drop(["cgpa"],axis=1)
print(df3.to_string())

# print(df.head(2))
# print(df.info())
# print(pd.options.display.max_rows)