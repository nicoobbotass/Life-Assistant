# Life Assistant (tu versión)

Dashboard personal instalable (PWA) que centraliza:

- **Calendario** — eventos de Outlook (Microsoft Graph API)
- **Canvas** — tareas pendientes con notificación push cuando se acerca la entrega
- **Notas de voz** — grabas una idea, se transcribe y se resume en el punto clave
- **Entrenamientos** — contador semanal + objetivos configurables
- **Salud** — pasos, calorías y entrenamientos desde Apple Health (vía Atajos)

Inspirado en la estructura de [Life-Assistant de malbisudlf](https://github.com/malbisudlf/Life-Assistant),
recortado a estas cinco funciones.

## Stack

| Capa | Tecnología |
|---|---|
| Frontend | React + Vite, PWA instalable en el móvil |
| Backend | FastAPI (Python), un solo servicio |
| Base de datos | Supabase (Postgres) |
| Calendario | Microsoft Graph API (Outlook) — OAuth |
| Tareas | Canvas LMS REST API (token personal) |
| Voz | Whisper (transcripción) + Claude API (resumen de idea clave) |
| Salud | Apple Health → app "Health Auto Export" → Atajos → webhook propio |
| Notificaciones | Web Push (funciona en iOS 16.4+ como PWA instalada) |

## Estructura

```
life-assistant/
├── src/                    # Frontend React
│   ├── App.jsx
│   └── components/
│       ├── Dashboard.jsx
│       ├── Calendario.jsx
│       ├── Canvas.jsx
│       ├── Entrenamientos.jsx
│       ├── Objetivos.jsx
│       ├── NotasVoz.jsx
│       └── Salud.jsx
├── backend/                 # FastAPI
│   ├── main.py
│   └── routers/
│       ├── calendario.py    # Microsoft Graph
│       ├── canvas.py        # Canvas LMS
│       ├── notas_voz.py     # Whisper + resumen
│       ├── entrenamientos.py
│       └── salud.py         # webhook de Atajos
└── supabase/migrations/     # esquema de base de datos
```

## Puesta en marcha (resumen — detalle en `docs/DESPLIEGUE.md`)

1. Crea un proyecto en [Supabase](https://supabase.com) y aplica las migraciones de `supabase/migrations/`.
2. Registra una app en [Azure Portal](https://portal.azure.com) (Entra ID) para obtener `MS_CLIENT_ID`, `MS_CLIENT_SECRET` y `MS_TENANT_ID` — esto da acceso a Outlook vía Graph.
3. Genera un token personal en Canvas: `Cuenta → Configuración → Nuevo token de acceso`.
4. Copia `backend/.env.example` a `backend/.env` y rellena las claves.
5. `cd backend && pip install -r requirements.txt && uvicorn main:app --reload`
6. `npm install && npm run dev` para el frontend.
7. En el iPhone: instala la app "Health Auto Export" y configura un Atajo que mande tus datos de salud al endpoint `/salud/webhook` una vez al día (ver `docs/SALUD.md`).
