# importing pandas package
import pandas as pd
import csv

# for find number of line in csv file for set id

with open("event_info.csv", 'r') as file:
	data = file.readlines()

print(len(data) - 1)

# for update remain capacity after doing some changes

df = pd.read_csv("event_info.csv")
df.head(8)  # prints 3 heading rows
df.loc[df["event_id"] == 5, "remain_capacity"] = 490
df.to_csv("event_info.csv", index=False)
