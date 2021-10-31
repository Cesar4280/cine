CREATE TABLE IF NOT EXISTS Calificaciones (
    id INTEGER NOT NULL PRIMARY KEY,
    calificacion VARCHAR(255),
    id_Personas INTEGER,
    FOREIGN KEY (id_Personas) REFERENCES Personas(id)
);