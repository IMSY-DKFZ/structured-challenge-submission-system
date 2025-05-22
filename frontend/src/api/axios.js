import axios from 'axios'
const AUTH_TOKEN = localStorage.getItem('accessToken')
const TYP_TOKEN = localStorage.getItem('tokenType')

export const api = axios.create({
  baseURL: 'https://www.biomedical-challenges.org/api/v2/',
  // baseURL: 'http://localhost:5000/api/v2',
  headers: {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    scheme: 'https',
  },
})
if (AUTH_TOKEN && TYP_TOKEN) {
  setToken(AUTH_TOKEN, TYP_TOKEN)
}

export function setToken(AUTH_TOKEN, TYP_TOKEN) {
  api.defaults.headers.common['Authorization'] = TYP_TOKEN + ' ' + AUTH_TOKEN
}

export default api
