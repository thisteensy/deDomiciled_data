import os
import pandas as pd

from csv_reader import csv_to_dictlist

count_dict = csv_to_dictlist()

df = pd.DataFrame(count_dict)

print(df)


# Read filenames from the given path
# data_files = os.listdir('data/PIT_csv_years/2019')


# def load_files(filenames):
#     for filename in filenames:
# 	    # if filename.endswith(".csv"):
#         df = yield pd.read_csv(
#             filename,
#             header=0,
#             usecol = [0, 1])
#         df["data_year"] = filename[:4]
#         df["state_id"] = 
#     return df 


# df2 = pd.concat(load_files(data_files))

# column_names = ["state_id", "pit_count", "data_year"]
# df_update_colnames = pd.df2(columns = column_names)

# print(df_update_colnames)

# df_cleaned = df.groupby(['state_id','data_year'],as_index=False).agg({'pit_count': 'sum'})

# print(df_cleaned)

