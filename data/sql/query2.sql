CREATE TABLE IF NOT EXISTS Comentarios (
    id INTEGER NOT NULL PRIMARY KEY,
    fechaComentario VARCHAR(255),
    tamanoComentario VARCHAR(255),
    id_Personas INTEGER,
    FOREIGN KEY (id_Personas) REFERENCES Personas(id)
);