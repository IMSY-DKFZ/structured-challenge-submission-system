<template>
  <div>
    <div class="pb-2">
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
    <ProposalTemplate v-if="!loadingState"></ProposalTemplate>
  </div>
</template>

<script>
import VueTextSection from '@/components/VueTextSection.vue'
import ProposalTemplate from '@/components/proposal/ProposalTemplate.vue'
import { useProposalStore } from '@/stores/proposal'
import CollapseSection from '@/components/CollapseSection.vue'
import { apiGet } from '@/api/api'
const proposalStore = useProposalStore()
export default {
  name: 'EditProposal',
  components: { CollapseSection, VueTextSection, ProposalTemplate },
  data() {
    return {
      proposalId: null,
      loadingState: true,
    }
  },
  async created() {
    this.proposalId = this.$route.params.id ? this.$route.params.id : null
    if (!this.proposalId) {
      this.$router.push({ name: 'Proposals' })
    }
    await apiGet(`challenge/${this.proposalId}`).then((resp) => {
      // set online for PUT only on Save
      proposalStore.setActiveProposalOnline(true)
      proposalStore.buildProposal(resp)
    })
    this.loadingState = false
  },
}
</script>

<style scoped></style>
