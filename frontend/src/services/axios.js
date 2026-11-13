import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const ACCESS_KEY = 'access_token'
const REFRESH_KEY = 'refresh_token'

export const guardarTokens = ({ access, refresh }) => {
  if (access) localStorage.setItem(ACCESS_KEY, access)
  if (refresh) localStorage.setItem(REFRESH_KEY, refresh)
}

export const cerrarSesion = () => {
  localStorage.removeItem(ACCESS_KEY)
  localStorage.removeItem(REFRESH_KEY)
}

export const haySesion = () => !!localStorage.getItem(REFRESH_KEY)

const api = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem(ACCESS_KEY)
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

let renovando = null // evita pedir varios refresh a la vez

const renovarAccess = async () => {
  const refresh = localStorage.getItem(REFRESH_KEY)
  if (!refresh) throw new Error('No hay refresh token')

  const { data } = await axios.post(`${API_URL}/token/refresh/`, { refresh })
  guardarTokens(data)
  return data.access
}

// si el access token venció (401), lo renueva y repite la petición original
api.interceptors.response.use(
  (respuesta) => respuesta,
  async (error) => {
    const original = error.config
    const esPeticionDeToken = original?.url?.includes('/token/')

    if (
      error.response?.status === 401 &&
      !original._reintentado &&
      !esPeticionDeToken &&
      haySesion()
    ) {
      original._reintentado = true
      try {
        renovando = renovando || renovarAccess().finally(() => (renovando = null))
        const nuevoAccess = await renovando
        original.headers.Authorization = `Bearer ${nuevoAccess}`
        return api(original)
      } catch (e) {
        // el refresh también venció: la sesión terminó de verdad
        cerrarSesion()
        window.location.href = '/login'
        return Promise.reject(e)
      }
    }

    return Promise.reject(error)
  },
)

export default api