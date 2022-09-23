import os
import shutil
import time
from tkinter import messagebox

import pandas as pd
import re

path_data_to_be_merged = os.getcwd()

try:
    files_list_csv = [f for f in os.listdir(path_data_to_be_merged) if
                      os.path.isfile(os.path.join(path_data_to_be_merged, f)) if f.endswith('.csv')]

    experience_id = files_list_csv[0][files_list_csv[0].find("(") + 1:files_list_csv[0].find(")")]

    df_orj = pd.read_csv(files_list_csv[0], skiprows=1, header=None)

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
            new_col = re.sub('[^.,_a-zA-Z0-9]+', '', new_col)
            new_cols.append(new_col)

    df1 = pd.DataFrame(
        columns=new_cols
    )

    for file in files_list_csv:
        path = path_data_to_be_merged + file
        df_temp = pd.read_csv(file, skiprows=1, header=None)
        datas = [experience_id, "Project_" + str(files_list_csv.index(file))]
        for j in range(df_temp.shape[1] - 1):
            for i in range(df_temp.shape[0] - 1):
                data = df_temp.iloc[i + 1, j + 1]
                data = re.sub('[^.,_a-zA-Z0-9]+', '', data)
                datas.append(data)
        df2 = pd.DataFrame(
            [datas],
            columns=new_cols
        )
        df1 = pd.concat([df1, df2])

    files_list_asc = [f for f in os.listdir(path_data_to_be_merged) if
                      os.path.isfile(os.path.join(path_data_to_be_merged, f)) if f.endswith('.asc')]

    date = time.ctime(os.path.getmtime(files_list_asc[0]))
    df1['date'] = date

    df1.to_csv(experience_id + ".csv", index=False)

    col_list = []
    for col in df1.columns:
        col_list.append(col)

    messagebox.showinfo("Process finished.", "The merge process is completed.")

except:
    messagebox.showerror("Error", "The merge process failed.\n\nCheck the report folder and the name of the CSV files.")
