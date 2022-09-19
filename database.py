# Methods that are used for inserting or getting data in/from database.

# Libraries
import logging
import os
import sqlite3
import subprocess
from tkinter import messagebox
import pandas as pd
import psutil

import main

# URL of the database. Needs to be checked always when we change the PC, since we are local.
db_path = 'db.db'
query_insert_into = 'INSERT INTO '
query_values = ' VALUES '
table_experience_column = '''experiences ("experience_id","device_sn", "operator_id","department_id",
            "experience_type_id","artefact_type_id","certificate_number_id","subject")'''
query_param = '(?, ?, ?, ? ,?, ?, ?, ?)'


# Open the database.
def open_db():
    check_process_running = "DB Browser for SQLite.exe" in (p.name() for p in psutil.process_iter())
    if check_process_running is False:
        try:
            os.startfile(db_path)
            logging.info(f'Following database has been opened: {db_path}')
        except subprocess.SubprocessError as e:
            print('Failed to open database', e)
            logging.error(f'Following database could not be opened: {db_path}')
    elif check_process_running is True:
        messagebox.showerror(main.application_title,
                             "Tool is already running.")


def search_last_id(table):
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        last_id = cursor.execute('SELECT MAX(id) FROM %s' % table).fetchall()[0][0]
        connection.commit()
        return last_id
    except sqlite3.Error as err:
        print(f"Error: '{err}'")


# Insert the experience to the database.
def insert_experience(device_sn, operator, department, experience_type, artefact_type, certificate_sn, subject, experience_id):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = query_insert_into + table_experience_column + query_values + query_param
        data = (experience_id, device_sn, operator, department, experience_type, artefact_type, certificate_sn, subject)
        cursor.execute(query, data)
        conn.commit()
    except sqlite3.Error as e:
        logging.error('Experience has not been added to database')
        print('Failed to insert accuracy test in database', e)


# Insert the experience to the database.
def insert_content(content, experience_id):
    print(content, experience_id)
    try:
        if content != '\n' and experience_id != '':
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            insert_query_with_param = """UPDATE experiences SET content = ? WHERE experience_id = ?"""
            data = (content, experience_id)
            cursor.execute(insert_query_with_param, data)
            conn.commit()
            messagebox.showinfo(main.application_title,
                                "The following content has been added successfully to this experience ID:%s\n\n\t"
                                "%s" % (experience_id, content))
        else:
            if content == "\n" and experience_id == '':
                messagebox.showerror(main.application_title,
                                     "Nothing to add to the database!\n\nContent is empty and experience ID has not been found.")
            elif experience_id == '':
                messagebox.showerror(main.application_title,
                                     "Nothing to add to the database!\n\nExperience ID is not found.")
            elif content == "\n":
                messagebox.showerror(main.application_title, "Nothing to add to the database!\n\nContent is empty.")
    except sqlite3.Error as e:
        logging.error('Experience has not been added to database')
        print('Failed to insert accuracy test in database', e)


# Check number of operators in order to see if a new operator is added or not.
def check_operator_id():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM operator")
    results = cursor.fetchall()
    last_id = len(results)
    return last_id


# Get the operators from database to list them in the first page.
def get_operators(department):
    conn = sqlite3.connect(db_path)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    department_id = c.execute('SELECT department_id FROM departments WHERE department = ?', (department,)).fetchone()
    data = c.execute('SELECT operator FROM operators WHERE department_id = ?', (department_id,)).fetchall()
    data = list(dict.fromkeys(data))
    return data


# Get the departments from database to list them in the first page.
def get_departments():
    conn = sqlite3.connect(db_path)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    data = c.execute('SELECT department FROM departments').fetchall()
    data = list(dict.fromkeys(data))
    return data


# Get the experience types from database to list them in the first page.
def get_experience_types():
    conn = sqlite3.connect(db_path)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    data = c.execute('SELECT experience_type FROM experience_types').fetchall()
    data = list(dict.fromkeys(data))
    return data


# Get the artefact SNs from database to list them in the first page.
def get_artefact_types(experience_type):
    conn = sqlite3.connect(db_path)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    experience_type_id = c.execute('SELECT experience_type_id FROM experience_types WHERE experience_type = ?',
                                   (experience_type,)).fetchone()
    data = c.execute('SELECT artefact_type FROM artefact_types WHERE experience_type_id = ?',
                     (experience_type_id,)).fetchall()
    data = list(dict.fromkeys(data))
    return data


def get_certificate_nos(artefact_type):
    conn = sqlite3.connect(db_path)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    artefact_type_id = c.execute('SELECT artefact_type_id FROM artefact_types WHERE artefact_type = ?',
                                 (artefact_type,)).fetchone()
    data = c.execute('SELECT certificate_no FROM certificate_nos WHERE artefact_type_id = ?',
                     (artefact_type_id,)).fetchall()
    return data


# Get the experience IDs from database to list them in the first page.xxx
def get_experience_id(device_sn):
    conn = sqlite3.connect(db_path)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    data = c.execute('SELECT experience_id FROM experiences WHERE device_sn = ?', (device_sn,)).fetchall()
    if len(data) == 0:
        print('Previous experience not found for the following serial number: ', device_sn)
        return 'no experience'
    else:
        print('Previous experience has been found for the following serial number: ', device_sn,
              "\n\t Previous experience is: ", data[-1])
        return data[-1]


# Check if the new experience has been added successfully
def check_experience_id(experience_id):
    conn = sqlite3.connect(db_path)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    data = c.execute('SELECT experience_id FROM experiences').fetchall()
    if experience_id in data:
        return 'exist'


# Get the values by filtering with experience ID
def get_attributes_from_experience_id(expid):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM experiences WHERE experience_id = ?', (expid,))
    data = c.fetchone()
    print('data', data)
    return data


# Select the table where the merged CSV will be inserted
def insert_table_select(url):
    try:
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        df = pd.read_csv(url)
        df_list = df.values.tolist()
        cursor.execute('SELECT experience_type_id FROM experiences WHERE experience_id = ?', (df_list[0][0],))
        arts = cursor.fetchone()
        arts = arts[0]
        print(arts)
        if arts == 'Ball-bar 300':
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS BB300(experience_id, filename, dp0_tol, dp0_dev, dp0_ref, dp0_meas, 
                    dp0__of_points, dp1_tol, dp1_dev, dp1_ref, dp1_meas, dp1__of_points, lp_tol, lp_dev, lp_ref, lp_meas, 
                    lp__of_points, 'date')''')
            insert_table_BB300(url)
            print('inserted to BB300')
        elif arts == 'Ball-bar 500':
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS BB300(experience_id, filename, dp0_tol, dp0_dev, dp0_ref, dp0_meas, 
                    dp0__of_points, dp1_tol, dp1_dev, dp1_ref, dp1_meas, dp1__of_points, lp_tol, lp_dev, lp_ref, lp_meas, 
                    lp__of_points, 'date')''')
            insert_table_BB500(url)
            print('inserted to BB500')
        elif arts == 'BallArray500':
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS BA500(experience_id, filename,'01-02_Tol','01-02_Dev','01-02_Ref_Value',
                    '01-02_Meas_Value','01-02__Of_Points','01-03_Tol','01-03_Dev','01-03_Ref_Value','01-03_Meas_Value',
                    '01-03__Of_Points','01-04_Tol','01-04_Dev','01-04_Ref_Value','01-04_Meas_Value','01-04__Of_Points',
                    '01-05_Tol','01-05_Dev','01-05_Ref_Value','01-05_Meas_Value','01-05__Of_Points','01-06_Tol','01-06_Dev',
                    '01-06_Ref_Value','01-06_Meas_Value','01-06__Of_Points','01-07_Tol','01-07_Dev','01-07_Ref_Value',
                    '01-07_Meas_Value','01-07__Of_Points','01-08_Tol','01-08_Dev','01-08_Ref_Value','01-08_Meas_Value',
                    '01-08__Of_Points','01-09_Tol','01-09_Dev','01-09_Ref_Value','01-09_Meas_Value','01-09__Of_Points',
                    '01-10_Tol','01-10_Dev','01-10_Ref_Value','01-10_Meas_Value','01-10__Of_Points','01-11_Tol','01-11_Dev',
                    '01-11_Ref_Value','01-11_Meas_Value','01-11__Of_Points', 'date')''')
            insert_table_BA500(url)
            print('inserted to BA500')
        else:
            print('exp type not found')
    except:
        messagebox.showwarning("Warning",
                               "Error with sending data to the database!\n\nPlease check if the Experience ID is correct.")


# Insert datas from the merged CSV in BB300 table
def insert_table_BB500(data):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    df = pd.read_csv(data)
    df_list = df.values.tolist()
    for i in df_list:
        insert_query_with_param = "INSERT INTO BB500(exp_ID, Name, dp0_tol, dp0_dev, dp0_ref, dp0_meas, " \
                                  "dp0__of_points, dp1_tol, dp1_dev, dp1_ref, dp1_meas, dp1__of_points, lp_tol, " \
                                  "lp_dev, lp_ref, lp_meas, lp__of_points, Date) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?," \
                                  "?,?,?,?) "
        cursor.execute(insert_query_with_param, i)
        conn.commit()
    messagebox.showinfo("Message", "Inserted to BB500 table successfully.\n\n".join([str(x) for x in df_list]))


def insert_table_BB300(data):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    df = pd.read_csv(data)
    df_list = df.values.tolist()
    for i in df_list:
        insert_query_with_param = "INSERT INTO BB300(exp_ID, Name, dp0_tol, dp0_dev, dp0_ref, dp0_meas, " \
                                  "dp0__of_points, dp1_tol, dp1_dev, dp1_ref, dp1_meas, dp1__of_points, lp_tol, " \
                                  "lp_dev, lp_ref, lp_meas, lp__of_points, Date) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?," \
                                  "?,?,?,?) "
        cursor.execute(insert_query_with_param, i)
        conn.commit()
    messagebox.showinfo("Message", "Inserted to BB300 table successfully.\n\n".join([str(x) for x in df_list]))


# Insert datas from the merged CSV in BA500 table
def insert_table_BA500(data):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    df = pd.read_csv(data)
    df_list = df.values.tolist()
    print(df_list)
    for i in df_list:
        insert_query_with_param = "INSERT INTO BA500('experiment_ID','Name','01-02_Tol','01-02_Dev','01-02_Ref_Value'," \
                                  "'01-02_Meas_Value','01-02__Of_Points','01-03_Tol','01-03_Dev','01-03_Ref_Value'," \
                                  "'01-03_Meas_Value','01-03__Of_Points','01-04_Tol','01-04_Dev','01-04_Ref_Value'," \
                                  "'01-04_Meas_Value','01-04__Of_Points','01-05_Tol','01-05_Dev','01-05_Ref_Value'," \
                                  "'01-05_Meas_Value','01-05__Of_Points','01-06_Tol','01-06_Dev','01-06_Ref_Value'," \
                                  "'01-06_Meas_Value','01-06__Of_Points','01-07_Tol','01-07_Dev','01-07_Ref_Value'," \
                                  "'01-07_Meas_Value','01-07__Of_Points','01-08_Tol','01-08_Dev','01-08_Ref_Value'," \
                                  "'01-08_Meas_Value','01-08__Of_Points','01-09_Tol','01-09_Dev','01-09_Ref_Value'," \
                                  "'01-09_Meas_Value','01-09__Of_Points','01-10_Tol','01-10_Dev','01-10_Ref_Value'," \
                                  "'01-10_Meas_Value','01-10__Of_Points','01-11_Tol','01-11_Dev','01-11_Ref_Value'," \
                                  "'01-11_Meas_Value','01-11__Of_Points', 'Date') VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?," \
                                  "?,?,?,?,?," \
                                  "?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) "
        cursor.execute(insert_query_with_param, i)
        conn.commit()
        messagebox.showinfo("Message", "Inserted to BA500 table successfully.\n\n".join([str(x) for x in df_list]))
