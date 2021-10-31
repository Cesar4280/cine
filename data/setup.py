import os


import os
rootDir = "."
import sqlite3
from sqlite3 import Error
from .connection import create_connection

def read_file(path):
    with open(path, "r") as sql_file:
        return sql_file.read()

def create_tables():
    con = create_connection()
    # for dirName, subdirList, fileList in os.walk(rootDir):
    # print('Directorio encontrado: %s' % dirName)
    # for fname in fileList:
    #     print('\t%s' % fname)
        
    path = "data/sql/query1.sql"
    sql = read_file(path)
    
    try:
        cursor = con.cursor()
        cursor.execute(sql)
        con.commit()
        return True

    except Error:
        print(f"Error at create tables: {Error}")
        return False

    finally:
        if con:
            cursor.close()
            con.close()
