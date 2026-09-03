import Calendario from './Calendario.jsx'
import Canvas from './Canvas.jsx'
import Entrenamientos from './Entrenamientos.jsx'
import Objetivos from './Objetivos.jsx'
import NotasVoz from './NotasVoz.jsx'
import Salud from './Salud.jsx'
import './dashboard.css'

export default function Dashboard() {
  return (
    <div className="dashboard">
      <header className="dashboard__header">
        <h1>Life Assistant</h1>
      </header>

      <div className="dashboard__grid">
        <Calendario />
        <Canvas />
        <Entrenamientos />
        <Objetivos />
        <Salud />
        <NotasVoz />
      </div>
    </div>
  )
}
