# Despliegue

## 1. Supabase
1. Crea un proyecto en https://supabase.com
2. Ve a SQL Editor y ejecuta, en orden, los archivos de `supabase/migrations/`
3. Copia `Project URL` y la `service_role key` (Settings → API) a `SUPABASE_URL` y `SUPABASE_SERVICE_KEY`

## 2. Microsoft Graph (Outlook)
1. https://portal.azure.com → Entra ID → Registros de aplicaciones → Nuevo registro
2. Añade el permiso delegado `Calendars.Read`
3. Genera un secreto de cliente
4. Copia Client ID, Client Secret y Tenant ID a `.env`

## 3. Canvas
1. En Canvas: Cuenta → Configuración → "+ Nuevo token de acceso"
2. Copia el token y la URL de tu instancia a `.env`

## 4. Backend
```
cd backend
cp .env.example .env   # rellena las claves
pip install -r requirements.txt
uvicorn main:app --reload
```

## 5. Frontend
```
npm install
echo "VITE_API_URL=http://localhost:8000" > .env
npm run dev
```

## 6. Producción
- Backend: Fly.io o Render (free tier vale para empezar)
- Frontend: Vercel o Netlify, apuntando `VITE_API_URL` al backend desplegado
