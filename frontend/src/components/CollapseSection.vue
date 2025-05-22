<template>
  <button class="btn btn-outline-primary" type="button" data-bs-toggle="collapse" :data-bs-target="'#' + name + 'body'"
    aria-expanded="false" :aria-controls="name + 'body'">
    <i class="bi bi-info-circle pe-1"></i>
    {{ triggerBtn }}
  </button>

  <div class="collapse py-3" :id="name + 'body'">
    <div class="card card-body">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CollapseSection',
  props: {
    name: {
      typ: String,
      required: true,
    },
    triggerBtn: {
      typ: String,
      default: 'More Info',
    },
  },
}
</script>

<style scoped></style>
