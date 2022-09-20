import os
import pandas as pd
import numpy as np
import time

# read data
df = pd.DataFrame()
path = os.getcwd()

path1 = path + "/report"
path2 = path

filepath_1 = os.listdir(path1)
filepath_1 = [ele for ele in filepath_1 if ele.rsplit(".", 1)[1] == "csv"]

# process data
for i in range(len(filepath_1)):

    data = pd.read_csv(path1 + "/" + filepath_1[i], skiprows=2,
                       header=None)

    list1 = []
    for j in range(len(data)):
        list1.extend(data.iloc[j][1:len(data.columns)])

    a = pd.DataFrame(list1)

    df = pd.concat([df, a], axis=1)

df = pd.DataFrame(df.values.T)

# add the first two columns
list1 = []
list2 = []

list3 = list((filepath_1[i].split(".")[0]) for i in range(len(filepath_1)))

for i in range(len(list3)):
    list1.append(list3[i].split("(")[1].replace(")", ""))
    list2.append(list3[i].split("(")[0])

df1 = pd.DataFrame(list1)
df2 = pd.DataFrame(list2)

df = pd.concat([df1, df2, df], axis=1)

# generate column names
data = pd.read_csv(path1 + "/" + filepath_1[1], skiprows=1, header=None)

list4 = []
list5 = []
for i in range(1, len(data)):

    for j in range(1, len(data.columns)):
        name = str(str.lower(data[0][i]) + "_" + str.lower(data.iloc[0][j]).rsplit(".", 1)[0])
        list4.append(name)

list4.insert(0, "filename")
list4.insert(0, "experience_id")

for x in list4:
    list5.append(x.replace("#", "").replace(" ", "_").replace(".", ""))

df.columns = list5

df = df.set_index("experience_id")

date = time.ctime(os.path.getmtime("0_Project1.asc"))
df['date'] = date

# save new document
a = list1[0]
df.to_csv(path2 + "/" + a + ".csv")
