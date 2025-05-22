<template>
  <header
    class="navbar sticky-top bg-light shadow-none flex-nowrap p-0 shadow px-3 px-md-4 d-md-none justify-content-end">
    <!-- <ConferencePeriod></ConferencePeriod> -->

    <button class="navbar-toggler d-md-none collapsed m-2 text-right" type="button" data-bs-toggle="collapse"
      data-bs-target="#sidebarMenu" aria-controls="sidebarMenu" aria-expanded="false" aria-label="Toggle navigation"
      @click="scrollTop">
      <span class="navbar-toggler-icon"></span>
    </button>

  </header>
  <!-- <ThemeSwitch /> -->
</template>

<style scoped></style>
<script setup>
import ConferencePeriod from '@/components/ConferencePeriod.vue'
import ThemeSwitch from '@/components/themeSwitch.vue'
</script>
<script>
export default {
  methods: {
    scrollTop() {
      window.scrollTo(0, 0)
    },
  },
}
</script>
<style scoped></style>
