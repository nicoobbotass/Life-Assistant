import { useEffect, useState } from 'react'
import { api } from '../lib/api.js'

export default function Entrenamientos() {
  const [datos, setDatos] = useState(null)

  const cargar = () => api.entrenamientos.semana().then(setDatos).catch(() => setDatos(null))

  useEffect(() => { cargar() }, [])

  const registrarHoy = async () => {
    await api.entrenamientos.registrar({ fecha: new Date().toISOString().slice(0, 10) })
    cargar()
  }

  return (
    <div className="card">
      <div className="card__title">Entrenamientos esta semana</div>
      {datos && (
        <>
          <div style={{ fontSize: 32, fontWeight: 700 }}>
            {datos.completados} <span style={{ fontSize: 16, color: 'var(--muted)' }}>/ {datos.objetivo}</span>
          </div>
          <button onClick={registrarHoy} style={{ marginTop: 8 }}>+ Registrar entrenamiento de hoy</button>
        </>
      )}
    </div>
  )
}
