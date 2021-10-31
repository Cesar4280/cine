CREATE TABLE IF NOT EXISTS Tiquetes (
    id INTEGER NOT NULL PRIMARY KEY,
    precioTiquete VARCHAR(255),
    cuposOcupados VARCHAR(255),
    id_Funciones INTEGER,
    id_Personas INTEGER,
    FOREIGN KEY (id_Funciones) REFERENCES Funciones(id),
    FOREIGN KEY (id_Personas) REFERENCES Personas(id)
);