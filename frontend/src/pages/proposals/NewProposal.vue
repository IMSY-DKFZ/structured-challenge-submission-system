<template>
  <div>
    <div class="pb-5">
      <router-link type="button" class="btn btn-outline-secondary me-2" :to="{ name: 'Proposals' }">
        <i class="be bi-arrow-left pe-1" />
        Go Back
      </router-link>
      <collapse-section name="InfoProposal">
        <VueTextSection>
          <template #text>
            <p>
              This view provides all challenge parameters for this proposal. Please fill in as many
              parameters as you can. You have to fill in a challenge name to save a challenge. The
              progress bar only updates after saving the proposal! Thank you for using the structured
              challenge submission system for MICCAI challenges!
            </p>
            <p>
              This form is the key to create a new challenge proposal. Please enter as many parameters
              as you can. You are able to submit a proposal after filling in at least 90% of the
              parameters. Please read the parameter descriptions carefully to avoid entering wrong
              information!
            </p>
          </template>
        </VueTextSection>
      </collapse-section>
    </div>
    <VueForm @submitEvent="createChallenge" actionBtn="Create Challenge Proposal" name="beforeProposalData"
      :showActionBtn="!noConferences" :error-message="noConferences" :actionBtnFullwidth="true">
      <br />
      <vue-text-section>
        <h2>Challenge name<small class="text-danger"><b>*</b></small></h2>
        <VueInput label="Use the title to convey the essential information on the challenge mission." type="text"
          :required="true" text-min-length="5" v-model="title">
        </VueInput>
      </vue-text-section>
      <vue-text-section>
        <h2>Conference<small class="text-danger"><b>*</b></small></h2>
        <VueInput label="Assign your proposal to a Conference" type="select" :options="options" :required="true"
          v-model="selectedConference">
        </VueInput>
      </vue-text-section>
    </VueForm>
    <confirm-dialogue ref="confirmDialogue"></confirm-dialogue>
  </div>
</template>

<script>
import VueTextSection from '@/components/VueTextSection.vue'
import { useProposalStore } from '@/stores/proposal'
import CollapseSection from '@/components/CollapseSection.vue'
import confirmDialogue from '@/components/ConfirmDialogue.vue'
import VueForm from '@/components/essentials/VueForm.vue'
import VueInput from '@/components/essentials/VueInput.vue'
import { apiPost } from '@/api/api'
import { useToastAlertStore } from '@/stores/toastAlert'
const proposalStore = useProposalStore()
export default {
  components: {
    VueInput,
    VueForm,
    CollapseSection,
    VueTextSection,
    confirmDialogue,
  },
  data() {
    return {
      loadingState: true,
      title: '',
      options: [],
      selectedConference: '',
      noConferencesMessage: 'There are currently no available conferences to create a proposal!',
    }
  },
  async created() { },
  async mounted() {
    this.options = await proposalStore.getConferences
    this.options = this.options.map((x) => x.name)

    if (!this.noConferences) {
      this.selectedConference = null
    }

  },
  computed: {
    noConferences() {
      return this.options.length !== 0 ? false : this.noConferencesMessage
    },

    async selectedConferenceId() {
      const conference_list = await proposalStore.getConferences;  // Make sure to await the asynchronous function
      const selectedConf = conference_list.find((x) => x.name === this.selectedConference);
      return selectedConf ? selectedConf.id : null;
    },
  },
  methods: {
    async createChallenge() {
      const conferenceId = await this.selectedConferenceId
      if (!conferenceId) {
        useToastAlertStore().showAlert('No conference found', 'danger', 6000)
        return
      }
      await apiPost('challenge/create?conference_id=' + conferenceId, {
        challenge_name: this.title,
      })
        .then(() => {
          useToastAlertStore().showAlert(
            'Your proposal was successfully created, please fill all necessary fields for submission'
          )
          this.$router.push({ name: 'Proposals' })
        })
        .catch((e) => {
          useToastAlertStore().showAlert(e, 'danger', 6000)
        })
    },
    async linkToWorkInProgressProposal(id) {
      const ok = await this.$refs.confirmDialogue.show({
        title: 'You are currently working on an Proposal!',
        message: 'Do you wish to create a new one? Not Saved Data might be lost! ',
        okButton: 'Start new Proposal',
        cancelButton: 'Continue current Proposal',
      })
      if (ok) {
        proposalStore.newProposal()
        this.loadingState = false
      } else {
        this.$router.push({ name: 'Edit Proposal', params: { id: id } })
      }
    },
  },
}
</script>

<style scoped></style>
