create table servicios
(
    id                integer not null
        constraint servicios_pk
            primary key autoincrement,
    nombre            TEXT    not null,
    precioUnitario    REAL    not null,
    fechaAlta         TEXT    not null,
    fechaModificacion TEXT    not null,
    fechaBaja         TEXT
);
