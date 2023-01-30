create table facturas
(
	id integer not null
		constraint facturas_id primary key autoincrement,
	nif text not null,
	matricula text not null,
	fecha text not null,
	emitida integer not null default 0,
	check ( emitida in (0,1) )
);

create table facturas_servicios
(
    factura_id integer not null,
    servicio_id integer not null,
    cantidad integer not null,
    constraint facturas_servicios_pk primary key (factura_id, servicio_id)
);