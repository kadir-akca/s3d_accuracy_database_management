import os
import shutil
import time
from tkinter import messagebox

import pandas as pd
import re

path_data_to_be_merged = os.getcwd()
print(path_data_to_be_merged)

try:
    files_list = [f for f in os.listdir(path_data_to_be_merged) if
                  os.path.isfile(os.path.join(path_data_to_be_merged, f))
                  if f.endswith('.csv')]
    print(files_list)
    df_orj = pd.read_csv(files_list[0], skiprows=1, header=None)

    col_names = []
    for i in range(df_orj.shape[1] - 1):
        col_names.append(df_orj.iloc[0][i + 1])

    row_names = []
    for i in range(df_orj.shape[0] - 1):
        row_names.append(df_orj.iloc[i + 1][0])

    new_cols = []
    for col in col_names:
        for row in row_names:
            new_col = '%s _ %s' % (row, col)
            new_col = new_col.lower()
            new_col = re.sub('[^.,_a-zA-Z0-9]+', '', new_col)
            new_cols.append(new_col)

    df1 = pd.DataFrame(
        columns=new_cols
    )

    for file in files_list:
        path = path_data_to_be_merged + file
        df_temp = pd.read_csv(file, skiprows=1, header=None)
        datas = []
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
    print('t1')

    print('t')
    date = time.ctime(os.path.getmtime(files_list[0]))
    df1['date'] = date

    experience_id = files_list[0][files_list[0].find("(") + 1:files_list[0].find(")")]

    '''path_experience_id = experience_id
    if not os.path.exists(path_experience_id):
        os.makedirs(path_experience_id)'''

    '''for file_to_be_moved in files_list:
        shutil.move(os.path.join(path_data_to_be_merged, file_to_be_moved), experience_id)'''

    df1.to_csv(experience_id + ".csv", index=False)

    print(df1.columns)

    col_list = []
    for col in df1.columns:
        col_list.append(col)
    print(col_list)

    messagebox.showinfo("Process finished.", "The merge process is completed.")

    print(df1)


except:
    messagebox.showerror("Error", "The merge process failed.\n\nCheck the report folder and the name of the CSV files.")
