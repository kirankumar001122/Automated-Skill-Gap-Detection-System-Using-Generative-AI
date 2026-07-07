import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Create axios instance with default configuration
const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  timeout: 180000, // 180 seconds timeout (3 minutes) for multi-agent workflows
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`)
    return config
  },
  (error) => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log(`Response received from ${response.config.url}:`, response.status)
    return response
  },
  (error) => {
    console.error('Response error:', error)
    
    if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
      throw new Error('Request timed out. The multi-agent workflow is taking longer than expected. Please try again or simplify your request.')
    }
    
    if (error.response) {
      // Server responded with error status
      const message = error.response.data?.detail || error.response.statusText || 'Server error'
      throw new Error(message)
    } else if (error.request) {
      // Request was made but no response received
      throw new Error('Unable to connect to the server. Please check if the backend is running.')
    } else {
      // Something else happened
      throw new Error(error.message || 'An unexpected error occurred')
    }
  }
)

// Types for API responses
export interface TaskRequest {
  prompt: string
  language?: string
  context?: string
}

export interface TaskResponse {
  task_id: string
  status: string
  generated_code?: string
  execution_result?: {
    success: boolean
    output: string
    error?: string
    execution_time: number
  }
  explanation?: string
  optimization_suggestions?: string[]
  test_results?: any[]
  agent_tasks?: any[]
  created_at: string
  completed_at?: string
}

export interface CodeExecutionResult {
  success: boolean
  status: string
  output: string
  compilation_output?: string
  runtime_output?: string
  error?: string
  execution_time: number
}

// API functions
export const generateCode = async (request: TaskRequest): Promise<TaskResponse> => {
  const response = await api.post('/generate-code', request)
  return response.data
}

export const debugCode = async (code: string, language: string = 'python'): Promise<TaskResponse> => {
  const response = await api.post('/debug-code', { code, language })
  return response.data
}

export const runCode = async (code: string, language: string = 'python', input_data?: string): Promise<CodeExecutionResult> => {
  const response = await api.post('/run-code', { code, language, input_data })
  return response.data
}

export const optimizeCode = async (code: string, language: string = 'python'): Promise<TaskResponse> => {
  const response = await api.post('/optimize-code', { code, language })
  return response.data
}

export const explainCode = async (code: string, language: string = 'python'): Promise<TaskResponse> => {
  const response = await api.post('/explain-code', { code, language })
  return response.data
}

export const getTaskStatus = async (taskId: string): Promise<TaskResponse> => {
  const response = await api.get(`/task/${taskId}`)
  return response.data
}

export const getAgentLogs = async (taskId?: string, limit: number = 50): Promise<any> => {
  const params = taskId ? { task_id: taskId, limit } : { limit }
  const response = await api.get('/logs', { params })
  return response.data
}

export const getAvailableModels = async (): Promise<{ models: string[] }> => {
  const response = await api.get('/models')
  return response.data
}

export const healthCheck = async (): Promise<{ status: string; service: string }> => {
  const response = await api.get('/health')
  return response.data
}

export default api
