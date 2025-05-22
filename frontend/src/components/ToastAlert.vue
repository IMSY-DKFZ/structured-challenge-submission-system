<template>
    <div class="fixed-top" aria-live="polite" aria-atomic="true">
        <div class="toast-container p-2 top-0 start-50 translate-middle-x">
            <div id="alertToast" :class="['toast', 'align-items-center', 'text-white', `bg-${color}`]"
                style="--bs-bg-opacity: 0.95" role="alert">
                <div class="d-flex">
                    <div class="toast-body fs-6 flex-fill text-center" v-html="text"></div>
                    <!-- <button type="button" class="btn-close btn-close-white me-2 m-auto" @click="hideToast"
                        aria-label="Close">
                    </button> -->
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { watch, onMounted, onUnmounted } from 'vue'
import { useToastAlertStore } from '@/stores/toastAlert'
import { Toast } from 'bootstrap'

const toastAlertStore = useToastAlertStore()
const { text, color, duration, toastAlertState, toastId, isActive } = storeToRefs(toastAlertStore)

let toastInstance = null

const showToast = () => {

    if (toastInstance) {
        toastInstance = null
    }

    const toastEl = document.getElementById('alertToast')
    if (toastEl) {
        toastInstance = new Toast(toastEl, {
            autohide: true,
            delay: duration.value,
        })

        // Remove any existing event listeners
        toastEl.removeEventListener('hidden.bs.toast', hideToast)
        toastEl.addEventListener('hidden.bs.toast', hideToast)
        toastInstance.show()
    } else {
        console.error('Toast element not found!')
    }
}

const hideToast = () => {
    if (toastInstance) {
        toastInstance = null
    }
    toastAlertStore.hideAlert()
}

// Initialize toast when component is mounted
onMounted(() => {
    const toastEl = document.getElementById('alertToast')
    if (toastEl) {
        toastInstance = new Toast(toastEl)
    }
})

// Watch for changes and show toast
watch(
    [toastAlertState, toastId],
    ([newState, newId]) => {
        if (newState) {
            showToast()
        }
    },
    { immediate: true }
)

// Cleanup on unmount
onUnmounted(() => {
    if (toastInstance) {
        toastInstance = null
    }
})
</script>
