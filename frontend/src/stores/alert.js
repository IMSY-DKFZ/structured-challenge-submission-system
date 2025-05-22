import { defineStore } from 'pinia'

export const useToastAlertStore = defineStore('alert', {
  state: () => {
    return {
      text: 'Hint',
      color: 'danger',
      alertState: false,
    }
  },
  actions: {
    showAlert(text = 'Something went wrong', color = 'danger') {
      this.text = text
      this.color = color
      this.alertState = true
      setTimeout(() => {
        this.alertState = false
      }, 2000)
    },
  },
})
