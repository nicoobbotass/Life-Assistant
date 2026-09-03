"""
Apple Health no tiene API pública para apps de terceros. La vía es:

  Apple Watch/iPhone -> app "Health Auto Export" -> Atajo de iOS que se
  dispara solo (p.ej. cada noche) -> POST a este webhook con un JSON.

Ver docs/SALUD.md para la configuración exacta del Atajo.
"""
from datetime import date

from fastapi import APIRouter
from pydantic import BaseModel

from lib.supabase import supabase

router = APIRouter()


class DatosSalud(BaseModel):
    fecha: str
    pasos: int
    calorias_activas: float | None = None
    frecuencia_cardiaca_media: float | None = None


@router.post("/webhook")
def recibir_datos_salud(datos: DatosSalud):
    """Endpoint al que apunta el Atajo de iOS. Sin autenticación fuerte
    todavía — para producción, protégelo con una clave secreta en la URL
    o cabecera (ver docs/SALUD.md)."""
    supabase.table("salud_diaria").upsert(datos.model_dump(), on_conflict="fecha").execute()
    return {"ok": True}


@router.get("/resumen")
def resumen_hoy():
    hoy = date.today().isoformat()
    res = supabase.table("salud_diaria").select("*").eq("fecha", hoy).limit(1).execute()
    return res.data[0] if res.data else None
