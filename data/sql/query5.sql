CREATE TABLE IF NOT EXISTS Funciones (
    id INTEGER NOT NULL PRIMARY KEY,
    fechaFinalDisponible VARCHAR(255),
    fechaConsulta VARCHAR(255),
    salaFuncion VARCHAR(255),
    cuposTotales VARCHAR(255),
    horarioFuncion VARCHAR(255),
    precioFuncion VARCHAR(255),
    id_Cartelera INTEGER,
    id_Personas INTEGER,
    FOREIGN KEY (id_Cartelera) REFERENCES Cartelera(id),
    FOREIGN KEY (id_Personas) REFERENCES Personas(id)
);