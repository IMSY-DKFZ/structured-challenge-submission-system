<template>
  <div class="toast-container position-fixed bottom-0 end-0  end-0">
    <div id="toastLive" class="toast align-items-center bg-secondary-subtle border-0" role="alert" aria-live="assertive"
      aria-atomic="true">
      <div v-if="show" class="d-flex justify-content-between align-items-center align-content-center p-2 m-auto shadow">
        <div>Auto Saving Proposal...</div>
        <div class="spinner-border ms-auto" role="status" aria-hidden="true"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AutoSaveInterval',
  data() {
    return {
      intervalFunction: null,
      toast: null,
    }
  },
  props: {
    timeout: {
      typ: Number,
      required: true,
      validator(value) {
        return value > 1000
      },
    },
    show: {
      // this component is only a time trigger with UI,
      // we don't want to show autosave on false values.
      // So we don't show this toast
      typ: Boolean,
    },
  },
  methods: {},
  emits: ['endOfTimePeriod'],
  mounted() {
    const toastLive = document.getElementById('toastLive')

    // eslint-disable-next-line no-undef
    this.toast = bootstrap.Toast.getOrCreateInstance(toastLive)
    this.intervalFunction = setInterval(() => {
      this.toast.show()
      this.$emit('endOfTimePeriod')
    }, this.timeout)
  },
  beforeUnmount() {
    clearInterval(this.intervalFunction)
  },
}
</script>

<style scoped></style>
