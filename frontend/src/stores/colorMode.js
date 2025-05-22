import { defineStore } from 'pinia'

export const useColorStore = defineStore('color', {
  state: () => {
    return {
      colorMode: 'dark',
      isDarkTheme: true,
    }
  },
  getters: {
    getColorMode: (state) => state.colorMode.slice(0, 1).toUpperCase() + state.colorMode.slice(1),
    getOppositeColorMode: (state) =>
      (state.colorMode === 'light' ? 'dark' : 'light').slice(0, 1).toUpperCase() +
      (state.colorMode === 'light' ? 'dark' : 'light').slice(1),
  },
  actions: {
    setTheme(mode) {
      this.colorMode = mode
      this.isDarkTheme = mode === 'dark';
      document.documentElement.setAttribute('data-bs-theme', mode)
      document.documentElement.setAttribute('color-scheme', mode)
      document.documentElement.setAttribute('prefers-color-scheme', mode)
      localStorage.setItem('theme', mode)
    },
    switchColorMode() {
      this.setTheme(this.colorMode === 'light' ? 'dark' : 'light')
    },
    setPreferredTheme() {
      this.colorMode = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
      this.isDarkTheme = this.colorMode === 'dark';
      if (localStorage.getItem('theme')) {
        this.setTheme(localStorage.getItem('theme'))
      } else {
        this.setTheme(this.colorMode)
      }
      // this.setTheme('light')
    },
  },
})
