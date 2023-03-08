alter table servicios
    add stock INTEGER default 0 not null;

alter table servicios
    add almacenable INT default 1;