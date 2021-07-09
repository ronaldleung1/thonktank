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
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    print(os.environ.get("DB_FILE"))
    create_connection(os.environ.get("DB_FILE")) # r"C:\sqlite\db\pythonsqlite.db"