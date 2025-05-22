<template>
  <div class="py-2 d-grid gap-2 mx-auto" role="group"
    :class="[userRole.length > 2 ? 'btn-group-vertical' : 'btn-group ']" aria-label="Basic example">
    <!-- <button v-for="role in userRoles" :key="role" :disabled="userRoles.length === 1" type="button"
      @click="setUserRole(role)" class="btn btn-sm btn-outline-dark bg-body-rounded shadow text-wrap"
      :class="[{ active: userRole === role }]"> -->
    <button v-for="role in userRoles" :key="role" :disabled="userRoles.length === 1" type="button"
      @click="setUserRole(role)" class="btn btn-sm shadow text-wrap active"
      :class="[{ active: userRole === role }, isDarkTheme ? 'btn-outline-light bg-body-rounded' : 'btn-outline-dark bg-body-rounded']">
      {{ role.toUpperCase() }}
    </button>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth'
import { useColorStore } from '@/stores/colorMode';

export default {
  computed: {
    userRoles() {
      return useAuthStore().getUserRoles
    },
    userRole() {
      return useAuthStore().getUserRole
    },
    isDarkTheme() {
      const colorStore = useColorStore();
      return colorStore.isDarkTheme
    },
  },
  methods: {
    setUserRole(role) {
      useAuthStore().setUserRole(role)
      if (
        this.$router.currentRoute.value.meta.access.length > 0 &&
        !this.$router.currentRoute.value.meta.access.includes(role)
      ) {
        this.$router.push({ name: 'SubmissionSystem' })
      }
    },
  },
}
</script>

<style scoped></style>
