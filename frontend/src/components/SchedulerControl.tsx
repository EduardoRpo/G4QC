import { useState } from 'react'
import { Play, Square, Settings, RefreshCw } from 'lucide-react'
import { api } from '../services/api'

interface SchedulerControlProps {
  schedulerStatus: any
  onUpdate: () => void
}

export default function SchedulerControl({ schedulerStatus, onUpdate }: SchedulerControlProps) {
  const [loading, setLoading] = useState(false)
  const [config, setConfig] = useState({
    update_interval_minutes: schedulerStatus?.update_interval_minutes || 1,
    market_hours_start: schedulerStatus?.market_hours_start || '09:00',
    market_hours_end: schedulerStatus?.market_hours_end || '16:00',
    symbols: schedulerStatus?.symbols || ['ES', 'NQ'],
    timeframes: schedulerStatus?.timeframes || ['1min'],
  })
  const [showConfig, setShowConfig] = useState(false)

  const handleEnable = async () => {
    setLoading(true)
    try {
      await api.enableScheduler()
      onUpdate()
    } catch (error: any) {
      console.error('Error enabling scheduler:', error)
      const errorMsg = error.response?.data?.detail?.message || 
                      error.response?.data?.detail || 
                      error.message || 
                      'Error al activar el scheduler'
      alert(`Error al activar el scheduler: ${errorMsg}`)
    } finally {
      setLoading(false)
    }
  }

  const handleDisable = async () => {
    setLoading(true)
    try {
      await api.disableScheduler()
      onUpdate()
    } catch (error) {
      console.error('Error disabling scheduler:', error)
      alert('Error al desactivar el scheduler')
    } finally {
      setLoading(false)
    }
  }

  const handleRunNow = async () => {
    setLoading(true)
    try {
      await api.runSchedulerNow()
      alert('Scheduler ejecutado manualmente')
      onUpdate()
    } catch (error) {
      console.error('Error running scheduler:', error)
      alert('Error al ejecutar el scheduler')
    } finally {
      setLoading(false)
    }
  }

  const handleUpdateConfig = async () => {
    setLoading(true)
    try {
      await api.updateSchedulerConfig(config)
      alert('Configuración actualizada')
      setShowConfig(false)
      onUpdate()
    } catch (error: any) {
      console.error('Error updating config:', error)
      const errorMsg = error.response?.data?.detail?.message || 
                      error.response?.data?.detail || 
                      error.message || 
                      'Error al actualizar la configuración'
      alert(`Error al actualizar la configuración: ${errorMsg}`)
    } finally {
      setLoading(false)
    }
  }

  const isEnabled = schedulerStatus?.enabled || false

  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
        <Settings className="w-5 h-5" />
        Control del Scheduler
      </h2>

      <div className="space-y-4">
        <div className="flex gap-2">
          {!isEnabled ? (
            <button
              onClick={handleEnable}
              disabled={loading}
              className="flex-1 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 px-4 py-2 rounded-lg font-semibold flex items-center justify-center gap-2"
            >
              <Play className="w-4 h-4" />
              Activar Scheduler
            </button>
          ) : (
            <button
              onClick={handleDisable}
              disabled={loading}
              className="flex-1 bg-red-600 hover:bg-red-700 disabled:bg-gray-600 px-4 py-2 rounded-lg font-semibold flex items-center justify-center gap-2"
            >
              <Square className="w-4 h-4" />
              Desactivar Scheduler
            </button>
          )}
          
          <button
            onClick={handleRunNow}
            disabled={loading || !isEnabled}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 px-4 py-2 rounded-lg font-semibold flex items-center justify-center gap-2"
          >
            <RefreshCw className="w-4 h-4" />
            Ejecutar Ahora
          </button>
        </div>

        <button
          onClick={() => setShowConfig(!showConfig)}
          className="w-full bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded-lg text-sm"
        >
          {showConfig ? 'Ocultar' : 'Mostrar'} Configuración
        </button>

        {showConfig && (
          <div className="bg-gray-700 rounded-lg p-4 space-y-4">
            <div>
              <label className="block text-sm text-gray-300 mb-1">
                Intervalo (minutos)
              </label>
              <input
                type="number"
                value={config.update_interval_minutes}
                onChange={(e) => setConfig({ ...config, update_interval_minutes: parseInt(e.target.value) })}
                className="w-full bg-gray-600 text-white px-3 py-2 rounded"
                min="1"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm text-gray-300 mb-1">
                  Inicio (HH:MM)
                </label>
                <input
                  type="time"
                  value={config.market_hours_start}
                  onChange={(e) => setConfig({ ...config, market_hours_start: e.target.value })}
                  className="w-full bg-gray-600 text-white px-3 py-2 rounded"
                />
              </div>
              <div>
                <label className="block text-sm text-gray-300 mb-1">
                  Fin (HH:MM)
                </label>
                <input
                  type="time"
                  value={config.market_hours_end}
                  onChange={(e) => setConfig({ ...config, market_hours_end: e.target.value })}
                  className="w-full bg-gray-600 text-white px-3 py-2 rounded"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm text-gray-300 mb-1">
                Símbolos (separados por comas)
              </label>
              <input
                type="text"
                value={config.symbols.join(', ')}
                onChange={(e) => setConfig({ ...config, symbols: e.target.value.split(',').map(s => s.trim()) })}
                className="w-full bg-gray-600 text-white px-3 py-2 rounded"
                placeholder="ES, NQ, YM"
              />
            </div>

            <div>
              <label className="block text-sm text-gray-300 mb-1">
                Timeframes (separados por comas)
              </label>
              <input
                type="text"
                value={config.timeframes.join(', ')}
                onChange={(e) => setConfig({ ...config, timeframes: e.target.value.split(',').map(s => s.trim()) })}
                className="w-full bg-gray-600 text-white px-3 py-2 rounded"
                placeholder="1min, 5min"
              />
            </div>

            <button
              onClick={handleUpdateConfig}
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 px-4 py-2 rounded-lg font-semibold"
            >
              Actualizar Configuración
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

