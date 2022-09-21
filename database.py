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
path_database = 'db.db'
application_title = 'S3D Accuracy Test Database Management'


# Open the database.
def open_db():
    check_process_running = "DB Browser for SQLite.exe" in (p.name() for p in psutil.process_iter())
    if check_process_running is False:
        try:
            os.startfile(path_database)
            print('Database: Successfully opened!')
        except subprocess.SubprocessError as e:
            print('Database: Failed to open database!', e)
            messagebox.showerror(main.application_title, "Database: Failed to open database!")
    elif check_process_running is True:
        messagebox.showerror(main.application_title, "Tool is already running.")

def get_ids(department, operator, experience_type, artefact_type, certificate_no):
    conn = sqlite3.connect(path_database)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    department_id = c.execute('SELECT department_id FROM departments WHERE department = ?', (department,)).fetchone()
    operator_id = c.execute('SELECT operator_id FROM operators WHERE operator = ?', (operator,)).fetchone()
    experience_type_id = c.execute('SELECT experience_type_id FROM experience_types WHERE experience_type = ?',
                                   (experience_type,)).fetchone()
    artefact_type_id = c.execute('SELECT artefact_type_id FROM artefact_types WHERE artefact_type = ?',
                                 (artefact_type,)).fetchone()
    certificate_no_id = c.execute('SELECT certificate_no_id FROM certificate_nos WHERE certificate_no = ?',
                                  (certificate_no,)).fetchone()
    data = [department_id, operator_id, experience_type_id, artefact_type_id, certificate_no_id]
    return data


# Insert the experience to the database.
def insert_experience(device_sn, operator, department, experience_type, artefact_type, certificate_no, subject,
                      experience_id):
    try:
        conn = sqlite3.connect(path_database)
        cursor = conn.cursor()
        insert_query_with_param = '''INSERT INTO experiences ("experience_id","device_sn","department_id", "operator_id",
            "experience_type_id","artefact_type_id","certificate_number_id","subject") VALUES (?, ?, ?, ? ,?, ?, ?, ?)'''
        department_id, operator_id, experience_type_id, artefact_type_id, certificate_no_id = get_ids(department,
                                                                                                      operator,
                                                                                                      experience_type,
                                                                                                      artefact_type,
                                                                                                      certificate_no)
        data = (
            experience_id, device_sn, department_id, operator_id, experience_type_id, artefact_type_id,
            certificate_no_id,
            subject)
        cursor.execute(insert_query_with_param, data)
        conn.commit()
        print('Insert Experience: Successfully inserted to database!')
    except:
        print('Insert Experience: Failed to insert to database!')
        messagebox.showerror(application_title,'Insert Experience: Failed to insert to database!')


# Get the operators from database to list them in the first page.
def get_operators(department):
    conn = sqlite3.connect(path_database)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    department_id = c.execute('SELECT department_id FROM departments WHERE department = ?', (department,)).fetchone()
    data = c.execute('SELECT operator FROM operators WHERE department_id = ?', (department_id,)).fetchall()
    data = list(dict.fromkeys(data))
    return data


# Get the departments from database to list them in the first page.
def get_departments():
    conn = sqlite3.connect(path_database)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    data = c.execute('SELECT department FROM departments').fetchall()
    data = list(dict.fromkeys(data))
    return data


# Get the experience types from database to list them in the first page.
def get_experience_types():
    conn = sqlite3.connect(path_database)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    data = c.execute('SELECT experience_type FROM experience_types').fetchall()
    data = list(dict.fromkeys(data))
    return data


# Get the artefact SNs from database to list them in the first page.
def get_artefact_types(experience_type):
    conn = sqlite3.connect(path_database)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    experience_type_id = c.execute('SELECT experience_type_id FROM experience_types WHERE experience_type = ?',
                                   (experience_type,)).fetchone()
    data = c.execute('SELECT artefact_type FROM artefact_types WHERE experience_type_id = ?',
                     (experience_type_id,)).fetchall()
    data = list(dict.fromkeys(data))
    return data


def get_certificate_nos(artefact_type):
    conn = sqlite3.connect(path_database)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    artefact_type_id = c.execute('SELECT artefact_type_id FROM artefact_types WHERE artefact_type = ?',
                                 (artefact_type,)).fetchone()
    data = c.execute('SELECT certificate_no FROM certificate_nos WHERE artefact_type_id = ?',
                     (artefact_type_id,)).fetchall()
    return data


# Get the experience IDs from database to list them in the first page.xxx
def get_experience_id(device_sn):
    conn = sqlite3.connect(path_database)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    data = c.execute('SELECT experience_id FROM experiences WHERE device_sn = ?', (device_sn,)).fetchall()
    if len(data) == 0:
        return 'no experience'
    else:
        return data[-1]


def get_experience_ids():
    conn = sqlite3.connect(path_database)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    data = c.execute('SELECT experience_id FROM experiences ORDER BY experience_id DESC').fetchall()
    return data


# Check if the new experience has been added successfully
def check_experience_id(experience_id):
    conn = sqlite3.connect(path_database)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    data = c.execute('SELECT experience_id FROM experiences').fetchall()
    if experience_id in data:
        return 'exist'


# Get the values by filtering with experience ID
def get_attributes_from_experience_id(experience_id):
    try:
        conn = sqlite3.connect(path_database)
        c = conn.cursor()
        device_sn = c.execute('SELECT device_sn FROM experiences WHERE experience_id = ?', (experience_id,)).fetchone()[
            0]
        department_id = \
            c.execute('SELECT department_id FROM experiences WHERE experience_id = ?', (experience_id,)).fetchone()[0]
        operator_id = \
            c.execute('SELECT operator_id FROM experiences WHERE experience_id = ?', (experience_id,)).fetchone()[
                0]
        experience_type_id = \
            c.execute('SELECT experience_type_id FROM experiences WHERE experience_id = ?',
                      (experience_id,)).fetchone()[0]
        artefact_type_id = \
            c.execute('SELECT artefact_type_id FROM experiences WHERE experience_id = ?', (experience_id,)).fetchone()[
                0]
        certificate_no_id = \
            c.execute('SELECT certificate_number_id FROM experiences WHERE experience_id = ?',
                      (experience_id,)).fetchone()[
                0]

        department = \
            next(c.execute('SELECT department FROM departments WHERE department_id = ?', (department_id,)), [None])[0]
        operator = next(c.execute('SELECT operator FROM operators WHERE operator_id = ?', (operator_id,)), [None])[0]
        experience_type = \
            next(c.execute('SELECT experience_type FROM experience_types WHERE experience_type_id = ?',
                           (experience_type_id,)),
                 [None])[0]
        artefact_type = \
            next(c.execute('SELECT artefact_type FROM artefact_types WHERE artefact_type_id = ?', (artefact_type_id,)),
                 [None])[
                0]
        certificate_no = \
            next(c.execute('SELECT certificate_no FROM certificate_nos WHERE certificate_no_id = ?',
                           (certificate_no_id,)),
                 [None])[0]

        data = [experience_id, device_sn, department, operator, experience_type, artefact_type, certificate_no]
        return data
    except:
        print('error')


# Select the table where the merged CSV will be inserted
def select_table_to_insert(path_csv_file, experience_id):
    try:
        conn = sqlite3.connect(path_database)
        c = conn.cursor()
        df = pd.read_csv(path_csv_file)
        print(df)
        df_col_list = []
        for col in df.columns:
            df_col_list.append(col)
        column_string = ''
        print('df col list::', df_col_list)
        for col in df_col_list:
            column_string = column_string + '''"''' + col + '''"''' + ' TEXT, '
        column_string = column_string[:-2]
        print('colstr:', column_string)
        experience_type_id = c.execute('SELECT experience_type_id FROM experiences WHERE experience_id = ?',
                                       (experience_id,)).fetchone()
        print(experience_type_id)
        experience_type = c.execute('SELECT experience_type FROM experience_types WHERE experience_type_id = ?',
                                    (experience_type_id[0],)).fetchone()
        print(experience_type)
        experience_type = experience_type[0]
        if experience_type == 'BB300':
            print('testp1')
            c.execute('CREATE TABLE IF NOT EXISTS csv_bb300 (' + column_string + ')')
            print('testp2')
            insert_data_to_table_BB300(path_csv_file)
        elif experience_type == 'BB500':
            c.execute('CREATE TABLE IF NOT EXISTS csv_bb500 (' + column_string + ')')
            insert_data_to_table_BB500(path_csv_file)
        elif experience_type == 'BA500':
            c.execute('CREATE TABLE IF NOT EXISTS csv_ba500 (' + column_string + ')')
            insert_data_to_table_BA500(path_csv_file)
        else:
            print('Store CSV: Failed! Experience type not found!')
            messagebox.showwarning(application_title, 'Store CSV: Failed! Experience type not found!')
    except sqlite3.Error:
        print('Store CSV: Failed to send data to database!')
        messagebox.showwarning(application_title, "Store CSV: Failed to send data to database!\n\n"
                                                  "Please check if the Experience ID is correct.")


# Insert datas from the merged CSV in BB300 table
def insert_data_to_table_BB300(path_csv_file):
    try:
        conn = sqlite3.connect(path_database)
        c = conn.cursor()
        df = pd.read_csv(path_csv_file)
        df_col_list = []
        for col in df.columns:
            df_col_list.append(col)
        column_string = ''
        for col in df_col_list:
            column_string = column_string + '''"''' + col + '''"''' + ', '
        column_string = column_string[:-2]
        values_string = '?,' * len(df_col_list)
        values_string = values_string[:-1]
        df_list = df.values.tolist()
        for i in df_list:
            c.execute("INSERT INTO csv_bb300(" + column_string + ") VALUES (" + values_string + ")", i)
            conn.commit()
        print("Insert Data: Successfully inserted to BB300 table!\n\n")
        messagebox.showinfo(application_title, "Insert Data: Successfully inserted to BB300 table!\n\n")
    except:
        print("Insert Data: Failed to insert to BB300 table!")
        messagebox.showerror(application_title, "Insert Data: Failed to insert to BB300 table!\n\n")


# Insert datas from the merged CSV in BB500 table
def insert_data_to_table_BB500(path_csv_file):
    try:
        conn = sqlite3.connect(path_database)
        c = conn.cursor()
        df = pd.read_csv(path_csv_file)
        df_col_list = []
        for col in df.columns:
            df_col_list.append(col)
        column_string = ''
        for col in df_col_list:
            column_string = column_string + '''"''' + col + '''"''' + ', '
        column_string = column_string[:-2]
        values_string = '?,' * len(df_col_list)[:-1]
        df_list = df.values.tolist()
        for i in df_list:
            c.execute("INSERT INTO csv_bb500(" + column_string + ") VALUES (" + values_string + ")", i)
            conn.commit()
        print("Insert Data: Successfully inserted to BB500 table!\n\n")
        messagebox.showinfo(application_title, "Inserted to BB500 table successfully.\n\n")
    except:
        print("Insert Data: Failed to insert to BB500 table!")
        messagebox.showerror(application_title, "Insert Data: Failed to insert to BB500 table!\n\n")


# Insert datas from the merged CSV in BA500 table
def insert_data_to_table_BA500(path_csv_file):
    try:
        conn = sqlite3.connect(path_database)
        c = conn.cursor()
        df = pd.read_csv(path_csv_file)
        df_col_list = []
        for col in df.columns:
            df_col_list.append(col)
        column_string = ''
        for col in df_col_list:
            column_string = column_string + '''"''' + col + '''"''' + ', '
        column_string = column_string[:-2]
        values_string = '?,' * len(df_col_list)[:-1]
        df_list = df.values.tolist()
        for i in df_list:
            c.execute("INSERT INTO csv_bb500(" + column_string + ") VALUES (" + values_string + ")", i)
            conn.commit()
        print("Insert Data: Successfully inserted to BA500 table!\n\n")
        messagebox.showinfo(application_title, "Insert Data: Failed to insert to BA500 table!\n\n")
    except:
        print("Insert Data: Failed to insert to BA500 table!")
        messagebox.showerror(application_title, "Insert Data: Failed to insert to BB500 table!\n\n")


# Insert the experience to the database.
def insert_content(content, experience_id):
    try:
        if content != '\n' and experience_id != '':
            conn = sqlite3.connect(path_database)
            cursor = conn.cursor()
            insert_query_with_param = """UPDATE experiences SET content = ? WHERE experience_id = ?"""
            data = (content, experience_id)
            cursor.execute(insert_query_with_param, data)
            conn.commit()
            messagebox.showinfo(main.application_title, "Insert Content: Success to insert content to the experience!\n\n\t"
                                "%s\n%s" % (experience_id, content))
        elif content == "\n" and experience_id == '':
            messagebox.showerror(main.application_title, "Insert Content: Failed to insert content to the experience!"
                                                         "\n\nContent is empty and experience ID has not been found.")
        elif experience_id == '' and content != '\n':
            messagebox.showerror(main.application_title, "Insert Content: Failed to insert content to the experience!"
                                                         "\n\nExperience ID has not been found.")
        elif content == "\n" and experience_id != '':
            messagebox.showerror(main.application_title, "Insert Content: Failed to insert content to the experience!"
                                                         "\n\nContent is empty.")
    except:
        print('Insert Content: Failed to insert content to the experience!')
        messagebox.showerror(main.application_title, "Insert Content: Failed to insert content to the experience!")
