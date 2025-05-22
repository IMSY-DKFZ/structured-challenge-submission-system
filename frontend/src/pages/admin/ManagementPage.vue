<template>
  <VueTextSection>
    <template #title>Manage deadlines</template>
    <template #text>Here, you can manage the deadlines for challenge proposals and reviews.</template>
    <VueForm name="deadlines" :action-btn-fullwidth="false" action-btn="Change Deadline" @submitEvent="setDeadline">
      <VueInput label="Deadline" type="date" :required="true" v-model="deadline"></VueInput>
    </VueForm>
  </VueTextSection>
  <VueTextSection>
    <template #title>Manage start date </template>
    <template #text>Here, you can manage the start date for the submission system.</template>
    <VueForm name="startDate" :action-btn-fullwidth="false" action-btn="Change starte date" @submitEvent="setStartDate">
      <VueInput label="Deadline" type="date" :required="true" v-model="startDate"></VueInput>
    </VueForm>
  </VueTextSection>
  <VueTextSection>
    <template #title>Add news in About page</template>
    <template #text>Create news</template>
    <VueForm name="news" :action-btn-fullwidth="false" action-btn="Add News" @submitEvent="setNews">
      <VueInput label="Description" type="textarea" :required="true" v-model="news"></VueInput>
    </VueForm>
  </VueTextSection>
  <VueTextSection>
    <template #title>Write email to system users</template>
    <template #text>Email will be sent to all users with the selected roles:</template>
    <VueForm name="email" :action-btn-fullwidth="false" action-btn="Send email" @submitEvent="setMail">
      <VueInput label="Organizer" type="checkbox" :required="true" v-model="email.to.organizer">
      </VueInput>
      <VueInput label="Sub Admin" type="checkbox" :required="true" v-model="email.to.subAdmin">
      </VueInput>
      <VueInput label="Admin" type="checkbox" :required="true" v-model="email.to.admin">
      </VueInput>
      <VueInput label="Subject" type="text" :required="true" text-min-length="5" v-model="email.subject"></VueInput>
      <VueInput label="Message" type="textarea" :required="true" v-model="email.message"></VueInput>
    </VueForm>
  </VueTextSection>
  <VueTextSection v-if="useAuthStore().adminOnly">
    <template #title>Update 2018 and 2019 challenges</template>
    <template #text>Updates challenges on the Challenges Page</template>
    <VueForm name="updateChallenges" :action-btn-fullwidth="false" action-btn="Update" @submitEvent="updateChallenges">
    </VueForm>
  </VueTextSection>
  <VueTextSection v-if="useAuthStore().adminOnly">
    <template #title>Update technical support prefix and chairs mailing list</template>
    <VueForm name="prefix" :action-btn-fullwidth="false" action-btn="Update mailing list"
      @submitEvent="updateMailingList">
      <VueInput label="Technical mailing list prefix" type="text" :required="true" v-model="mailingPrefix"></VueInput>
      <VueInput label="Chairs mail addresses" type="email" :required="true" v-model="chairsMailAddress"></VueInput>
    </VueForm>
  </VueTextSection>
</template>

<script>
import VueTextSection from '@/components/VueTextSection.vue'
import VueForm from '@/components/essentials/VueForm.vue'
import VueInput from '@/components/essentials/VueInput.vue'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'ManagementPage',
  components: { VueInput, VueForm, VueTextSection },
  data() {
    return {
      deadline: '2023-07-22',
      startDate: '2023-07-22',
      news: '',
      email: {
        subject: '',
        message: '',
        to: {
          organizer: false,
          subAdmin: false,
          admin: false,
        },
      },
      mailingPrefix: 'challenges-support',
      chairsMailAddress: 'miccai-challenge-chairs@dkfz-heidelberg.de',
    }
  },
  methods: {
    useAuthStore,
    setDeadline() { },
    setStartDate() { },
    setNews() { },
    setMail() { },
    updateChallenges() { },
    updateMailingList() { },
  },
}
</script>

<style scoped></style>
