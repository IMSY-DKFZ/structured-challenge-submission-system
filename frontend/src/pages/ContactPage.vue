<template>
  <div>
    <VueTextSection>
      <template #text>
        Please check the <router-link :to="{ name: 'FAQ' }">FAQ</router-link> first. Your question might be listed
        there.
        If you are still missing
        your solution, please contact us! If you have general questions, please choose MICCAI
        challenge chairs as recipient. For technical questions (regarding the submission system
        itself), choose technical support.
      </template>
    </VueTextSection>
    <VueForm :action-btn-fullwidth="false" action-btn="Send" name="contact" @submit="submitEmail">
      <VueInput v-model="contactFormData.sender_name" type="text" label="Your name" icon="person" :required="true">
      </VueInput>
      <VueInput v-model="contactFormData.sender_email" type="email" label="Your email address" icon="envelope"
        :required="true">
      </VueInput>
      <VueInput v-model="contactFormData.subject" type="text" label="Subject" icon="file-earmark" :required="true">
      </VueInput>
      <VueInput v-model="contactFormData.recipients_group" type="select"
        :options="['Technical support', 'Challenge chairs']" label="Recipient" icon="person-rolodex" :required="true">
      </VueInput>
      <VueInput v-model="contactFormData.message" type="textarea" text-max-length="2000"
        label="Your Message <small>(2000 character max.)</small>" icon="pen" :required="true">
      </VueInput>
    </VueForm>
  </div>
</template>

<script>
import VueForm from '@/components/essentials/VueForm.vue'
import VueInput from '@/components/essentials/VueInput.vue'
import VueTextSection from '@/components/VueTextSection.vue'
import { apiPost } from '@/api/api'
import { useToastAlertStore } from '@/stores/toastAlert'

export default {
  name: 'ContactPage',
  components: { VueTextSection, VueInput, VueForm },
  data() {
    return {
      contactFormData: {
        sender_name: '',
        sender_email: '',
        subject: '',
        recipients_group: 'Technical support',
        message: '',
      },
    }
  },
  methods: {
    async submitEmail() {
      await apiPost(
        '/contact/',
        this.contactFormData,
        {
          accept: 'application/json',
        },
        true
      )
        .then(() => {
          useToastAlertStore().showAlert('Your message has been sent', 'success')
          this.contactFormData = {}
        })
        .catch((e) => {
          useToastAlertStore().showAlert(e, 'danger', 6000)
        })
    },
  },
}
</script>

<style scoped></style>
