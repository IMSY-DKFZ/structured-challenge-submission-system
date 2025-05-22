<template>
  <VueForm @submit-event="updateProfilData" actionBtn="Update Profile" name="profile-form" :action-btn-fullwidth="false"
    :actionBtnFullwidth="true">
    <VueTextSection>
      <h4>User information</h4>
      <span class="opacity-75 small">(Fields you leave empty will not be updated)</span>
      <VueInput label="Bio" type="text" v-model="bio"></VueInput>
      <VueInput label="Titel" type="text" v-model="titel"></VueInput>
      <VueInput label="First Name" type="text" v-model="first_name"></VueInput>
      <VueInput label="Last name" type="text" v-model="last_name"></VueInput>
      <VueInput label="Country" type="text" v-model="country"></VueInput>
      <VueInput label="City" type="text" v-model="city"></VueInput>
      <VueInput label="Institution" type="text" v-model="institution"></VueInput>
      <VueInput label="Newsletter" type="checkbox" v-model="newsletter"></VueInput>
      <VueInput label="Website" type="text" v-model="website"></VueInput>
    </VueTextSection>
    <VueTextSection :highlight="true">
      <h4>Password update</h4>
      <VueInput label="New Password" type="password-repeat" v-model="password"></VueInput>
      <span>Please enter your current password if you want to change password:</span>

      <VueInput label="Current password" type="password" :required="password.length > 0" v-model="current_password">
      </VueInput>
    </VueTextSection>
  </VueForm>
</template>

<script>
import VueForm from '@/components/essentials/VueForm.vue'
import VueInput from '@/components/essentials/VueInput.vue'
import VueTextSection from '@/components/VueTextSection.vue'
import { apiPut } from '@/api/api'
import { useAuthStore } from '@/stores/auth'
import { useToastAlertStore } from '@/stores/toastAlert'

export default {
  name: 'EditProfile',
  components: { VueTextSection, VueForm, VueInput },
  data() {
    return {
      bio: '',
      city: '',
      country: '',
      first_name: '',
      institution: '',
      last_name: '',
      newsletter: false,
      password: '',
      titel: '',
      website: '',
      current_password: '',
    }

  },
  computed: {
    userData() {
      return useAuthStore().userData
    },
  },
  created() {
    const newObj = {}
    Object.entries(this.userData).forEach((item) => {
      const key = item[0]
      const value = item[1]
      Object.assign(newObj, { [key]: value })
    })
    Object.assign(this, newObj)
  },
  methods: {
    updateProfilData() {
      const formData = `?active_user_password=${encodeURIComponent(this.current_password)}`

      const noEmptyValues = Object.fromEntries(
        Object.entries({
          bio: this.bio,
          city: this.city,
          country: this.country,
          first_name: this.first_name,
          institution: this.institution,
          last_name: this.last_name,
          password: this.password,
          newsletter: this.newsletter.toString(),
          titel: this.titel,
          website: this.website,
        }).filter(([_, v]) => v !== null && v !== '')
      )
      apiPut('user/update' + formData, noEmptyValues)
        .then((resp) => {
          useToastAlertStore().showAlert('Your data has been updated', 'success')
          this.$router.push({ to: '/' })
          setTimeout(1000);
          location.reload();
        })
        .catch((e) => {
          useToastAlertStore().showAlert(e, 'danger', 6000)
        })
    },
  },
}
</script>

<style scoped></style>
