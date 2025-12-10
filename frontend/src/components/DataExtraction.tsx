import { useState } from 'react'
import { Download, Loader } from 'lucide-react'
import { api } from '../services/api'

interface DataExtractionProps {
  onExtract: () => void
}

export default function DataExtraction({ onExtract }: DataExtractionProps) {
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    symbol: 'ES',
    duration: '1 D',
    bar_size: '1 min',
    num_blocks: 1,
    contract_month: '',
  })

  const handleExtract = async () => {
    setLoading(true)
    try {
      const params: any = {
        symbol: formData.symbol,
        duration: formData.duration,
        bar_size: formData.bar_size,
        num_blocks: formData.num_blocks,
      }
      
      if (formData.contract_month) {
        params.contract_month = formData.contract_month
      }

      const response = await api.extractData(params)
      alert(`Extracción completada: ${response.records_saved || 0} registros guardados`)
      onExtract()
    } catch (error: any) {
      console.error('Error extracting data:', error)
      const errorMsg = error.response?.data?.detail?.message || 
                      (typeof error.response?.data?.detail === 'string' ? error.response?.data?.detail : '') ||
                      error.response?.data?.detail?.error ||
                      error.message || 
                      'Error desconocido'
      alert(`Error al extraer datos: ${errorMsg}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
        <Download className="w-5 h-5" />
        Extracción Manual de Datos
      </h2>

      <div className="space-y-4">
        <div>
          <label className="block text-sm text-gray-300 mb-1">
            Símbolo
          </label>
          <input
            type="text"
            value={formData.symbol}
            onChange={(e) => setFormData({ ...formData, symbol: e.target.value.toUpperCase() })}
            className="w-full bg-gray-700 text-white px-3 py-2 rounded"
            placeholder="ES, NQ, YM, GC..."
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm text-gray-300 mb-1">
              Duración
            </label>
            <select
              value={formData.duration}
              onChange={(e) => setFormData({ ...formData, duration: e.target.value })}
              className="w-full bg-gray-700 text-white px-3 py-2 rounded"
            >
              <option value="1 D">1 Día</option>
              <option value="1 W">1 Semana</option>
              <option value="1 M">1 Mes</option>
              <option value="3 M">3 Meses</option>
            </select>
          </div>

          <div>
            <label className="block text-sm text-gray-300 mb-1">
              Tamaño de Barra
            </label>
            <select
              value={formData.bar_size}
              onChange={(e) => setFormData({ ...formData, bar_size: e.target.value })}
              className="w-full bg-gray-700 text-white px-3 py-2 rounded"
            >
              <option value="1 min">1 minuto</option>
              <option value="5 mins">5 minutos</option>
              <option value="15 mins">15 minutos</option>
              <option value="1 hour">1 hora</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm text-gray-300 mb-1">
              Bloques
            </label>
            <input
              type="number"
              value={formData.num_blocks}
              onChange={(e) => setFormData({ ...formData, num_blocks: parseInt(e.target.value) })}
              className="w-full bg-gray-700 text-white px-3 py-2 rounded"
              min="1"
              max="12"
            />
          </div>

          <div>
            <label className="block text-sm text-gray-300 mb-1">
              Mes de Contrato (opcional)
            </label>
            <input
              type="text"
              value={formData.contract_month}
              onChange={(e) => setFormData({ ...formData, contract_month: e.target.value })}
              className="w-full bg-gray-700 text-white px-3 py-2 rounded"
              placeholder="202512"
            />
          </div>
        </div>

        <button
          onClick={handleExtract}
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 px-4 py-2 rounded-lg font-semibold flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <Loader className="w-4 h-4 animate-spin" />
              Extrayendo...
            </>
          ) : (
            <>
              <Download className="w-4 h-4" />
              Extraer Datos
            </>
          )}
        </button>
      </div>
    </div>
  )
}

