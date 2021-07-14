from dotenv import load_dotenv
load_dotenv('.env')

import os, sys

from tabulate import tabulate

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
        print(e)

def create_idea(conn, idea):
    """
    Add a new idea into the ideas table
    :param conn:
    :param idea:
    :return: idea id
    """
    sql = """INSERT INTO ideas(name, description, tags)
             VALUES(?,?,?)"""
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

    print(tabulate(rows, headers=["#", "Name", "Description", "Tags"], tablefmt="fancy_grid"))

def update_idea(conn, idea):
    """
    Update idea with matching id in table
    :param conn: the Connection object
    :return: idea
    """
    sql =  """UPDATE ideas
              SET name = ? ,
                  description = ? ,
                  tags = ?
              WHERE id = ?"""
    cur = conn.cursor()
    cur.execute(sql, idea)
    conn.commit()

def delete_idea(conn, id):
    """
    Delete an idea by id
    :param conn:  Connection to the SQLite database
    :param id: id of the idea
    :return:
    """
    sql = "DELETE FROM ideas WHERE id=?"
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

conn = None

def main():
    os.system("clear")

    database = os.environ.get("DB_FILE_PATH")

    sql_create_ideas_table =  """CREATE TABLE IF NOT EXISTS ideas (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    name text NOT NULL,
                                    description text,
                                    tags text
                                );"""
     
    # create a database connection
    global conn
    conn = create_connection(database) # if os.path.exists(database) else create_connection(r"C:\sqlite\db\pythonsqlite.db")

    if conn is not None:

        # create ideas table
        create_ideas_table(conn, sql_create_ideas_table)
        
        while(True):
            print("Thonktank")
            select_ideas_table(conn)
            option = input("\n(1) Create new idea (2) Edit idea (3) Delete idea (4) Exit\n")
            if(option == "1"):
                # Create new idea
                name = str(input("Name: "))
                description = str(input("Description: "))
                tags = str(input("Tags (separate with spaces): ")).lower()
                create_idea(conn, (name, description, tags))
            elif(option == "2"):
                # Edit idea
                id = int(input("Select ID of idea to be edited: "))
                name = str(input("Name: "))
                description = str(input("Description: "))
                tags = str(input("Tags (separate with spaces): ")).lower()
                update_idea(conn, (name, description, tags, id))
            elif(option == "3"):
                # Delete idea
                id = int(input("Select ID of idea to be deleted: "))
                delete_idea(conn, id)
            elif(option == "4"):
                sys.exit(0)
            else:
                input("Not a valid command (enter to continue)")
            os.system("clear")
    else:
        sys.exit("Cannot create the database connection")

if __name__ == '__main__':
    main()