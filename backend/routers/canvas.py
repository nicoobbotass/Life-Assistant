"""
Tareas pendientes de Canvas — vía el feed de calendario (.ics), no la API REST.

Útil cuando tu institución tiene desactivada la creación de tokens
personales. El feed es una URL única por usuario que ya funciona como
autenticación (nadie más la conoce), así que no hace falta login.

Cómo encontrarla: en Canvas, ve a Calendario -> botón "Calendario"
(abajo a la derecha) -> "Feed de calendario" (Calendar Feed). Copia esa
URL completa (empieza por https:// y termina en .ics) en CANVAS_ICS_URL,
dentro de backend/.env.
"""
import os
import re
from datetime import datetime, timedelta, timezone

import httpx
from fastapi import APIRouter
from icalendar import Calendar

router = APIRouter()

CANVAS_ICS_URL = os.environ.get("CANVAS_ICS_URL", "")

PATRON_CURSO = re.compile(r"\[([^\]]+)\]\s*$")


def _a_datetime(valor) -> datetime:
    dt = valor.dt
    if not isinstance(dt, datetime):
        dt = datetime(dt.year, dt.month, dt.day, tzinfo=timezone.utc)
    elif dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


@router.get("/pendientes")
async def tareas_pendientes(dias: int = 14):
    if not CANVAS_ICS_URL:
        return []

    async with httpx.AsyncClient() as client:
        resp = await client.get(CANVAS_ICS_URL, timeout=15)
        resp.raise_for_status()

    calendario = Calendar.from_ical(resp.content)
    ahora = datetime.now(timezone.utc)
    limite = ahora + timedelta(days=dias)

    tareas = []
    for evento in calendario.walk("VEVENT"):
        uid = str(evento.get("UID", ""))
        if "assignment" not in uid:
            continue
        if "DTSTART" not in evento:
            continue

        fecha = _a_datetime(evento["DTSTART"])
        if not (ahora <= fecha <= limite):
            continue

        titulo_completo = str(evento.get("SUMMARY", "Sin título"))
        match = PATRON_CURSO.search(titulo_completo)
        curso = match.group(1) if match else None
        titulo = PATRON_CURSO.sub("", titulo_completo).strip()

        tareas.append(
            {
                "id": uid,
                "titulo": titulo,
                "curso": curso,
                "fecha_entrega": fecha.isoformat(),
                "url": str(evento.get("URL", "")) or None,
            }
        )

    tareas.sort(key=lambda t: t["fecha_entrega"])
    return tareas