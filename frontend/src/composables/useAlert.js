// src/composables/useAlert.js
import { ref, onBeforeUnmount } from 'vue'

export function useAlert() {
  const alert = ref({
    show: false,
    type: 'success',
    message: '',
    timeout: null,
  })

  const showAlert = (message, type = 'success', duration = 6000) => {
    // Clear any existing timeout
    if (alert.value.timeout) {
      clearTimeout(alert.value.timeout)
    }

    // Set alert data
    alert.value.show = true
    alert.value.type = type
    alert.value.message = message // Can now contain HTML

    // Auto-dismiss after duration if duration > 0
    if (duration > 0) {
      alert.value.timeout = setTimeout(() => {
        dismissAlert()
      }, duration)
    }
  }

  const dismissAlert = () => {
    alert.value.show = false
    alert.value.message = ''
    if (alert.value.timeout) {
      clearTimeout(alert.value.timeout)
      alert.value.timeout = null
    }
  }

  // Cleanup function
  onBeforeUnmount(() => {
    if (alert.value.timeout) {
      clearTimeout(alert.value.timeout)
    }
  })

  return {
    alert,
    showAlert,
    dismissAlert,
  }
}