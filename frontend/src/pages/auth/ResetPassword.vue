<template>
  <ContentCard headline="Reset Password" subtitle="" :show-logo="false" :backlink="backlink" :showLinks="false">
    <BaseAlert :model-value="alert" @dismiss="dismissAlert" />

    <div class="">
      <p>Use this form to reset your password. Please enter the token that was sent to your email address. If you didn't
        receive the reset token, please visit the <router-link :to="{ name: 'Reset password request' }">reset
          password
          request</router-link> page.</p>

    </div>
    <VueForm @submit-event="reset" actionBtn="Reset password" name="reset-password-form" :actionBtnFullwidth="true">
      <VueInput label="Password reset token" type="text" :required="true" value="resetToken" v-model="resetToken">
      </VueInput>
      <VueInput label="New password" type="password-repeat" :required="true" text-min-length="8" v-model="password">
      </VueInput>
    </VueForm>
    <div class="text-center d-flex flex-column">
      <span class="pb-3 lh-1">If you are unable to recover your password, please <router-link
          :to="{ name: 'Contact' }">contact technical
          support</router-link>.</span>
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
import { getStaticUrl } from '@/helper/router-helper'

export default {
  name: 'ResetPassword',
  components: { VueForm, VueInput, ContentCard, BaseAlert },
  setup() {
    const { alert, showAlert, dismissAlert } = useAlert()
    return { alert, showAlert, dismissAlert }
  },
  data() {
    return {
      password: '',
      backlink: {
        to: { name: 'Login' },
        text: '← Login',
      },
      resetToken: this.$route.query.token ? this.$route.query.token : '',
    }
  },
  methods: {

    reset() {
      apiPost(
        'user/reset_password',
        {
          reset_token: this.resetToken,
          new_password: this.password,

        },
        {},
        true
      )
        .then(() => {
          const loginLink = getStaticUrl({ name: 'Login' })
          //           this.showAlert(
          //             `<p>Password updated successfully. You can now login with your new password.<p><div class="d-grid gap-2 col-6 mx-auto">
          // <a class="btn btn-primary" href="${loginLink}" role="button">Login page</a></div>`,
          //             'success',
          //             0
          //           )
          this.$router.push({ name: 'Login' })
          useToastAlertStore().showAlert('Password updated successfully. You can now login with your new password.', 'success', 6000);
        })
        .catch((error) => {
          this.showAlert(error.message, 'danger', 0)


        })
    },
  },
}
</script>

<style scoped></style>
