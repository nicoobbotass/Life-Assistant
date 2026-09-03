"""
Calendario de Outlook vía Microsoft Graph API.

Requiere una app registrada en Azure Portal (Entra ID) con permiso
delegado `Calendars.Read`. El flujo de auth (login + refresh token) se
hace una sola vez y el refresh token se guarda en Supabase; aquí se
asume que ya existe una función `obtener_token_valido()` que lo gestiona.

Guía paso a paso de registro de la app: docs/DESPLIEGUE.md
"""
import os
from datetime import datetime, timedelta

import httpx
from fastapi import APIRouter

router = APIRouter()

GRAPH_URL = "https://graph.microsoft.com/v1.0"


def obtener_token_valido() -> str:
    """TODO: implementar con MSAL — intercambia el refresh token guardado
    en Supabase por un access token vigente. Ver docs/BACKEND_REFERENCIA.md
    del repo de referencia para el patrón exacto (msal.ConfidentialClientApplication).
    """
    raise NotImplementedError("Configura el flujo OAuth de Microsoft Graph")


@router.get("/proximos")
async def proximos_eventos(dias: int = 7):
    token = obtener_token_valido()
    inicio = datetime.utcnow().isoformat()
    fin = (datetime.utcnow() + timedelta(days=dias)).isoformat()

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{GRAPH_URL}/me/calendarview",
            params={"startDateTime": inicio, "endDateTime": fin, "$orderby": "start/dateTime"},
            headers={"Authorization": f"Bearer {token}"},
        )
        resp.raise_for_status()
        eventos = resp.json()["value"]

    return [
        {
            "id": e["id"],
            "titulo": e["subject"],
            "inicio": e["start"]["dateTime"],
            "fin": e["end"]["dateTime"],
            "lugar": e.get("location", {}).get("displayName"),
        }
        for e in eventos
    ]


@router.get("/hoy")
async def eventos_hoy():
    return await proximos_eventos(dias=1)
