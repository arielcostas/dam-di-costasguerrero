CREATE TABLE clientes (
    dni TEXT NOT NULL UNIQUE,
    nombre TEXT NOT NULL,
    alta TEXT NOT NULL,
    direccion TEXT,
    provincia TEXT,
    municipio TEXT,
    PRIMARY KEY (dni)
);

CREATE TABLE coches(
    matricula TEXT NOT NULL UNIQUE,
    dnicli TEXT NOT NULL,
    marca TEXT NOT NULL,
    modelo TEXT NOT NULL,
    motor TEXT NOT NULL,
    PRIMARY KEY (matricula),
    FOREIGN KEY (dnicli) REFERENCES clientes(dni)
);