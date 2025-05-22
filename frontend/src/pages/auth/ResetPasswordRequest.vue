<template>
  <ContentCard headline="Reset Password Request" subtitle="" :show-logo="false" :backlink="backlink" :showLinks="false">
    <BaseAlert :model-value="alert" @dismiss="dismissAlert" />
    <div class="pb-3">Using this form you can request a password reset. Please provide your email address.
      If the data
      matches our records, you will receive a mail with further instructions. If you are unable to recover your
      password, please <router-link :to="{ name: 'Contact' }">contact technical support</router-link>.</div>
    <VueForm @submit-event="resetRequest" actionBtn="Reset password request" name="reset-password-form"
      :actionBtnFullwidth="true">
      <VueInput label="Email" type="email" :required="true" v-model="email"></VueInput>
    </VueForm>
    <div class="text-center d-flex flex-column">

      <span class="pb-3 lh-1">If you have received password reset token via e-mail, you can complete the process at
        <router-link :to="{ name: 'Reset password' }">reset password</router-link> page.</span>
      <span><router-link class="text-decoration-underline" :to="{ name: 'Registration' }">Create an
          account</router-link> if
        you don't have one.</span>
    </div>
  </ContentCard>
</template>

<script>
import ContentCard from '@/components/ContentCard.vue'
import VueForm from '@/components/essentials/VueForm.vue'
import VueInput from '@/components/essentials/VueInput.vue'
import { apiPost } from '@/api/api.js'
import { useToastAlertStore } from '@/stores/toastAlert'
import BaseAlert from '@/components/BaseAlert.vue'
import { useAlert } from '@/composables/useAlert'

export default {
  name: 'ResetPassword',
  components: { VueForm, VueInput, ContentCard, BaseAlert },
  setup() {
    const { alert, showAlert, dismissAlert } = useAlert()
    return { alert, showAlert, dismissAlert }
  },
  data() {
    return {
      email: '',
      backlink: {
        to: { name: 'Login' },
        text: '← Login',
      },
    }
  },
  methods: {
    resetRequest() {
      apiPost(`user/reset_password_request?email=${this.email}`)
        .then(() => {
          // this.showAlert('A new password has been requested. Instructions have been sent to your e-mail address.', 'success', 0)
          this.$router.push({ name: 'SubmissionSystem' })
          useToastAlertStore().showAlert('A new password has been requested. Instructions have been sent to your e-mail address.', 'success', 6000);
        })
        .catch((error) => {
          this.showAlert(error.message, 'danger', 0)
        })
    },
  },
}
</script>

<style scoped></style>
