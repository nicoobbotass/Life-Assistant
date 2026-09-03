from datetime import date, timedelta

from fastapi import APIRouter
from pydantic import BaseModel

from lib.supabase import supabase

router = APIRouter()


class NuevoEntrenamiento(BaseModel):
    fecha: str
    tipo: str | None = None


class Objetivo(BaseModel):
    entrenamientos_semana: int
    pasos_diarios: int


def inicio_semana() -> date:
    hoy = date.today()
    return hoy - timedelta(days=hoy.weekday())  # lunes


@router.get("/semana")
def resumen_semana():
    desde = inicio_semana().isoformat()
    entrenamientos = (
        supabase.table("entrenamientos").select("*").gte("fecha", desde).execute()
    )
    objetivo = supabase.table("objetivos_actividad").select("*").limit(1).execute()

    return {
        "completados": len(entrenamientos.data),
        "objetivo": objetivo.data[0]["entrenamientos_semana"] if objetivo.data else 4,
        "desde": desde,
    }


@router.post("")
def registrar_entrenamiento(datos: NuevoEntrenamiento):
    fila = supabase.table("entrenamientos").insert(datos.model_dump()).execute()
    return fila.data[0]


@router.get("/objetivos")
def obtener_objetivos():
    res = supabase.table("objetivos_actividad").select("*").limit(1).execute()
    return res.data[0] if res.data else None


@router.post("/objetivos")
def guardar_objetivos(datos: Objetivo):
    existente = supabase.table("objetivos_actividad").select("id").limit(1).execute()
    if existente.data:
        fila = (
            supabase.table("objetivos_actividad")
            .update(datos.model_dump())
            .eq("id", existente.data[0]["id"])
            .execute()
        )
    else:
        fila = supabase.table("objetivos_actividad").insert(datos.model_dump()).execute()
    return fila.data[0]
