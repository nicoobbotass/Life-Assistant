// Base del backend. En dev, FastAPI corre en :8000; en producción, cambia
// VITE_API_URL en tu .env de frontend a la URL donde despliegues el backend.
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function request(path, options = {}) {
  const res = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options
  })
  if (!res.ok) throw new Error(`Error ${res.status} en ${path}`)
  return res.json()
}

export const api = {
  calendario: {
    hoy: () => request('/calendario/hoy'),
    proximos: (dias = 7) => request(`/calendario/proximos?dias=${dias}`)
  },
  canvas: {
    pendientes: () => request('/canvas/pendientes')
  },
  entrenamientos: {
    semana: () => request('/entrenamientos/semana'),
    registrar: (datos) =>
      request('/entrenamientos', { method: 'POST', body: JSON.stringify(datos) }),
    objetivos: () => request('/entrenamientos/objetivos'),
    guardarObjetivo: (datos) =>
      request('/entrenamientos/objetivos', { method: 'POST', body: JSON.stringify(datos) })
  },
  notasVoz: {
    subir: (blobAudio) => {
      const form = new FormData()
      form.append('audio', blobAudio, 'nota.webm')
      return fetch(`${API_URL}/notas-voz`, { method: 'POST', body: form }).then((r) => r.json())
    },
    listar: () => request('/notas-voz')
  },
  salud: {
    resumen: () => request('/salud/resumen')
  }
}
