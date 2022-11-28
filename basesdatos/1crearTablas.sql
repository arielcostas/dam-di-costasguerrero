CREATE TABLE provincias
(
	id        INTEGER,
	provincia TEXT
);

CREATE TABLE municipios
(
	provincia_id INTEGER,
	municipio    TEXT,
	id           INTEGER
);

CREATE TABLE clientes
(
	dni                     TEXT NOT NULL UNIQUE,
	nombre                  TEXT NOT NULL,
	alta                    TEXT NOT NULL,
	direccion               TEXT,
	provincia               TEXT,
	municipio               TEXT,
	permitido_efectivo      INT  NOT NULL,
	permitido_factura       INT  NOT NULL,
	permitido_transferencia INT  NOT NULL,
	PRIMARY KEY (dni),
	CHECK ( permitido_efectivo IN (0, 1) ),
	CHECK ( permitido_factura IN (0, 1) ),
	CHECK ( permitido_transferencia IN (0, 1) )
);

CREATE TABLE coches
(
	matricula TEXT NOT NULL UNIQUE,
	dnicli    TEXT NOT NULL,
	marca     TEXT NOT NULL,
	modelo    TEXT NOT NULL,
	motor     TEXT NOT NULL,
	PRIMARY KEY (matricula),
	FOREIGN KEY (dnicli) REFERENCES clientes (dni)
);

ALTER TABLE clientes ADD COLUMN fecha_baja TEXT DEFAULT NULL;
ALTER TABLE coches ADD COLUMN fecha_baja TEXT DEFAULT NULL;