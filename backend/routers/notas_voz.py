"""
Flujo: audio grabado en el navegador -> Whisper transcribe -> Claude
extrae título + resumen de la idea clave -> se guarda en Supabase.

Necesita OPENAI_API_KEY (solo para Whisper) y ANTHROPIC_API_KEY.
"""
import os
import json

import httpx
from fastapi import APIRouter, UploadFile, File
from openai import OpenAI

from lib.supabase import supabase  # cliente sencillo, ver backend/lib/supabase.py

router = APIRouter()

openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")


async def resumir_idea(transcripcion: str) -> dict:
    """Manda la transcripción a Claude y pide un JSON con título + resumen."""
    prompt = (
        "Te doy la transcripción de una nota de voz. Devuelve SOLO un JSON "
        'con esta forma exacta: {"titulo": "...", "resumen": "..."}. '
        "El título son 3-6 palabras. El resumen es una frase con la idea clave, "
        "nada de relleno.\n\nTranscripción:\n" + transcripcion
    )
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-6",
                "max_tokens": 200,
                "messages": [{"role": "user", "content": prompt}],
            },
        )
        resp.raise_for_status()
        texto = resp.json()["content"][0]["text"]
        return json.loads(texto)


@router.post("")
async def crear_nota(audio: UploadFile = File(...)):
    audio_bytes = await audio.read()

    transcripcion = openai_client.audio.transcriptions.create(
        model="whisper-1",
        file=(audio.filename, audio_bytes, audio.content_type),
    ).text

    idea = await resumir_idea(transcripcion)

    fila = (
        supabase.table("notas_voz")
        .insert(
            {
                "transcripcion": transcripcion,
                "titulo": idea["titulo"],
                "resumen": idea["resumen"],
            }
        )
        .execute()
    )
    return fila.data[0]


@router.get("")
def listar_notas():
    res = supabase.table("notas_voz").select("*").order("created_at", desc=True).limit(20).execute()
    return res.data
