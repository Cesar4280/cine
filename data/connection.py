import sqlite3
from sqlite3 import Error

def create_connection():
    con = None

    try:
        con = sqlite3.connect('data/sql/cinema.db',check_same_thread=False)
    
    except Error:
        print(f"Error connecting to database: {Error}")

    return con