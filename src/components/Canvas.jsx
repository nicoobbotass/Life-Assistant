import { useEffect, useState } from 'react'
import { api } from '../lib/api.js'

// Colorea según urgencia: rojo si entrega en <24h, ámbar si <72h, gris si más lejos.
function colorUrgencia(fechaEntrega) {
  const horas = (new Date(fechaEntrega) - new Date()) / 3600000
  if (horas < 24) return '#e05252'
  if (horas < 72) return 'var(--accent)'
  return 'var(--muted)'
}

export default function Canvas() {
  const [tareas, setTareas] = useState(null)

  useEffect(() => {
    api.canvas.pendientes().then(setTareas).catch(() => setTareas([]))
  }, [])

  return (
    <div className="card">
      <div className="card__title">Entregas pendientes (Canvas)</div>
      {!tareas && <p>Cargando…</p>}
      {tareas?.length === 0 && <p style={{ color: 'var(--muted)' }}>Sin entregas próximas.</p>}
      {tareas?.map((t) => (
        <div key={t.id} style={{ marginBottom: 8, borderLeft: `3px solid ${colorUrgencia(t.fecha_entrega)}`, paddingLeft: 8 }}>
          <strong>{t.titulo}</strong>
          <div style={{ color: 'var(--muted)', fontSize: 13 }}>{t.curso} · vence {new Date(t.fecha_entrega).toLocaleDateString('es-ES')}</div>
        </div>
      ))}
    </div>
  )
}
