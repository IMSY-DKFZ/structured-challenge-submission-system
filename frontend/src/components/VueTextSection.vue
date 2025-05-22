<template>
  <div class="mb-3 VueTextSection">
    <component :is="titleSize" v-if="$slots?.title" class="pb-1">
      <slot name="title"></slot>
    </component>
    <div class="py-2" v-if="$slots?.text">
      <slot name="text"></slot>
    </div>
    <div v-if="$slots?.default">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VueTextSection',
  props: {
    title: {
      typ: String,
      default: '',
    },
    highlight: {
      typ: Boolean,
      default: false,
    },
    titleSize: {
      typ: String,
      default: 'h3',
      validator(value) {
        return ['', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'].includes(value)
      },
    },
  },
}
</script>

<style scoped></style>
