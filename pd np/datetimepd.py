
import pandas as pd
from datetime import datetime, timedelta
from pandas import DataFrame
df = DataFrame.from_dict(
    {'Courses':["Spark","Hadoop","pandas"],
     'Fee' :[20000,25000,30000],
     'Duration':['30days','40days','35days'],
     'Discount':[1000,2500,1500],
     'Inserted': ["11/22/2021, 10:39:24","11/22/2021, 10:39:24","11/22/2021, 10:39:24"]},
     orient='index', 
     columns=['A','B','C'])
print(df)
