<!-- src/components/BaseAlert.vue -->
<template>
  <div v-if="modelValue.show" :class="`alert alert-${modelValue.type} alert-dismissible fade show my-3`" role="alert">
    <span v-html="modelValue.message"></span>
    <button type="button" class="btn-close" @click="$emit('dismiss')" aria-label="Close">
    </button>
  </div>
</template>

<script>
export default {
  name: 'BaseAlert',
  props: {
    modelValue: {
      type: Object,
      required: true
    }
  },
  emits: ['dismiss']
}
</script>

<style scoped>
.alert {
  margin-bottom: 1rem;
}
</style>