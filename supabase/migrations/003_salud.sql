create table salud_diaria (
  fecha date primary key,
  pasos int not null default 0,
  calorias_activas numeric not null default 0,
  frecuencia_cardiaca_media numeric
);
