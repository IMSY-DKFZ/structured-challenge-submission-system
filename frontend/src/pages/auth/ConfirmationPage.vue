<template>
  <ContentCard :headline="headline" :subtitle="subTitle" :show-logo="false" :backlink="backlink" :showLinks="false">
    <BaseAlert :model-value="alert" @dismiss="dismissAlert" />
    <VueForm class="mt-4" @submitEvent="confirm" actionBtn="Confirm" name="confirm-form" :actionBtnFullwidth="true">
      <VueInput label="Confirmation Code" type="text" value="confirmationCode" :required="true"
        v-model="confirmationCode"></VueInput>
    </VueForm>
    <div class="text-center d-flex flex-column">
      <span><router-link class="text-decoration-underline" :to="{ name: 'Registration' }">Create an
          account</router-link> if
        you don't have one.</span>
    </div>
  </ContentCard>
</template>

<script>
import ContentCard from '@/components/ContentCard.vue'
import VueInput from '@/components/essentials/VueInput.vue'
import VueForm from '@/components/essentials/VueForm.vue'
import { apiPost } from '@/api/api'
import { useToastAlertStore } from '@/stores/toastAlert'
import BaseAlert from '@/components/BaseAlert.vue'
import { useAlert } from '@/composables/useAlert'
import { getStaticUrl } from '@/helper/router-helper'

export default {
  name: 'ConfirmationPage',
  components: { VueForm, VueInput, ContentCard, BaseAlert },
  setup() {
    const { alert, showAlert, dismissAlert } = useAlert()
    return { alert, showAlert, dismissAlert }
  },
  mounted() {
    this.headline = this.$route.query.headline ? this.$route.query.headline : this.headline
    this.subTitle = this.$route.query.subTitle ? this.subTitle : this.subTitle
    this.state = this.$route.query.state ? this.$route.query.state : this.state
  },
  data() {
    return {
      backlink: {
        to: { name: 'Login' },
        text: '← Login',
      },
      headline: 'Confirmation',
      confirmationCode: this.$route.query.code ? this.$route.query.code : '',
      subTitle: 'Please enter your personal token that we sent to your e-mail.',
      state: false,
    }
  },
  methods: {
    confirm() {
      apiPost(`/user/confirm_email/?confirmation_token=${this.confirmationCode}`, true)
        .then((response) => {
          //           const loginLink = getStaticUrl({ name: 'Login' })
          //           this.showAlert(
          //             `<p>Your account is now activated. Please log in.<p><div class="d-grid gap-2 col-6 mx-auto">
          // <a class="btn btn-primary" href="${loginLink}" role="button">Login page</a></div>`,
          //             'success',
          //             0
          //           )
          this.$router.push({ name: 'Login' })
          useToastAlertStore().showAlert('Your account is now activated. Please log in.', 'success', 6000);
        })
        .catch((error) => {
          this.showAlert(error, 'danger', 0)
        })
    },
  },
}
</script>

<style scoped></style>
