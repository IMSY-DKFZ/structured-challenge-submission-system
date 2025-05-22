<template>
  <popup-modal ref="popup">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ title }}</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="_cancel"></button>
        </div>
        <div class="modal-body lh-sm py-3">
          <p>{{ message }}</p>
          <!-- New password input field -->
          <div v-if="showPasswordInput" class="form-group">
            <p><label for="password">Enter Your Password:</label></p>
            <input type="password" v-model="password" class="form-control" id="password" required>
          </div>
          <slot></slot>
        </div>
        <div class="modal-footer gap-2">
          <button type="button" class="btn btn-secondary" @click="_cancel">
            {{ cancelButton }}
          </button>
          <button type="button" v-if="okButton" class="btn" :class="okButtonTheme" @click="_confirm">
            {{ okButton }}
          </button>
        </div>
      </div>
    </div>
  </popup-modal>
</template>

<script>
import PopupModal from './PopupModal.vue'

export default {
  name: 'ConfirmDialogue',

  components: { PopupModal },

  data: () => ({
    title: undefined,
    message: undefined,
    okButton: undefined,
    okButtonTheme: undefined,
    cancelButton: 'Close',
    showPasswordInput: false, // Flag to show/hide password input
    password: '', // bind this to the password input


    // Private variables
    resolvePromise: undefined,
    rejectPromise: undefined,
  }),

  methods: {
    show(opts = {}) {
      this.title = opts.title
      this.message = opts.message
      this.okButton = opts.okButton
      this.okButtonTheme = opts.okButtonTheme || 'btn-primary'
      this.showPasswordInput = opts.showPasswordInput || false; // Set the flag
      if (opts.cancelButton) {
        this.cancelButton = opts.cancelButton
      }
      // Once we set our config, we tell the popup modal to open
      this.$refs.popup.open()
      // Return promise so the caller can get results
      return new Promise((resolve, reject) => {
        this.resolvePromise = resolve
        this.rejectPromise = reject
      })
    },

    _confirm() {
      this.$refs.popup.close()
      this.resolvePromise(this.showPasswordInput ? this.password : true);
    },

    _cancel() {
      this.$refs.popup.close()
      this.resolvePromise(false)
    },
  },
}
</script>

<style scoped>
.modal-header .btn-close {
  padding: 0.5rem 0.5rem;
  margin: -0.5rem -0.5rem -0.5rem auto;
}

.popup-modal {
  z-index: 999
}
</style>
