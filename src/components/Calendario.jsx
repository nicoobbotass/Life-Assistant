import { useEffect, useState } from 'react'
import { api } from '../lib/api.js'

export default function Calendario() {
  const [eventos, setEventos] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    api.calendario.proximos(7).then(setEventos).catch((e) => setError(e.message))
  }, [])

  return (
    <div className="card">
      <div className="card__title">Calendario (Outlook)</div>
      {error && <p>No se pudo cargar: {error}</p>}
      {!eventos && !error && <p>Cargando…</p>}
      {eventos?.map((ev) => (
        <div key={ev.id} style={{ marginBottom: 8 }}>
          <strong>{ev.titulo}</strong>
          <div style={{ color: 'var(--muted)', fontSize: 13 }}>
            {new Date(ev.inicio).toLocaleString('es-ES', {
              weekday: 'short',
              hour: '2-digit',
              minute: '2-digit'
            })}
          </div>
        </div>
      ))}
    </div>
  )
}
