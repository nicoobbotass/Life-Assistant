import { useEffect, useState } from 'react'
import { api } from '../lib/api.js'

export default function Objetivos() {
  const [objetivo, setObjetivo] = useState(null)
  const [form, setForm] = useState({ entrenamientos_semana: 4, pasos_diarios: 8000 })

  useEffect(() => {
    api.entrenamientos.objetivos().then((o) => {
      if (o) { setObjetivo(o); setForm(o) }
    }).catch(() => {})
  }, [])

  const guardar = async () => {
    const guardado = await api.entrenamientos.guardarObjetivo(form)
    setObjetivo(guardado)
  }

  return (
    <div className="card">
      <div className="card__title">Objetivos de actividad</div>
      <label style={{ display: 'block', marginBottom: 8, fontSize: 14 }}>
        Entrenamientos por semana
        <input
          type="number"
          value={form.entrenamientos_semana}
          onChange={(e) => setForm({ ...form, entrenamientos_semana: Number(e.target.value) })}
          style={{ display: 'block', marginTop: 4, width: '100%' }}
        />
      </label>
      <label style={{ display: 'block', marginBottom: 8, fontSize: 14 }}>
        Pasos diarios
        <input
          type="number"
          value={form.pasos_diarios}
          onChange={(e) => setForm({ ...form, pasos_diarios: Number(e.target.value) })}
          style={{ display: 'block', marginTop: 4, width: '100%' }}
        />
      </label>
      <button onClick={guardar}>Guardar objetivos</button>
      {objetivo && <p style={{ color: 'var(--muted)', fontSize: 12, marginTop: 8 }}>Guardado ✓</p>}
    </div>
  )
}
