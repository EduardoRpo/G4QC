import axios from 'axios'

// En desarrollo, usar localhost. En Docker, usar el nombre del servicio
// Vite inyecta variables de entorno en tiempo de compilación
const API_BASE_URL = import.meta.env.VITE_API_URL || 
  (import.meta.env.DEV ? 'http://localhost:8000' : 'http://45.137.192.196:8000')

console.log('🔧 API Base URL:', API_BASE_URL)

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 segundos de timeout
})

// Interceptor para manejar errores
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('❌ API Error:', {
      url: error.config?.url,
      method: error.config?.method,
      status: error.response?.status,
      data: error.response?.data,
      message: error.message,
    })
    return Promise.reject(error)
  }
)

export const api = {
  // Scheduler endpoints
  async getSchedulerStatus() {
    const response = await apiClient.get('/api/v1/scheduler/status')
    return response.data
  },

  async enableScheduler() {
    const response = await apiClient.post('/api/v1/scheduler/enable')
    return response.data
  },

  async disableScheduler() {
    const response = await apiClient.post('/api/v1/scheduler/disable')
    return response.data
  },

  async updateSchedulerConfig(config: any) {
    const response = await apiClient.put('/api/v1/scheduler/config', config)
    return response.data
  },

  async runSchedulerNow() {
    const response = await apiClient.post('/api/v1/scheduler/run-now')
    return response.data
  },

  // Data extraction endpoints
  async extractData(params: {
    symbol: string
    duration: string
    bar_size: string
    num_blocks?: number
    contract_month?: string
  }) {
    const response = await apiClient.post('/api/v1/data/extract', params)
    return response.data
  },

  // Data query endpoints
  async getSymbols() {
    const response = await apiClient.get('/api/v1/data/symbols')
    return response.data
  },

  async getData(symbol: string, timeframe: string, limit: number = 100) {
    const response = await apiClient.get(`/api/v1/data/data/${symbol}`, {
      params: { timeframe, limit },
    })
    return response.data
  },

  async getTimeframes(symbol: string) {
    const response = await apiClient.get(`/api/v1/data/timeframes/${symbol}`)
    return response.data
  },
}

