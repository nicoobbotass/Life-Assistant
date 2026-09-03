create table entrenamientos (
  id bigint generated always as identity primary key,
  fecha date not null,
  tipo text,
  created_at timestamptz default now()
);

create table objetivos_actividad (
  id bigint generated always as identity primary key,
  entrenamientos_semana int not null default 4,
  pasos_diarios int not null default 8000,
  updated_at timestamptz default now()
);
