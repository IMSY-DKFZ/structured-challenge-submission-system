import { defineStore } from 'pinia'
import { apiGet, apiPost } from '@/api/api'
import { useToastAlertStore } from '@/stores/toastAlert'
import router from '../router/index'
import { setToken } from '@/api/axios'

//'organizer', 'subAdmin', 'admin'
export const useAuthStore = defineStore('auth', {
  state: () => {
    return {
      role: '',
      isLoggedIn: false,
      roles: [],
      userData: {},
      institution: '',
      country: '',
      city: '',
      tokenType: '',
    }
  },

  persist: {
    storage: sessionStorage, // data in sessionStorage is cleared when the page session ends.
  },
  getters: {
    getUserData: (state) => state.userData,
    getUserRole: (state) => state.role,
    getUserRoles: (state) => state.roles,
    getUserLoginState: (state) => state.isLoggedIn,
    adminOnly(state) {
      return state.role === 'admin' && localStorage.getItem('accessToken') !== ''
    },
    adminSubOnly(state) {
      return (
        ['admin', 'subadmin'].includes(state.role) && localStorage.getItem('accessToken') !== ''
      )
    },
    getUserName: (state) =>
      state.userData?.first_name + ' ' + state.userData?.last_name
        ? state.userData?.first_name + ' ' + state.userData?.last_name
        : state.userData?.email,
  },
  actions: {
    setUserData(data) {
      this.userData = data
    },
    setUserRole(role) {
      this.role = role
    },
    setUserRoles(roles) {
      this.roles = roles
    },
    async getAndSetUserDataMe() {
      await apiGet('user/me/', {
        accept: 'application/json',
        Authorization:
          localStorage.getItem('tokenType') + ' ' + localStorage.getItem('accessToken'),
      })
        .then((data) => {
          if (data.toString().includes('Error')) {
            new Error(data)
          } else {
            this.setUserRole(data.roles[0] ? data.roles[0].toLowerCase() : '')
            this.setUserRoles(data.roles ? data.roles.map((x) => x.toLowerCase()) : [])
            this.setUserData(data)
            this.isLoggedIn = true
          }
        })
        .catch((e) => {
          setTimeout(1000);
          useToastAlertStore().showAlert(e, 'danger', 6000)
        })
    },
    setTokens(access, refresh, typ) {
      localStorage.setItem('accessToken', JSON.parse(JSON.stringify(access)))
      localStorage.setItem('refreshToken', JSON.parse(JSON.stringify(refresh)))
      localStorage.setItem('tokenType', JSON.parse(JSON.stringify(typ)))
      this.accessToken = JSON.stringify(access)
      this.refreshToken = JSON.stringify(refresh)
      this.tokenType = JSON.stringify(typ)
    },
    clearTokens() {
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      localStorage.removeItem('tokenType')
      localStorage.removeItem('auth')
      sessionStorage.clear()
      this.role = ''
      this.isLoggedIn = false
      this.roles = []
      this.userData = {}
      this.accessToken = ''
      this.refreshToken = ''
      this.tokenType = ''
    },
    async logInUser(password, email) {
      this.clearTokens()
      return new Promise((resolve, reject) => {
        this.isLoggedIn = false
        const loginString = `grant_type=&username=${encodeURIComponent(
          email
        )}&password=${encodeURIComponent(password)}&grant_type=password&scope=&client_id=&client_secret=`

        apiPost(
          'user/token',
          loginString,
          {
            accept: 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          true
        )
          .then(async (response) => {
            await this.setTokens(response.access_token, response.refresh_token, response.token_type)
            await setToken(response.access_token, response.token_type)
            await this.getAndSetUserDataMe()
              .then((resp) => {
                if (resp !== undefined) throw new Error('DAA')
                resolve(true)
                this.isLoggedIn = true
              })
              .catch((e) => {
                setTimeout(1000);
                useToastAlertStore().showAlert(e, 'danger', 6000)
                reject(new Error(e))
              })
          })
          .catch((e) => {
            setTimeout(1000);
            useToastAlertStore().showAlert(e, 'danger', 6000)
            reject(new Error(e))
          })
      })
    },
    logOutUser() {
      apiPost(
        'user/logout',
        {
          access_token: localStorage.getItem('accessToken'),
          refresh_token: localStorage.getItem('refreshToken'),
          token_type: localStorage.getItem('tokenType'),
        },
        {
          accept: 'application/json',
          'Content-Type': 'application/json',
        },
        {}
      )
        .then((response) => {
          if (response.data) {
            this.isLoggedIn = false
            this.role = ''
            this.roles = []
          }
        })
        .catch((error) => {
          console.log('error', error)
        })
        .finally(() => {
          this.clearTokens()
          router.push({ name: 'Workflow' })
        })
    },
  },
})
