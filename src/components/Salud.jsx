import { useEffect, useState } from 'react'
import { api } from '../lib/api.js'

export default function Salud() {
  const [datos, setDatos] = useState(null)

  useEffect(() => {
    api.salud.resumen().then(setDatos).catch(() => setDatos(null))
  }, [])

  if (!datos) {
    return (
      <div className="card">
        <div className="card__title">Salud (Apple Health)</div>
        <p style={{ color: 'var(--muted)', fontSize: 13 }}>
          Sin datos aún — configura el Atajo de exportación (ver docs/SALUD.md).
        </p>
      </div>
    )
  }

  return (
    <div className="card">
      <div className="card__title">Salud (Apple Health) — hoy</div>
      <div style={{ display: 'flex', gap: 24 }}>
        <div>
          <div style={{ fontSize: 28, fontWeight: 700 }}>{datos.pasos}</div>
          <div style={{ color: 'var(--muted)', fontSize: 12 }}>pasos</div>
        </div>
        <div>
          <div style={{ fontSize: 28, fontWeight: 700 }}>{datos.calorias_activas}</div>
          <div style={{ color: 'var(--muted)', fontSize: 12 }}>kcal activas</div>
        </div>
      </div>
    </div>
  )
}
