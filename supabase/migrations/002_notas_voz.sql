create table notas_voz (
  id bigint generated always as identity primary key,
  transcripcion text not null,
  titulo text not null,
  resumen text not null,
  created_at timestamptz default now()
);
