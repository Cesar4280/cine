CREATE TABLE IF NOT EXISTS Cartelera (
    id INTEGER NOT NULL PRIMARY KEY,
    nombrePelicula VARCHAR(255),
    descripcion VARCHAR(255),
    idioma VARCHAR(255),
    clasificacion VARCHAR(255),
    genero VARCHAR(255),
    duracionPelicula VARCHAR(255),
    trailer VARCHAR(255),
    portada VARCHAR(255),
    id_Comentarios INTEGER,
    id_Calificacion INTEGER,
    FOREIGN KEY (id_Comentarios) REFERENCES Comentarios(id),
    FOREIGN KEY (id_Calificacion) REFERENCES Calificacion(id)
);