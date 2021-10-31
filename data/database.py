import sqlite3
from sqlite3 import Error
from .connection import create_connection


class DB_Cinema:
    con = create_connection()
    def __init__(self):
        try:
            self.con = sqlite3.connect('data/sql/cinema.db',check_same_thread=False)
            self.cursor = self.con.cursor()
            print("Database Conneted Successfully")
        except Error:
            print(Error)
    
    def __del__(self):
        self.cursor.close()
        self.con.close()
        print("Closing Database Conneted Successfully")

    def view_all_users(self):
        try:
            self.con.row_factory = sqlite3.Row
            self.cursor = self.con.cursor()
            self.cursor.execute("SELECT * FROM Personas WHERE tipoUsuario == 'cliente' ;")
            rows = self.cursor.fetchall()
            users = [dict(row) for row in rows]
            return users
        except Error:
            print(f"Error getting all users: {Error}")
            return False

    def view_users(self, count):
        query = f"SELECT * FROM Personas LIMIT {count};"
        try:
            self.con.row_factory = sqlite3.Row
            self.cursor = self.con.cursor()
            self.cursor.execute(query)
            rows = self.cursor.fetchmany()
            users = [dict(row) for row in rows]
            return users
        except Error:
            print(f"Error getting {count} users: {Error}")
            return False 

    def view_user(self, userid):
        query = ("SELECT nombre, apellido, email, direccion, fechaNacimiento FROM Personas WHERE id = ? LIMIT 1;")
        try:
            
            self.con.row_factory = sqlite3.Row
            self.cursor = self.con.cursor()
            self.cursor.execute(query, (userid,))
            row = self.cursor.fetchone()
            if row:
                row = dict(row)
                return row
            return False
        except Error:
            print(f"Error getting user: {Error}")
            return False

    def insert_user(self, nombre, apellido, alias, tipoDoc, userid, numeroCelular, email, direccion, dia_nacimiento, mes_nacimiento, ano_nacimiento, ciudad, departamento, contrasena, autorizaciones):
        fechaNacimiento = f"{dia_nacimiento}-{mes_nacimiento}-{ano_nacimiento}"
        check_email, check_phone, check_sms = False, False, False
        if autorizaciones:
            for check in autorizaciones:
                if check == "1":
                    check_email = True
                elif check == "2":
                    check_phone = True
                else:
                    check_sms = True
        tipoUsuario = "cliente"
        query = ("INSERT INTO Personas (nombre, apellido, alias, tipoDoc, id, numeroCelular, email, direccion, fechaNacimiento, ciudad, departamento, tipoUsuario, contrasena, check_email, check_phone, check_sms) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);")
        values = [nombre, apellido, alias, tipoDoc, userid, numeroCelular, email, direccion, fechaNacimiento, ciudad, departamento, tipoUsuario, contrasena, check_email, check_phone, check_sms]
        try:
            self.cursor.execute(query, values)
            self.con.commit()
            print("New user added to database")
            return self.cursor.lastrowid
        except Error:
            print(f"Error inserting user: {Error}")
            return False
            

    def update_user(self, userid, nombre, apellido, email, direccion, fechaNacimiento):
        query = ("UPDATE Personas (nombre, apellido, email, direccion, fechaNacimiento) SET VALUES (?, ?, ?, ?, ?) WHERE id = ?;")
        values = [nombre, apellido,email, direccion, fechaNacimiento,  userid]
        try:
            self.cursor.execute(query, values)
            self.con.commit()
            print("User was update to database")
            return True
        except Error:
            print(f"Error updating user: {Error}")
            return False
	
    def delete_user(self, userid):
        query = ("SELECT correo, contrasena FROM Personas WHERE correo = ?")
        try:
            self.cursor.execute(query, [userid])
            self.con.commit()
            print("User was delete to database")
        except Error:
            print(f"User was deleted to database: {Error}")


    def login(self, correo, contrasena):
        query = ("SELECT tipoUsuario, alias FROM Personas WHERE (email = ? AND contrasena = ?);")
        values = [correo, contrasena]
        try:
            self.con.row_factory = sqlite3.Row
            self.cursor = self.con.cursor()
            self.cursor.execute(query, values)
            row = self.cursor.fetchone()
            if row:
                row = dict(row)
                return row
            return {}
        except Error:
            print(f"Error login: {Error}")
            return False
	    
    # def view_comments(self, count):
    #     query = ("SELECT TOP ? FROM Personas")
    #     self.cursor.execute(query, count)
    #     row = self.cursor.fetchall()
    #     return row

    # def view_comment(self, userid):
    #     query = ("SELECT ? FROM Personas")
    #     self.cursor.execute(query, userid)
    #     row = self.cursor.fetchall()
    #     return row

    # def insert_comment(self, userid, nombre, apellido, alias, cedula, numeroCelular, email, direccion, tipoUsuario, contrasena):
    #     query = ("INSERT INTO Personas (id, nombre, apellido, alias, cedula, numeroCelular, email, direccion, tipoUsuario, contrasena) VALUE (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
    #     values = [userid, nombre, apellido, alias, cedula, numeroCelular, email, direccion, tipoUsuario, contrasena]
    #     self.cursor.execute(query, values)
    #     self.con.commit()
    #     print("New user added to database")

    # def update_comment(self, userid, nombre, apellido, alias, cedula, numeroCelular, email, direccion, tipoUsuario, contrasena):
    #     query = "UPDATE Personas (id, nombre, apellido, alias, cedula, numeroCelular, email, direccion, tipoUsuario, contrasena) SET VALUE (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    #     values = [userid, nombre, apellido, alias, cedula, numeroCelular, email, direccion, tipoUsuario, contrasena]
    #     self.cursor.execute(query, values)
    #     self.con.commit()
    #     print("User was update to database")
	
    # def delete_comment(self, userid):
    #     query = "DELETE FROM Personas WHERE id = ?"
    #     self.cursor.execute(query, [userid])
    #     self.con.commit()
    #     print("User was delete to database")
