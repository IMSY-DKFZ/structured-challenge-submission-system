<template>
  <div id="fistElement"
    class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
    <h1 class="h2">{{ title }}</h1>
    <div class="btn-toolbar mb-2 mb-md-0">
      <div class="btn-group me-2">
        <router-link v-if="isProposalsPage" :to="{ name: 'New Proposal' }" class="btn btn-lg btn-primary shadow">
          <i class="bi bi-file-earmark-plus"></i> Create new proposal
        </router-link>
        <!-- <button
          v-if="isNewProposalsPage"
          @click="deleteProposal"
          class="btn btn-sm btn-primary">
          Delete Proposal
        </button> -->
      </div>
    </div>
  </div>
</template>

<script>
import { useProposalStore } from '@/stores/proposal'
export default {
  name: 'TitleBar',
  computed: {
    title() {
      return this.$route?.name ? this.$route.name : ''
    },
    isProposalsPage() {
      return this.$route?.name === 'Proposals'
    },
    isNewProposalsPage() {
      return ['New Proposal', 'Edit Proposal'].includes(this.$route?.name)
    },
  },
  methods: {
    deleteProposal() {
      useProposalStore().newProposal()
      useProposalStore().resetCreated()
      useProposalStore().resetTasks()
      this.$router.push({ name: 'Proposals' })
    },
  },
}
</script>

<style scoped></style>
