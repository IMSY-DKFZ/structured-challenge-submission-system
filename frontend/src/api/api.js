import api, { setToken } from '@/api/axios'
import { useToastAlertStore } from '@/stores/toastAlert'
import { useAuthStore } from '@/stores/auth'

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
        if (!skipConnectionError) throw new Error(error?.response.data.detail || error?.message)
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
        if (
          error?.response?.data?.detail[0].msg !== undefined &&
          error?.response?.data?.detail[0].msg.toString().includes('password')
        ) {
          throw new Error(error?.response?.data?.detail[0].msg || error?.message)
        }
        if (skipConnectionError) {
          throw new Error(error?.response.data.detail || error?.message)
        } else {
          throw new Error(error?.response.data.detail || error?.message)
        }
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
        throw new Error(error?.response?.data.detail || error?.message)
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
        throw new Error(error?.response?.data.detail || error?.message)
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
      throw new Error(typeof error?.response.data.detail == "string" ? error?.response.data.detail : error?.message)
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
        let errorMessage =
          error.response !== undefined ? error?.response.data.detail : error?.message
        throw new Error(errorMessage)
      })
  } else {
    await api
      .get(`${path}`)
      .then((response) => {
        data = response.data
      })
      .catch((error) => {
        data = error.response !== undefined ? connectionError(error) : error
        let errorMessage =
          error.response !== undefined ? error?.response.data.detail : error?.message
        throw new Error(errorMessage)
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
