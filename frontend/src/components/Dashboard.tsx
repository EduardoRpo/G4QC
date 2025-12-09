import { Activity, Database, Clock, CheckCircle, XCircle } from 'lucide-react'

interface DashboardProps {
  schedulerStatus: any
}

export default function Dashboard({ schedulerStatus }: DashboardProps) {
  const isEnabled = schedulerStatus?.enabled || false
  const lastRun = schedulerStatus?.last_run
  const nextRun = schedulerStatus?.next_run
  const jobsCount = schedulerStatus?.jobs_count || 0

  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
        <Activity className="w-5 h-5" />
        Estado del Sistema
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-gray-700 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-gray-400 text-sm">Scheduler</span>
            {isEnabled ? (
              <CheckCircle className="w-5 h-5 text-green-500" />
            ) : (
              <XCircle className="w-5 h-5 text-red-500" />
            )}
          </div>
          <p className="text-2xl font-bold">
            {isEnabled ? 'Activo' : 'Inactivo'}
          </p>
        </div>

        <div className="bg-gray-700 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-gray-400 text-sm">Jobs Activos</span>
            <Database className="w-5 h-5 text-blue-500" />
          </div>
          <p className="text-2xl font-bold">{jobsCount}</p>
        </div>

        <div className="bg-gray-700 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-gray-400 text-sm">Última Ejecución</span>
            <Clock className="w-5 h-5 text-yellow-500" />
          </div>
          <p className="text-sm">
            {lastRun 
              ? new Date(lastRun).toLocaleString('es-ES')
              : 'Nunca'
            }
          </p>
        </div>

        <div className="bg-gray-700 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-gray-400 text-sm">Próxima Ejecución</span>
            <Clock className="w-5 h-5 text-green-500" />
          </div>
          <p className="text-sm">
            {nextRun 
              ? new Date(nextRun).toLocaleString('es-ES')
              : 'No programada'
            }
          </p>
        </div>
      </div>

      {schedulerStatus && (
        <div className="mt-4 pt-4 border-t border-gray-700">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <span className="text-gray-400">Intervalo:</span>
              <p className="font-semibold">{schedulerStatus.update_interval_minutes} min</p>
            </div>
            <div>
              <span className="text-gray-400">Horario:</span>
              <p className="font-semibold">
                {schedulerStatus.market_hours_start} - {schedulerStatus.market_hours_end}
              </p>
            </div>
            <div>
              <span className="text-gray-400">Símbolos:</span>
              <p className="font-semibold">
                {schedulerStatus.symbols?.join(', ') || 'Ninguno'}
              </p>
            </div>
            <div>
              <span className="text-gray-400">Timeframes:</span>
              <p className="font-semibold">
                {schedulerStatus.timeframes?.join(', ') || 'Ninguno'}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

