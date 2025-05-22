<template>
  <ContentCard headline="Login" :show-logo="false" :backlink="backlink" :showLinks="false">
    <BaseAlert :model-value="alert" @dismiss="dismissAlert" />
    <VueForm @submitEvent="login" actionBtn="Login" name="login-form" :actionBtnFullwidth="true">
      <VueInput label="Email" type="email" :required="true" v-model="email"></VueInput>
      <VueInput label="Password" type="password" :required="true" v-model="password"></VueInput>
      <div class="text-end pb-3"><router-link class="link-secondary" :to="{ name: 'Reset password request' }">Forget
          password?</router-link></div>
    </VueForm>

    <div class="text-center d-flex flex-column">
      <router-link class="text-decoration-underline" :to="{ name: 'Registration' }">Create an account</router-link>
      <router-link :to="{
        // query: {
        //   code: 'SubTitle',
        // },
        name: 'ConfirmationPage',
      }" class="text-decoration-underline">Activate your account</router-link>
      <!-- <router-link class="link-secondary " :to="{ name: 'SubmissionSystem' }" @click="noAccount">Continue
        without
        Account <i class="bi bi-arrow-right"></i></router-link> -->

    </div>
  </ContentCard>
</template>

<script setup></script>
<script>
import ContentCard from '@/components/ContentCard.vue'
import VueForm from '@/components/essentials/VueForm.vue'
import VueInput from '@/components/essentials/VueInput.vue'
import { useAuthStore } from '@/stores/auth'
// import { useToastAlertStore } from '@/stores/toastAlert'
import BaseAlert from '@/components/BaseAlert.vue'
import { useAlert } from '@/composables/useAlert'

export default {
  name: 'LoginPage',
  components: { VueForm, VueInput, ContentCard, BaseAlert },
  setup() {
    const { alert, showAlert, dismissAlert } = useAlert()
    return { alert, showAlert, dismissAlert }
  },
  data() {
    return {
      email: '',
      password: '',
      backlink: {
        to: { name: 'SubmissionSystem' },
        text: '← Return to Submission System',
      },
    }
  },
  mounted() {
    useAuthStore().clearTokens()
  },
  methods: {
    noAccount() {
      useAuthStore().clearTokens()
    },
    async login() {
      await useAuthStore()
        .logInUser(this.password, this.email)
        .then((success) => {
          if (success) {
            this.showAlert('Login successful. Redirecting to Submission System...', 'success', 0)
            setTimeout(2000);
            this.$router.push({ name: 'Workflow' })
          }
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
