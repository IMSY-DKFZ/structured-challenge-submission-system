<template>
  <VueTextSection>
    <div class="row">
      <div class="row col-12 mb-3 p-3">
        <div class="col-12 col-md-4 mb-3">
          <h6 class="mb-0">Full name</h6>
          <div class="mb-3 opacity-75">{{ userData?.first_name }} {{ userData?.last_name }}</div>
        </div>
        <div class="col-12 col-md-4 mb-3">
          <h6 class="mb-0">Email address</h6>
          <div class="mb-3 opacity-75">{{ userData?.email }}</div>
        </div>
        <div class="col-12 col-md-4 mb-3">
          <h6 class="mb-0">Roles</h6>
          <div class="mb-3 opacity-75">
            <span v-for="role in userData?.roles" :key="role" class="badge text-bg-primary me-1">{{ role }}</span>
          </div>
        </div>


        <div class="col-12 col-md-4 mb-3">
          <h6 class="mb-0">Crated time</h6>
          <div class="mb-3 opacity-75 small">{{ StringToPrettyDate(userData?.created_time) }}</div>
        </div>
        <div class="col-12 col-md-4 mb-3">
          <h6 class="mb-0">Modified time</h6>
          <div class="mb-3 opacity-75 small">{{ StringToPrettyDate(userData?.modified_time) }}</div>
        </div>
        <div class="col-12 col-md-4 mb-3">
          <h6 class="mb-0">Last login</h6>
          <div class="mb-3 opacity-75 small">{{ StringToPrettyDate(userData?.last_login_time) }}</div>
        </div>
        <div class="col-12 col-md-4 mb-3">
          <h6 class="mb-0">Institution</h6>
          <div class="mb-3 opacity-75">{{ userData?.institution }}</div>
        </div>
        <div class="col-12 col-md-4 mb-3">
          <h6 class="mb-0">City</h6>
          <div class="mb-3 opacity-75">{{ userData?.city }}</div>
        </div>
        <div class="col-12 col-md-4 mb-3">
          <h6 class="mb-0">Country</h6>
          <div class="mb-3 opacity-75">{{ userData?.country }}</div>
        </div>
      </div>
    </div>
  </VueTextSection>
</template>

<script>
import VueTextSection from '@/components/VueTextSection.vue'
import { useAuthStore } from '@/stores/auth'
import StringToPrettyDate from '../../helper/format'
export default {
  name: 'Profile',
  components: { VueTextSection },
  data() {
    return {
      userData: useAuthStore().userData,
    }
  },
  methods: {
    StringToPrettyDate,
    useAuthStore,
  },
}
</script>

<style scoped></style>
