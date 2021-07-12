from dotenv import load_dotenv
load_dotenv('.env')

import os, sys

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

def select_ideas_table(conn):
    """
    Query all rows in the ideas table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM ideas")

    rows = cur.fetchall()

    for row in rows:
        print(row)

def main():
    os.system("clear")

    database = os.environ.get("DB_FILE_PATH")

    sql_create_ideas_table =  """CREATE TABLE IF NOT EXISTS ideas (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    name text NOT NULL,
                                    description text
                                );"""
     
    # create a database connection
    conn = create_connection(database) # if os.path.exists(database) else create_connection(r"C:\sqlite\db\pythonsqlite.db")

    if conn is not None:

        # create ideas table
        create_ideas_table(conn, sql_create_ideas_table)
        
        while(True):
            print("Thonktank (Ctrl+C to exit)")
            select_ideas_table(conn)
            option = input("\n(1) Create new idea (2) Edit idea (3) Delete idea (4) Exit\n")
            if(option == "1"):
                name = str(input("Name: "))
                description = str(input("Description: "))
                create_idea(conn, (name, description))
            elif(option == "2"):
                print("Feature to be implemented")
            elif(option == "3"):
                print("Feature to be implemented")
            elif(option == "3"):
                sys.exit(0)
            else:
                print("Not a valid command")
            os.system("clear")
    else:
        sys.exit("Cannot create the database connection")

if __name__ == '__main__':
    main()