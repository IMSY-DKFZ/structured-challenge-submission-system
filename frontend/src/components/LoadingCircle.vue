<template>
  <div
    class="text-center my-5"
    v-if="activated">
    <div
      class="spinner-border"
      role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoadingCircle',
  props: {
    activated: {
      typ: Boolean,
    },
  },
  data() {
    return {
      userAcceptedCookies: false,
    }
  },
}
</script>

<style scoped></style>
