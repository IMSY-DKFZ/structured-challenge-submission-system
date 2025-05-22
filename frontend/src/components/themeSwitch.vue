<template>
  <div class="clearfix">
    <button type="button" class="btn btn-primary text-nowrap bg-danger-subtle m-2 float-right shadow" :class="[
      useColorStore().getOppositeColorMode === 'Light'
        ? ' bg-dark-subtle text-light'
        : 'bg-light-subtle  text-dark',
    ]" @click="useColorStore().switchColorMode()">
      <i class="bi bi-sun pe-1" style="color: yellow" v-if="useColorStore().getOppositeColorMode === 'Light'"></i>
      <i class="bi bi-moon pe-1" style="color: darkblue" v-else></i>
      <!-- <span>{{ useColorStore().getOppositeColorMode }}</span> -->
    </button>
  </div>
</template>

<script setup>
import { useColorStore } from '@/stores/colorMode'
</script>

<style scoped></style>
