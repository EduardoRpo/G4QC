import { useState, useEffect } from 'react'
import { Database, RefreshCw, TrendingUp } from 'lucide-react'
import { api } from '../services/api'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

export default function DataViewer() {
  const [symbols, setSymbols] = useState<string[]>([])
  const [selectedSymbol, setSelectedSymbol] = useState('')
  const [timeframes, setTimeframes] = useState<string[]>([])
  const [selectedTimeframe, setSelectedTimeframe] = useState('1min')
  const [data, setData] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadSymbols()
  }, [])

  useEffect(() => {
    if (selectedSymbol) {
      loadTimeframes(selectedSymbol)
    }
  }, [selectedSymbol])

  useEffect(() => {
    if (selectedSymbol && selectedTimeframe) {
      loadData()
    }
  }, [selectedSymbol, selectedTimeframe])

  const loadSymbols = async () => {
    try {
      const response = await api.getSymbols()
      setSymbols(response.symbols || [])
      if (response.symbols && response.symbols.length > 0) {
        setSelectedSymbol(response.symbols[0])
      }
    } catch (error) {
      console.error('Error loading symbols:', error)
    }
  }

  const loadTimeframes = async (symbol: string) => {
    try {
      const response = await api.getTimeframes(symbol)
      setTimeframes(response.timeframes || [])
      if (response.timeframes && response.timeframes.length > 0) {
        setSelectedTimeframe(response.timeframes[0])
      }
    } catch (error) {
      console.error('Error loading timeframes:', error)
    }
  }

  const loadData = async () => {
    setLoading(true)
    try {
      const response = await api.getData(selectedSymbol, selectedTimeframe, 100)
      const formattedData = response.data?.map((item: any) => ({
        timestamp: new Date(item.timestamp).toLocaleString('es-ES'),
        close: parseFloat(item.close),
        open: parseFloat(item.open),
        high: parseFloat(item.high),
        low: parseFloat(item.low),
        volume: parseInt(item.volume),
      })) || []
      setData(formattedData)
    } catch (error) {
      console.error('Error loading data:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold flex items-center gap-2">
          <Database className="w-5 h-5" />
          Visualización de Datos
        </h2>
        <button
          onClick={loadData}
          disabled={loading || !selectedSymbol}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 px-4 py-2 rounded-lg text-sm flex items-center gap-2"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          Actualizar
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div>
          <label className="block text-sm text-gray-300 mb-1">
            Símbolo
          </label>
          <select
            value={selectedSymbol}
            onChange={(e) => setSelectedSymbol(e.target.value)}
            className="w-full bg-gray-700 text-white px-3 py-2 rounded"
          >
            <option value="">Seleccionar...</option>
            {symbols.map((symbol) => (
              <option key={symbol} value={symbol}>
                {symbol}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm text-gray-300 mb-1">
            Timeframe
          </label>
          <select
            value={selectedTimeframe}
            onChange={(e) => setSelectedTimeframe(e.target.value)}
            className="w-full bg-gray-700 text-white px-3 py-2 rounded"
            disabled={!selectedSymbol}
          >
            {timeframes.map((tf) => (
              <option key={tf} value={tf}>
                {tf}
              </option>
            ))}
          </select>
        </div>

        <div className="flex items-end">
          <div className="bg-gray-700 rounded-lg px-4 py-2 w-full">
            <div className="text-sm text-gray-400">Registros</div>
            <div className="text-xl font-bold">{data.length}</div>
          </div>
        </div>
      </div>

      {data.length > 0 && (
        <>
          <div className="bg-gray-700 rounded-lg p-4 mb-4" style={{ height: '400px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data.slice(-50)}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis 
                  dataKey="timestamp" 
                  stroke="#9CA3AF"
                  tick={{ fill: '#9CA3AF', fontSize: 12 }}
                  angle={-45}
                  textAnchor="end"
                  height={80}
                />
                <YAxis 
                  stroke="#9CA3AF"
                  tick={{ fill: '#9CA3AF', fontSize: 12 }}
                />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#1F2937', 
                    border: '1px solid #374151',
                    borderRadius: '8px'
                  }}
                />
                <Line 
                  type="monotone" 
                  dataKey="close" 
                  stroke="#3B82F6" 
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="bg-gray-700 rounded-lg p-4 max-h-64 overflow-y-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-600">
                  <th className="text-left py-2 px-2 text-gray-300">Timestamp</th>
                  <th className="text-right py-2 px-2 text-gray-300">Open</th>
                  <th className="text-right py-2 px-2 text-gray-300">High</th>
                  <th className="text-right py-2 px-2 text-gray-300">Low</th>
                  <th className="text-right py-2 px-2 text-gray-300">Close</th>
                  <th className="text-right py-2 px-2 text-gray-300">Volume</th>
                </tr>
              </thead>
              <tbody>
                {data.slice(-20).reverse().map((item, index) => (
                  <tr key={index} className="border-b border-gray-600 hover:bg-gray-600">
                    <td className="py-2 px-2 text-gray-400">{item.timestamp}</td>
                    <td className="py-2 px-2 text-right">{item.open.toFixed(2)}</td>
                    <td className="py-2 px-2 text-right text-green-400">{item.high.toFixed(2)}</td>
                    <td className="py-2 px-2 text-right text-red-400">{item.low.toFixed(2)}</td>
                    <td className="py-2 px-2 text-right font-semibold">{item.close.toFixed(2)}</td>
                    <td className="py-2 px-2 text-right text-gray-400">{item.volume}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}

      {data.length === 0 && !loading && selectedSymbol && (
        <div className="text-center py-8 text-gray-400">
          No hay datos disponibles para {selectedSymbol} ({selectedTimeframe})
        </div>
      )}
    </div>
  )
}

