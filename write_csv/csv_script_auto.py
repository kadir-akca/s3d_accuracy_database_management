from os import path, listdir, makedirs
from re import sub

import os
# import re
import shutil
import time
from tkinter import messagebox
from pandas import DataFrame, read_csv, concat

# import pandas as pd

path_data_to_be_merged = 'data_to_be_merged_automatically/'

try:
    files_list_csv = [f for f in listdir(path_data_to_be_merged) if
                      path.isfile(path.join(path_data_to_be_merged, f)) if f.endswith('.csv')]

    experience_id = files_list_csv[0][files_list_csv[0].find("(") + 1:files_list_csv[0].find(")")]

    df_orj = read_csv(path_data_to_be_merged + files_list_csv[0], skiprows=1, header=None)

    col_names = []
    for i in range(df_orj.shape[1] - 1):
        col_names.append(df_orj.iloc[0][i + 1])

    row_names = []
    for i in range(df_orj.shape[0] - 1):
        row_names.append(df_orj.iloc[i + 1][0])

    new_cols = ['experience_id', 'filename']
    for col in col_names:
        for row in row_names:
            new_col = '%s _ %s' % (row, col)
            new_col = new_col.lower()
            new_col = sub('[^.,_a-zA-Z0-9]+', '', new_col)
            new_cols.append(new_col)

    df1 = DataFrame(
        columns=new_cols
    )

    for file in files_list_csv:
        path = path_data_to_be_merged + file
        df_temp = read_csv(path, skiprows=1, header=None)
        datas = [experience_id, "Project_" + str(files_list_csv.index(file))]
        for j in range(df_temp.shape[1] - 1):
            for i in range(df_temp.shape[0] - 1):
                data = df_temp.iloc[i + 1, j + 1]
                data = sub('[^.,_a-zA-Z0-9]+', '', data)
                datas.append(data)
        df2 = DataFrame(
            [datas],
            columns=new_cols
        )
        df1 = concat([df1, df2])

    # osdir command to do
    files_list_asc = [f for f in listdir(path_data_to_be_merged) if f.endswith('.asc')]
    print(time.ctime(os.path.getmtime(path_data_to_be_merged + files_list_asc[0])))

    date = time.ctime(os.path.getmtime(path_data_to_be_merged + files_list_asc[0]))  # ASC file date to take
    df1['date'] = date

    path_experience_id = experience_id
    if not os.path.exists(path_experience_id):
        makedirs(path_experience_id)

    files_to_be_moved = files_list_csv + files_list_asc

    for file_to_be_moved in files_to_be_moved:
        shutil.move(os.path.join(path_data_to_be_merged, file_to_be_moved), experience_id)
    df1.to_csv('%s/' % experience_id + experience_id + ".csv", index=False)

    col_list = []
    for col in df1.columns:
        col_list.append(col)

    messagebox.showinfo("Process finished.", "The merge process is completed.")

except:
    messagebox.showerror("Error", "The merge process failed.\n\nCheck the report folder and the name of the CSV files.")
