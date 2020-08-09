import os
import pandas as pd
import csv

a = os.listdir(".\\csvs")
print(a)

output_list = []
for filename in a:

    with open(f"./csvs/"+filename, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            output_list.append(row)

with open(f"test.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["word", "frequency"])
    writer.writerows(output_list)
    # SMOOSH THE CSV DATA TOGETHER

df = pd.read_csv("test.csv", index_col=0)
print(df)


# with open(f"test.csv", newline="") as f:
#     reader = csv.reader(f)
#     for row in reader:
#         print(row)

