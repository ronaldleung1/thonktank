from dotenv import load_dotenv
load_dotenv('.env')

import os

import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None;
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def create_ideas_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print("SQL error: ") 
        print(e)

def create_idea(conn, idea):
    """
    Add a new idea into the ideas table
    :param conn:
    :param idea:
    :return: idea id
    """
    sql = """INSERT INTO ideas(name,description)
             VALUES(?,?)"""
    cur = conn.cursor()
    cur.execute(sql, idea)
    conn.commit()
    return cur.lastrowid

def main():
    database = os.environ.get("DB_FILE_PATH")

    sql_create_ideas_table =  """CREATE TABLE IF NOT EXISTS ideas (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    description text
                                );"""
     
    # create a database connection
    conn = create_connection(database) # if os.path.exists(database) else create_connection(r"C:\sqlite\db\pythonsqlite.db")

    # create tables
    if conn is not None:
        # create ideas table
        create_ideas_table(conn, sql_create_ideas_table)
        create_idea(conn, ("Test idea", "This is a test idea"))
        create_idea(conn, ("Test idea 2", "This is another test idea"))
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()