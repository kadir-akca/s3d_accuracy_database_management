# Methods that are used for inserting or getting data in/from database.

# Libraries
import logging
import os
import sqlite3
import subprocess
import pandas as pd

# URL of the database. Needs to be checked always when we change the PC, since we are local.
db_url = 'C:/Users/shining3d/Desktop/s3d_db_management/db.db'


# Open the database.
def open_db():
    try:
        os.startfile(db_url)
        logging.info(f'Following database has been opened: {db_url}')
    except subprocess.SubprocessError as e:
        print('Failed to open database', e)
        logging.error(f'Following database could not be opened: {db_url}')


# Insert the experience to the database.
def insert_experience(dev, op, dep, etype, artsn, certsn, sub, eid):
    try:
        if dev != '':
            conn = sqlite3.connect(db_url)
            cursor = conn.cursor()
            insert_query_with_param = """INSERT INTO experience("device_sn", "operator","department","experience_type","artefact_sn","certificate_sn", subject, experience_id) VALUES (?, ?, ?, ? ,?, ?, ?, ?)"""
            data = (dev, op, dep, etype, artsn, certsn, sub, eid)
            cursor.execute(insert_query_with_param, data)
            conn.commit()
            global x
            x = eid
            return cursor
        else:
            pass
    except sqlite3.Error as e:
        logging.error('Experience has not been added to database')
        print('Failed to insert accuracy test in database', e)


# Insert the experience to the database.
def insert_content(content, experience_id):
    print(content, experience_id)
    try:
        if content != '':
            conn = sqlite3.connect(db_url)
            cursor = conn.cursor()
            insert_query_with_param = """UPDATE experience SET content = ? WHERE experience_id = ?"""
            data = (content, experience_id)
            cursor.execute(insert_query_with_param, data)
            conn.commit()

            return cursor
        else:
            pass
    except sqlite3.Error as e:
        logging.error('Experience has not been added to database')
        print('Failed to insert accuracy test in database', e)


# Insert operator in database.
def insert_operator(us, d):
    try:
        conn = sqlite3.connect(db_url)
        c = conn.cursor()
        insert_query_with_param = """INSERT INTO operator(name, "add_date") VALUES (?, ?)"""
        data = (us, d)
        if us != '' and us not in get_operators():
            c.execute(insert_query_with_param, data)
            conn.commit()
            logging.info(f'Operator {us} has been added.')
        elif us in get_operators():
            print('Operator exists already')
            logging.warning(f'Operator {us} already exists.')
        else:
            print('No value to add')
            logging.warning('No operator to add.')
    except sqlite3.Error as e:
        print('Failed to insert user in database', e)
        logging.error('Failed to add operator.')


# Check number of operators in order to see if a new operator is added or not.
def check_operator_number():
    conn = sqlite3.connect(db_url)
    cursor = conn.cursor()
    cursor.execute("select * from operator")
    results = cursor.fetchall()
    return len(results)


# Get the operators from database to list them in the first page.
def get_operators():
    conn = sqlite3.connect(db_url)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    data = c.execute('SELECT name FROM operator').fetchall()
    return data


# Get the departments from database to list them in the first page.
def get_departments():
    conn = sqlite3.connect(db_url)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    data = c.execute('SELECT name FROM department').fetchall()
    return data


# Get the experience types from database to list them in the first page.
def get_experience_type():
    conn = sqlite3.connect(db_url)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    data = c.execute('SELECT experience_type FROM experience_type').fetchall()
    data = list(dict.fromkeys(data))
    return data


# Get the artefact SNs from database to list them in the first page.
def get_artefact_sn(etype):
    conn = sqlite3.connect(db_url)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    data = c.execute('SELECT artefact_sn FROM experience_type WHERE experience_type = ?', (etype,)).fetchall()
    data = list(dict.fromkeys(data))
    return data


def get_cert_sn(id):
    conn = sqlite3.connect(db_url)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    data = c.execute('SELECT cert_sn FROM experience_type WHERE artefact_sn = ?', (id,)).fetchall()

    return data


# Get the experience IDs from database to list them in the first page.
def get_experience_id(dsn):
    conn = sqlite3.connect(db_url)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    data = c.execute('SELECT experience_id FROM experience WHERE device_sn = ?', (dsn,)).fetchall()
    if len(data) == 0:
        print('Previous experience not found for the following serial number: ', dsn)
        return 'no experience'
    else:
        print('Previous experience has been found for the following serial number: ', dsn,
              "\n\t Previous experience is: ", data[-1])
        return data[-1]


# Check if the new experience has been added succesfully
def check_experience_id(expid):
    conn = sqlite3.connect(db_url)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    data = c.execute('SELECT experience_id FROM experience').fetchall()
    if expid in data:
        return 'exist'


# Get the values by filtering with experience ID
def get_attributes_from_experience_id(expid):
    conn = sqlite3.connect(db_url)
    c = conn.cursor()
    c.execute('SELECT * FROM experience WHERE experience_id = ?', (expid,))
    data = c.fetchone()
    print('data', data)
    return data


# Create new table for BB300 artefact
def create_table_BB300(url):
    df = pd.read_csv(url)
    col = []
    for c in df.columns:
        col.append(c)
    coldb = ' TEXT, '.join(col)
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    # table = 'CREATE TABLE IF NOT EXISTS BB300 (' + coldb + ' TEXT)'
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS BB300(exp_ID,Name,dp0_tol,dp0_dev,dp0_ref,dp0_meas,dp0__of_points,dp1_tol,
        dp1_dev,dp1_ref,dp1_meas,dp1__of_points,lp_tol,lp_dev,lp_ref,lp_meas,lp__of_points)''')
    conn.commit()


# Create new table for BB300 artefact
def create_table_BA500():
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS BA500(experiment_ID,Name,'01-02_Tol','01-02_Dev','01-02_Ref_Value',
        '01-02_Meas_Value','01-02__Of_Points','01-03_Tol','01-03_Dev','01-03_Ref_Value','01-03_Meas_Value',
        '01-03__Of_Points','01-04_Tol','01-04_Dev','01-04_Ref_Value','01-04_Meas_Value','01-04__Of_Points',
        '01-05_Tol','01-05_Dev','01-05_Ref_Value','01-05_Meas_Value','01-05__Of_Points','01-06_Tol','01-06_Dev',
        '01-06_Ref_Value','01-06_Meas_Value','01-06__Of_Points','01-07_Tol','01-07_Dev','01-07_Ref_Value',
        '01-07_Meas_Value','01-07__Of_Points','01-08_Tol','01-08_Dev','01-08_Ref_Value','01-08_Meas_Value',
        '01-08__Of_Points','01-09_Tol','01-09_Dev','01-09_Ref_Value','01-09_Meas_Value','01-09__Of_Points',
        '01-10_Tol','01-10_Dev','01-10_Ref_Value','01-10_Meas_Value','01-10__Of_Points','01-11_Tol','01-11_Dev',
        '01-11_Ref_Value','01-11_Meas_Value','01-11__Of_Points')''')
    conn.commit()


# Select the table where the merged CSV will be inserted
def insert_table_select(url):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    df = pd.read_csv(url)
    df_list = df.values.tolist()
    cursor.execute('SELECT experience_type FROM experience WHERE experience_id = ?', (df_list[0][0],))
    artsn = cursor.fetchone()
    artsn = artsn[0]
    if artsn == 'Ball-bar 300':
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS BB300('Date',exp_ID, Name, dp0_tol, dp0_dev, dp0_ref, dp0_meas, 
                dp0__of_points, dp1_tol, dp1_dev, dp1_ref, dp1_meas, dp1__of_points, lp_tol, lp_dev, lp_ref, lp_meas, 
                lp__of_points)''')
        insert_table_BB300(url)
        print('inserted to BB300')
    elif artsn == 'Ball-bar 500':
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS BB300('Date',exp_ID, Name, dp0_tol, dp0_dev, dp0_ref, dp0_meas, 
                dp0__of_points, dp1_tol, dp1_dev, dp1_ref, dp1_meas, dp1__of_points, lp_tol, lp_dev, lp_ref, lp_meas, 
                lp__of_points)''')
        insert_table_BB500(url)
        print('inserted to BB500')
    elif artsn == 'BallArray500':
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS BA500('Date', experiment_ID,Name,'01-02_Tol','01-02_Dev','01-02_Ref_Value',
                '01-02_Meas_Value','01-02__Of_Points','01-03_Tol','01-03_Dev','01-03_Ref_Value','01-03_Meas_Value',
                '01-03__Of_Points','01-04_Tol','01-04_Dev','01-04_Ref_Value','01-04_Meas_Value','01-04__Of_Points',
                '01-05_Tol','01-05_Dev','01-05_Ref_Value','01-05_Meas_Value','01-05__Of_Points','01-06_Tol','01-06_Dev',
                '01-06_Ref_Value','01-06_Meas_Value','01-06__Of_Points','01-07_Tol','01-07_Dev','01-07_Ref_Value',
                '01-07_Meas_Value','01-07__Of_Points','01-08_Tol','01-08_Dev','01-08_Ref_Value','01-08_Meas_Value',
                '01-08__Of_Points','01-09_Tol','01-09_Dev','01-09_Ref_Value','01-09_Meas_Value','01-09__Of_Points',
                '01-10_Tol','01-10_Dev','01-10_Ref_Value','01-10_Meas_Value','01-10__Of_Points','01-11_Tol','01-11_Dev',
                '01-11_Ref_Value','01-11_Meas_Value','01-11__Of_Points')''')
        insert_table_BA500(url)
        print('inserted to BA500')
    else:
        print('exp type not found')


# Insert datas from the merged CSV in BB300 table
def insert_table_BB500(data):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    df = pd.read_csv(data)
    df_list = df.values.tolist()
    for i in df_list:
        insert_query_with_param = "INSERT INTO BB500(exp_ID, Name, dp0_tol, dp0_dev, dp0_ref, dp0_meas, " \
                                  "dp0__of_points, dp1_tol, dp1_dev, dp1_ref, dp1_meas, dp1__of_points, lp_tol, " \
                                  "lp_dev, lp_ref, lp_meas, lp__of_points, Date) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) "
        cursor.execute(insert_query_with_param, i)
        conn.commit()


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
                                  "'01-11_Meas_Value','01-11__Of_Points', 'Date') VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?," \
                                  "?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) "
        cursor.execute(insert_query_with_param, i)
        conn.commit()
