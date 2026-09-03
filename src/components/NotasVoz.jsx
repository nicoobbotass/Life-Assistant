import { useRef, useState, useEffect } from 'react'
import { api } from '../lib/api.js'

export default function NotasVoz() {
  const [grabando, setGrabando] = useState(false)
  const [notas, setNotas] = useState([])
  const [procesando, setProcesando] = useState(false)
  const mediaRecorder = useRef(null)
  const chunks = useRef([])

  const cargarNotas = () => api.notasVoz.listar().then(setNotas).catch(() => {})
  useEffect(() => { cargarNotas() }, [])

  const empezarGrabacion = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder.current = new MediaRecorder(stream)
    chunks.current = []
    mediaRecorder.current.ondataavailable = (e) => chunks.current.push(e.data)
    mediaRecorder.current.onstop = async () => {
      const blob = new Blob(chunks.current, { type: 'audio/webm' })
      setProcesando(true)
      await api.notasVoz.subir(blob)
      setProcesando(false)
      cargarNotas()
    }
    mediaRecorder.current.start()
    setGrabando(true)
  }

  const pararGrabacion = () => {
    mediaRecorder.current?.stop()
    setGrabando(false)
  }

  return (
    <div className="card">
      <div className="card__title">Ideas por voz</div>
      <button onClick={grabando ? pararGrabacion : empezarGrabacion}>
        {grabando ? '⏹ Parar y guardar' : '🎙 Grabar idea'}
      </button>
      {procesando && <p style={{ color: 'var(--muted)', fontSize: 13 }}>Transcribiendo y resumiendo…</p>}
      <div style={{ marginTop: 12 }}>
        {notas.map((n) => (
          <div key={n.id} style={{ marginBottom: 8 }}>
            <strong>{n.titulo}</strong>
            <div style={{ color: 'var(--muted)', fontSize: 13 }}>{n.resumen}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
