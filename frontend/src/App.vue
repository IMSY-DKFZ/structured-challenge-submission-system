<script setup>
import { RouterView } from 'vue-router'
import CookieBanner from '@/components/CookieBanner.vue'
import { useColorStore } from '@/stores/colorMode'
import AlertModal from '@/components/AlertModal.vue'
import ToastAlert from '@/components/ToastAlert.vue'
useColorStore().setPreferredTheme()
</script>

<template>
  <CookieBanner />
  <ToastAlert />
  <Alert-modal />
  <RouterView />

</template>

<style scoped></style>
