"""
Tareas pendientes de Canvas LMS.

Necesita un token personal: en Canvas ve a
Cuenta -> Configuración -> "+ Nuevo token de acceso".
Guárdalo como CANVAS_TOKEN en backend/.env, junto con la URL de tu
instancia (p.ej. https://tuuniversidad.instructure.com) en CANVAS_URL.
"""
import os
from datetime import datetime, timedelta

import httpx
from fastapi import APIRouter

router = APIRouter()

CANVAS_URL = os.environ.get("CANVAS_URL", "")
CANVAS_TOKEN = os.environ.get("CANVAS_TOKEN", "")


@router.get("/pendientes")
async def tareas_pendientes(dias: int = 14):
    """Devuelve las tareas (assignments) con fecha de entrega en los
    próximos `dias` días, de todos los cursos activos."""
    limite = datetime.utcnow() + timedelta(days=dias)
    headers = {"Authorization": f"Bearer {CANVAS_TOKEN}"}

    async with httpx.AsyncClient() as client:
        cursos_resp = await client.get(
            f"{CANVAS_URL}/api/v1/courses",
            params={"enrollment_state": "active", "per_page": 50},
            headers=headers,
        )
        cursos_resp.raise_for_status()
        cursos = cursos_resp.json()

        tareas = []
        for curso in cursos:
            r = await client.get(
                f"{CANVAS_URL}/api/v1/courses/{curso['id']}/assignments",
                params={"per_page": 100, "order_by": "due_at"},
                headers=headers,
            )
            r.raise_for_status()
            for t in r.json():
                if not t.get("due_at"):
                    continue
                fecha = datetime.fromisoformat(t["due_at"].replace("Z", "+00:00"))
                if fecha.replace(tzinfo=None) <= limite:
                    tareas.append(
                        {
                            "id": t["id"],
                            "titulo": t["name"],
                            "curso": curso.get("name"),
                            "fecha_entrega": t["due_at"],
                            "url": t.get("html_url"),
                        }
                    )

    tareas.sort(key=lambda t: t["fecha_entrega"])
    return tareas
