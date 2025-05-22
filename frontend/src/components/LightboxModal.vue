<template>
  <div style="cursor: pointer">
    <div @click="show">
      <slot></slot>
    </div>
    <div class="modal fade modal" :id="'lightboxModal' + id" tabindex="-1" :aria-labelledby="'lightboxModalLabel' + id"
      @click="close()">
      <div class="modal-dialog modal-dialog-centered modal-fullscreen">
        <div class="d-none d-md-flex justify-content-center w-100 p-5">
          <div class="w-75 bg-dark-subtle">
            <slot />
          </div>
        </div>
        <div class="d-flex d-block d-md-none justify-content-center w-100 p-3">
          <div class="w-100 bg-dark-subtle">
            <slot />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Modal } from 'bootstrap';
</script>
<script>
export default {
  name: 'LightboxModal',
  data() {
    return {
      modal: null,
      id: null,
    }
  },
  mounted() {
    this.id = Math.random()
  },
  methods: {
    show() {
      this.modal = new Modal(`#lightboxModal${this.id}`, { backdrop: true })
      this.modal.show()
    },
    close() {
      this.modal.hide()
    },
  },
}
</script>

<style scoped></style>
