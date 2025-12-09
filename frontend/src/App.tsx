import { useState, useEffect } from 'react'
import Dashboard from './components/Dashboard'
import SchedulerControl from './components/SchedulerControl'
import DataExtraction from './components/DataExtraction'
import DataViewer from './components/DataViewer'
import { api } from './services/api'

function App() {
  const [schedulerStatus, setSchedulerStatus] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadSchedulerStatus()
    // Actualizar estado cada 5 segundos
    const interval = setInterval(loadSchedulerStatus, 5000)
    return () => clearInterval(interval)
  }, [])

  const loadSchedulerStatus = async () => {
    try {
      const status = await api.getSchedulerStatus()
      setSchedulerStatus(status)
    } catch (error) {
      console.error('Error loading scheduler status:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-white text-xl">Cargando...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <header className="bg-gray-800 border-b border-gray-700 px-6 py-4">
        <h1 className="text-2xl font-bold">G4QC Trading Platform</h1>
        <p className="text-gray-400 text-sm">Sistema de Trading Automatizado</p>
      </header>

      <main className="container mx-auto px-6 py-8">
        <Dashboard schedulerStatus={schedulerStatus} />
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
          <SchedulerControl 
            schedulerStatus={schedulerStatus} 
            onUpdate={loadSchedulerStatus}
          />
          <DataExtraction onExtract={loadSchedulerStatus} />
        </div>

        <div className="mt-6">
          <DataViewer />
        </div>
      </main>
    </div>
  )
}

export default App

