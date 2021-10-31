-- SQLite
CREATE TABLE IF NOT EXISTS Personas (
    nombre VARCHAR(255),
    apellido VARCHAR(255),
    alias VARCHAR(255),
    tipoDoc VARCHAR(255),
    id INTEGER NOT NULL PRIMARY KEY,
    numeroCelular VARCHAR(255),
    email VARCHAR(255),
    direccion VARCHAR(255),
    fechaNacimiento VARCHAR(255),
    ciudad VARCHAR(255),
    departamento VARCHAR(255),
    tipoUsuario VARCHAR(255),
    contrasena VARCHAR(255),
    check_email BOOLEAN(255), 
    check_phone BOOLEAN(255), 
    check_sms BOOLEAN(255)
);