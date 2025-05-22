// stores/toastAlert.js
import { defineStore } from 'pinia'

export const useToastAlertStore = defineStore('alert-toast', {
  state: () => ({
    text: '',
    color: 'success',
    duration: 3000,
    toastAlertState: false,
    toastId: 0,
    isActive: false,
  }),

  actions: {
    showAlert(text = 'Something went wrong', color = 'success', duration = 3000) {
      // console.log('showAlert called with:', { text, color, duration, isActive: this.isActive })

      // Reset the state if there's an existing active toast
      if (this.isActive) {
        this.hideAlert()
      }

      this.text = text
      this.color = color
      this.duration = duration
      this.toastId++
      this.isActive = true
      this.toastAlertState = true

      // Auto-hide after duration
      setTimeout(() => {
        this.hideAlert()
      }, duration + 100) // Add small buffer to ensure toast completes
    },

    hideAlert() {
      // console.log('hideAlert called, resetting state')
      this.toastAlertState = false
      this.isActive = false
    },
  },
})
