<template>
  <div>
    <div class="modal fade" id="alertModal" tabindex="-1" aria-labelledby="alertModalLabel">
      <div class="modal-dialog">
        <div :class="`alert alert-${color}`" role="alert">
          {{ text }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { watch } from 'vue'
import { useToastAlertStore } from '@/stores/alert'
import { Modal } from 'bootstrap';

const alertStore = useToastAlertStore()
const { text, color } = storeToRefs(alertStore)
const { alertState } = storeToRefs(alertStore)

let modal = null
watch(alertState, (state) => {
  if (state) {
    modal = new Modal('#alertModal', { backdrop: false })
    modal.show()
  } else {
    if (modal) {
      modal.hide()
      modal = null
    }
  }
})
</script>
<script>
export default {
  name: 'AlertModal',
  props: {
    title: {
      typ: String,
      default: 'Warning',
    },
    text: {
      typ: String,
      default: 'This action can not be undone, are you sure you want to continue?',
    },
    abortBtn: {
      typ: String,
      default: 'Abort',
    },
    acceptBtn: {
      typ: String,
      default: 'Accept',
    },
  },
}
</script>

<style scoped></style>
