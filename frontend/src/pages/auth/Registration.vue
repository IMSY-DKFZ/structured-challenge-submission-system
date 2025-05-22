<template>
  <ContentCard headline="Registration" :backlink="backlink" :show-logo="false" :showLinks="false"
    subtitle="Please read the privacy policy and the data protection policy below carefully!">
    <BaseAlert :model-value="alert" @dismiss="dismissAlert" />
    <VueForm actionBtn="Create Account" name="registration-form" :actionBtnFullwidth="true" @submit-event="register">
      <VueInput label="First name" type="text" :required="true" v-model="firstName"></VueInput>
      <VueInput label="Last name" type="text" :required="true" v-model="lastName"></VueInput>
      <VueInput label="Email" type="email" :required="true" v-model="email"></VueInput>
      <VueInput label="Password" type="password-repeat" :required="true" text-min-length="8" v-model="password">
      </VueInput>
      <VueInput
        label="I agree that I will be registered to the MICCAI submission system for biomedical challenges. In addition, I agree that my personal and challenge proposal data will be used for the purposes described above."
        type="checkbox" :required="true" v-model="readAgreement"></VueInput>
    </VueForm>
    <div class="text-center  d-flex flex-column">
      <router-link class="text-decoration-underline" :to="{ name: 'Login' }">You have an Account? Login</router-link>
      <router-link class="text-decoration-underline" :to="{ name: 'ConfirmationPage' }">Activate your
        account</router-link>
    </div>
  </ContentCard>
</template>

<script>
import ContentCard from '@/components/ContentCard.vue'
import { apiGet, apiPost } from '@/api/api.js'

import VueInput from '@/components/essentials/VueInput.vue'
import VueForm from '@/components/essentials/VueForm.vue'
import { useToastAlertStore } from '@/stores/toastAlert'
import BaseAlert from '@/components/BaseAlert.vue'
import { useAlert } from '@/composables/useAlert'

export default {
  name: 'RegistrationPage',
  components: { VueForm, VueInput, ContentCard, BaseAlert },
  setup() {
    const { alert, showAlert, dismissAlert } = useAlert()
    return { alert, showAlert, dismissAlert }
  },
  data() {
    return {
      backlink: {
        to: { name: 'SubmissionSystem' },
        text: '← Return to Submission System',
      },
      firstName: '',
      lastName: '',
      password: '',
      email: '',
      readAgreement: false,
    }
  },
  mounted() {
    apiGet('health', {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
      },
    })
  },
  methods: {
    register() {
      apiPost(
        'user/create',
        {
          first_name: this.firstName,
          last_name: this.lastName,
          password: this.password,
          email: this.email,
        },
        {},
        true
      )
        .then(() => {
          this.$router.push({ name: 'SubmissionSystem' })
          useToastAlertStore().showAlert('Your registration has been successful, please check your email for the activation steps.', 'success', 6000);
        })
        .catch((error) => {
          this.showAlert(error.message, 'danger', 0)
        })
    },
  },
  watch: {
    email(newVal) {
      this.email = this.email.toLowerCase()
    }
  },
}
</script>

<style scoped></style>
