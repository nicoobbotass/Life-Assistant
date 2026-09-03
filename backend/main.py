from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()

from routers import calendario, canvas, entrenamientos, notas_voz, salud

app = FastAPI(title="Life Assistant API")

# En producción, restringe esto a tu dominio del frontend (Vercel, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(calendario.router, prefix="/calendario", tags=["calendario"])
app.include_router(canvas.router, prefix="/canvas", tags=["canvas"])
app.include_router(entrenamientos.router, prefix="/entrenamientos", tags=["entrenamientos"])
app.include_router(notas_voz.router, prefix="/notas-voz", tags=["notas de voz"])
app.include_router(salud.router, prefix="/salud", tags=["salud"])


@app.get("/")
def estado():
    return {"estado": "ok"}
