import api, { setToken } from '@/api/axios'
import { useToastAlertStore } from '@/stores/toastAlert'
import { useAuthStore } from '@/stores/auth'

function apiErrorMessage(error) {
  const detail = error?.response?.data?.detail
  if (Array.isArray(detail)) {
    return detail
      .map((item) => item?.msg || item?.message || JSON.stringify(item))
      .filter(Boolean)
      .join('; ')
  }
  if (detail && typeof detail === 'object') {
    return detail.msg || detail.message || JSON.stringify(detail)
  }
  return detail || error?.message || 'Request failed'
}

async function apiPost(path, payload, headers, skipConnectionError) {
  let data
  // let errorText
  if (headers === undefined) {
    await api
      .post(`${path}`, payload)
      .then((response) => {
        data = response
      })
      .catch((error) => {
        data = error
        if (!skipConnectionError) throw new Error(apiErrorMessage(error))
      })
    return data.data
  } else {
    await api
      .post(`${path}`, payload, {
        headers: headers,
      })
      .then((response) => {
        if (response.data && response.data.name === 'AxiosError') {
          throw Error(response.toString())
        } else {
          data = response
        }
      })
      .catch((error) => {
        throw new Error(apiErrorMessage(error))
      })
    return data.data
  }
}
async function apiPut(path, payload, headers) {
  let data
  if (headers === undefined) {
    await api
      .put(`${path}`, payload)
      .then((response) => {
        data = response
      })
      .catch((error) => {
        data = error
        throw new Error(apiErrorMessage(error))
      })
    return data
  } else {
    await api
      .put(`${path}`, payload, {
        headers: headers,
      })
      .then((response) => {
        data = response
      })
      .catch((error) => {
        data = error
        throw new Error(apiErrorMessage(error))
      })
    return data.data
  }
}
async function apiDelete(path, payload) {
  let data
  await api
    .delete(`${path}`, payload)
    .then((response) => {
      data = response
    })
    .catch((error) => {
      data = error
      throw new Error(apiErrorMessage(error))
    })
  return data.data
}

async function apiGet(path, headers) {
  let data
  if (headers !== undefined) {
    await api
      .get(`${path}`, {
        headers: headers,
      })
      .then((response) => {
        data = response.data
      })
      .catch((error) => {
        data = error.response !== undefined ? connectionError(error) : error
        throw new Error(apiErrorMessage(error))
      })
  } else {
    await api
      .get(`${path}`)
      .then((response) => {
        data = response.data
      })
      .catch((error) => {
        data = error.response !== undefined ? connectionError(error) : error
        throw new Error(apiErrorMessage(error))
      })
  }
  return data
}
async function apiGetDownload(path, headers) {
  let data
  if (headers !== undefined) {
    await api
      .get(`${path}`, {
        headers: headers,
        responseType: 'blob',
      })
      .then((response) => {
        data = response
      })
      .catch((error) => {
        data = connectionError(error)
        throw new Error(error?.message)
      })
  } else {
    await api
      .get(`${path}`, { responseType: 'blob' })
      .then((response) => {
        data = response
      })
      .catch((error) => {
        data = connectionError(error)
        throw new Error(error?.message)
      })
  }
  return data
}

// TODO JWT TOKEN IN CONNECTIONERROR
let refresh = false
async function connectionError(error) {
  let data = error
  if (error.response.status === 401 && !refresh) {
    refresh = true
    setToken(localStorage.getItem('refreshToken'), localStorage.getItem('tokenType'))

    await apiPost('user/refresh_token')
      .then((resp) => {
        useAuthStore().setTokens(resp.access_token, resp.refresh_token, resp.token_type)
        setToken(resp.access_token, resp.token_type)
      })
      .catch((e) => {
        useToastAlertStore().showAlert('Your login has expired', 'danger')
        // useAuthStore().logOutUser()
        console.error(e)
      })
  }
  refresh = false
  return data
}

export { apiGet, apiPost, apiPut, apiDelete, apiGetDownload }
