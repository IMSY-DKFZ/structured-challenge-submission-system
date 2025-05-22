<template>
  <div>
    <collapse-section name="info">
      <VueTextSection>
        <template #text>
          This view provides an overview of all your challenge proposals. Use the create new
          challenge proposal button to create new proposals. Fill out the form carefully and don't
          forget to save your data. You may change the content of your draft as often as you like
          before submission. With more than 90% of parameters covered, you can submit your proposal.
          Click on the options button and select generate proposal. After submitting your draft, the
          proposal will be reviewed by different reviewers. A MICCAI challenge (co-) chair will take
          the final decision on the acceptance of the challenge. For more details, please open the
          workflow view on the left.
        </template>
      </VueTextSection>
    </collapse-section>

    <div class="accordion" id="proposalList
">
      <LoadingCircle :activated="LoadingCircleState"></LoadingCircle>

      <div v-if="!LoadingCircleState">
        <div v-for="(item, idx) in proposalsList" :key="'item' + idx" class="py-2">

          <div class="card">
            <div class="card-header d-flex" :class="{
              'bg-success text-white': isProposalAccepted(item?.challenge_status),
              'bg-primary text-white': isProposalSubmitted(item?.challenge_status),
              'bg-danger text-bg-danger': isProposalRejected(item?.challenge_status),
              'text-bg-warning': isRevisionRequired(item?.challenge_status),
              'bg-body-secondary': !isProposalAccepted(item?.challenge_status) &&
                !isProposalSubmitted(item?.challenge_status) &&
                !isProposalRejected(item?.challenge_status) &&
                !isRevisionRequired(item?.challenge_status)
            }">
              <div class="flex-grow-1"><small class="fw-semibold">Challenge proposal ID #{{ item?.id
                  }}</small> (<small>{{ setStatusText(item?.challenge_status) }})</small></div>
              <div class="">
                <h5 :hidden="!isRevisionRequired(item?.challenge_status)">⚠️</h5>
                <h5 :hidden="!isProposalAccepted(item?.challenge_status)">✅</h5>
                <h5 :hidden="!isProposalSubmitted(item?.challenge_status)">⌛</h5>
                <h5 :hidden="!isProposalRejected(item?.challenge_status)">⛔</h5>
              </div>
            </div>

            <div class="card-body"
              :class="{ 'bg-warning-subtle': isRevisionRequired(item?.challenge_status), 'bg-danger-subtle': isProposalRejected(item?.challenge_status), 'bg-success-subtle': isProposalAccepted(item?.challenge_status), 'bg-primary-subtle': isProposalSubmitted(item?.challenge_status), }">
              <!-- <h4 class="card-title">{{ item?.challenge_abstract }}</h4> -->
              <div class="row py-3">
                <div class="col-12 col-md-8 col-lg-9">
                  <h4 class="pe-5">{{ item?.challenge_name }}</h4>
                  <VueTextSection>

                    <template #text class="w-75 pb-3">{{ item?.challenge_abstract }}</template>
                    <div class="d-flex flex-column gap-3">
                      <div>
                        <h6 class="mb-0">Status</h6>
                        <small class="mb-0 opacity-75"><span :hidden="!isRevisionRequired(item?.challenge_status)">⚠️
                          </span>{{ setStatusText(item?.challenge_status) }}</small>
                      </div>
                      <div>
                        <h6 class="mb-0">Created</h6>
                        <small class="mb-0 opacity-75">{{
                          StringToPrettyDate(item?.challenge_created_time)
                        }}</small>
                      </div>
                      <div>
                        <h6 class="mb-0">Last modified</h6>
                        <small class="mb-0 opacity-75">{{
                          StringToPrettyDate(item?.challenge_modified_time)
                        }}</small>
                      </div>
                    </div>
                  </VueTextSection>
                </div>
                <div class="col-12 col-md-4 col-lg-3">
                  <div class="d-grid gap-3 pt-3">
                    <button :disabled="!checkModifyProposal(item?.challenge_status)"
                      class="btn btn-primary text-nowrap shadow-sm"
                      :class="{ 'btn-outline-secondary': !checkModifyProposal(item?.challenge_status) }"
                      @click="$router.push({ name: 'Edit Proposal', params: { id: item?.id } })">
                      <i class="bi bi-folder2-open"></i>
                      <span class="ps-2">Edit proposal</span>
                    </button>
                    <!-- <button :disabled="!checkModifyProposal(item?.challenge_status)" class="btn btn-light text-nowrap shadow-sm"
                      type="button" @click="modifyProposal">
                      <i class="bi bi-files"></i>
                      <span class="ps-2">Modify proposal</span>
                    </button> -->

                    <!-- <button :disabled="!checkShowHistory(item?.challenge_status)" class="btn btn-light text-nowrap shadow-sm"
                      type="button" @click="showHistory">
                      <i class="bi bi-info-circle"></i>
                      <span class="ps-2">Show History</span>
                    </button> -->
                    <!-- <button :disabled="!checkCreateCopy(item?.challenge_status)" class="btn btn-light text-nowrap shadow-sm"
                      type="button" @click="createCopy">
                      <i class="bi bi-files"></i>
                      <span class="ps-2">Create a Copy</span>
                    </button> -->
                    <!-- <button :disabled="!checkModifyProposal(item?.challenge_status)" class="btn btn-light text-nowrap shadow-sm"
                      type="button" @click="modifyProposal">
                      <i class="bi bi-files"></i>
                      <span class="ps-2">Modify proposal</span>
                    </button> -->
                    <button :disabled="!checkDownloadProposal(item?.challenge_status)"
                      :class="{ 'btn': true, 'btn-success': checkDownloadProposal(item?.challenge_status), 'btn-outline-secondary': !checkDownloadProposal(item?.challenge_status) }"
                      class="text-nowrap shadow-sm" type="button" @click="downloadProposal(item?.id)">
                      <i class="bi bi-download"></i>
                      <span class="ps-2">Download proposal</span>
                    </button>
                    <button :disabled="!checkSubmitProposal(item?.challenge_status)"
                      :class="{ 'btn': true, 'btn-dark': checkSubmitProposal(item?.challenge_status), 'btn-outline-secondary': !checkSubmitProposal(item?.challenge_status) }"
                      class="text-nowrap shadow-sm" type="button" @click="submitProposal(item?.id)">
                      <i class="bi bi-send"></i>
                      <span class="ps-2">Re-generate proposal</span>
                    </button>
                    <button :disabled="checkDeleteProposal(item?.challenge_status)"
                      :class="{ 'btn-outline-secondary': checkDeleteProposal(item?.challenge_status) }"
                      class="btn btn-danger text-nowrap shadow-sm" type="button" @click="deleteProposal(item?.id)">
                      <i class="bi bi-trash3"></i>
                      <span class="ps-2">Delete proposal</span>
                    </button>
                    <!-- <button class="btn btn-outline -danger text-nowrap shadow-sm" type="button" @click="declineProposal">
                      <i class="bi bi-backspace-fill"></i>
                      <span class="ps-2">Decline proposal</span>
                    </button> -->
                  </div>
                </div>
              </div>

            </div>
            <!-- <div class="card-footer">
              <span class="mb-0">Last modified: </span>
              <small class="mb-0 opacity-75">{{
        StringToPrettyDate(item?.challenge_modified_time)
                }}</small>
            </div> -->

          </div>


        </div>
      </div>
    </div>
    <confirm-dialogue ref="confirmDialogue"></confirm-dialogue>
  </div>
</template>

<script>
import VueTextSection from '@/components/VueTextSection.vue'
import CollapseSection from '@/components/CollapseSection.vue'
import { apiGet, apiPut, apiGetDownload, apiDelete } from '@/api/api'
import { formatISO } from 'date-fns'
import StringToPrettyDate from '../../helper/format'
import ConfirmDialogue from '@/components/ConfirmDialogue.vue'
import LoadingCircle from '@/components/LoadingCircle.vue'
import { useToastAlertStore } from '@/stores/toastAlert'

export default {
  name: 'ProposalsPage',
  components: { LoadingCircle, ConfirmDialogue, CollapseSection, VueTextSection },
  data() {
    return {
      proposalsList: [],
      LoadingCircleState: true,
    }
  },

  async created() {
    await this.getAndSetProposals()
  },
  methods: {
    StringToPrettyDate,
    formatISO,
    async getAndSetProposals() {
      this.proposalsList = []
      this.LoadingCircleState = false
      await apiGet('/user/my_challenges/?limit=1000&offset=0').then((resp) => {
        this.proposalsList = resp["content"]
        this.LoadingCircleState = false
      })
    },
    showHistory() { },
    createCopy() { },
    modifyProposal() { },
    async downloadProposal(id) {
      if (Number.isInteger(id)) {
        await apiGetDownload(`/challenge/${id}/download`, {
          responseType: 'blob',
        })
          .then((response) => {

            const contentType = response.headers['content-type'];
            const blob = new Blob([response.data], { type: "application/pdf" });
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');

            link.href = url;
            const contentDisposition = response.headers['content-disposition'];
            const filenameSection = response.headers['x-content-filename'] || "Challenge_proposal.pdf";
            let decodedFilename = decodeURIComponent(filenameSection);
            link.setAttribute('download', decodedFilename);
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.URL.revokeObjectURL(url);

          })
          .catch((e) => {
            useToastAlertStore().showAlert(e, 'danger', 6000);

          });

      } else { useToastAlertStore().showAlert('Challenge not found!', 'danger', 6000); }
    },
    async submitProposal(id) {
      if (Number.isInteger(id)) {
        await apiPut(`/challenge/${id}/submit`, {
          accept: 'application/json',
        })
          .then(() => {
            this.$router.push({ name: 'Proposals' })
            useToastAlertStore().showAlert('Challenge proposal submitted successfully. You can download your submission file.', 'success', 6000);


          })
          .catch((e) => {
            // this.$router.push({ name: 'Proposals' })
            useToastAlertStore().showAlert(e, 'danger', 6000);

          });

      }
    },

    async deleteProposal(id) {
      const ok = await this.$refs.confirmDialogue.show({
        title: 'Delete proposal',
        message: 'Are you sure you want to delete this proposal? It cannot be undone.',
        okButton: 'Delete proposal permanently',
        okButtonTheme: 'btn-danger',
        showPasswordInput: true,

      })
      if (ok) {
        await apiDelete(
          `challenge/${id}/delete?active_user_password=${encodeURIComponent(
            this.$refs.confirmDialogue.password
          )}`
        )
          .then(() => {
            setTimeout(1000);
            useToastAlertStore().showAlert('The proposal was permanently deleted', 'success')
            setTimeout(3000);
            location.reload();
          })
          .catch((e) => {
            useToastAlertStore().showAlert(e, 'danger', 6000);

          });

      } else {
      }
    },
    async declineProposal() {
      const ok = await this.$refs.confirmDialogue.show({
        title: 'Decline proposal',
        message: 'Are you sure you want to decline this proposal? It cannot be undone.',
        okButton: 'Decline Forever',
      })
      if (ok) {
        // await apiDelete(`user/${userId}?active_user_password=${this.current_password}`)
        //   .then(() => {
        //     useToastAlertStore().showAlert('The proposal was permanently decline', 'success')
        //   })
        //   .catch(() => {
        //     useToastAlertStore().showAlert('Something failed. please contact an admin', 'danger', 6000)
        //   })
      } else {
      }
    },

    checkShowHistory(role) {
      return true
    },
    checkCreateCopy(role) {
      return true
    },
    checkModifyProposal(role) {
      return [
        "Draft",
        "DraftUpdated",
        "DraftSubmitted",
        "MinorRevisionRequired",
        "MajorRevisionRequired",
        "RevisionUpdated",
        "RevisionSubmitted",
        "PrelimAcceptAsStandardChallenge",
        "PrelimAcceptAsLighthouseChallenge",
        "RevisionUpdatedPrelimAccept",
        "RevisionSubmittedPrelimAccept",
        "AcceptedModifiedDraft",
        "AcceptedModifiedUpdated",
        "AcceptedModifiedSubmitted",
        'Accept',
        'AcceptAsLighthouseChallenge',
        'AcceptAsStandardChallenge',
        'AcceptedModified',
      ].includes(role)
    },
    checkDownloadProposal(role) {
      return [
        'DraftSubmitted',
        'RevisionSubmitted',
        'Accept',
        'AcceptAsLighthouseChallenge',
        'AcceptAsStandardChallenge',
        'AcceptedModified',
        'Reject',
        "AcceptedModifiedSubmitted",
        "RevisionSubmittedPrelimAccept",
        'CleanProposal'
      ].includes(role)
    },
    checkSubmitProposal(role) {
      return [
        'DraftSubmitted',
        'RevisionSubmitted',
        'Accept',
        'AcceptAsLighthouseChallenge',
        'AcceptAsStandardChallenge',
        'AcceptedModified',
        'Reject',
        "AcceptedModifiedSubmitted",
        "RevisionSubmittedPrelimAccept",
        'CleanProposal',
      ].includes(role)
    },
    isProposalSubmitted(role) {
      return [
        'DraftSubmitted',
        'RevisionSubmitted',
        "AcceptedModifiedSubmitted",
        "RevisionSubmittedPrelimAccept",

      ].includes(role)
    },
    isRevisionRequired(role) {
      return [
        'MajorRevisionRequired',
        'MinorRevisionRequired',
        'PrelimAcceptAsLighthouseChallenge',
        'PrelimAcceptAsStandardChallenge',

      ].includes(role)
    },
    isProposalRejected(role) {
      return [
        'Reject',
        'Deleted',
      ].includes(role)
    },
    isProposalAccepted(role) {
      return [
        'Accept',
        'AcceptAsLighthouseChallenge',
        'AcceptAsStandardChallenge',
        'AcceptedModified',
      ].includes(role)
    },
    checkDeleteProposal(role) {
      return [
        'Deleted',
        'Accept',
        'AcceptAsLighthouseChallenge',
        'AcceptAsStandardChallenge',
        'Reject',
        'CleanProposal'
      ].includes(role)
    },
    setStatusText(status) {
      switch (status) {
        case 'DraftSubmitted':
          return 'Draft submitted'
        case 'DraftUpdated':
          return 'Draft updated'
        case 'RevisionUpdated':
          return 'Revision updated'
        case 'RevisionSubmitted':
          return 'Revision submitted'
        case 'MajorRevisionRequired':
          return 'Major revision required'
        case 'MinorRevisionRequired':
          return 'Minor revision required'
        case 'SubmittedNewParametersAndWaitingForFeedback':
          return 'Submitted new parameters and waiting for feedback'
        case 'RevisionOfSubmittedNewParameters':
          return 'Revision of submitted new parameters'
        case 'AcceptAsLighthouseChallenge':
          return 'Accept as lighthouse challenge'
        case 'AcceptAsStandardChallenge':
          return 'Accept as standard challenge'
        case 'PrelimAcceptAsLighthouseChallenge':
          return 'Preliminary accept as lighthouse challenge (subject to minor revision)'
        case 'PrelimAcceptAsStandardChallenge':
          return 'Preliminary accept as standard challenge (subject to minor revision)'
        case 'AcceptedModified':
          return 'Accepted modified'
        case 'RevisionUpdatedPrelimAccept':
          return 'Revision updated for preliminary accept'
        case 'RevisionSubmittedPrelimAccept':
          return 'Revision submitted for preliminary accept'
        case 'AcceptedModifiedDraft':
          return 'Accepted modified draft'
        case 'AcceptedModifiedUpdated':
          return 'Accepted modified updated'
        case 'AcceptedModifiedSubmitted':
          return 'Accepted modified submitted'
        case "CleanProposal":
          return "Clean/Unmark proposal"
        default:
          return status
      }
    },
  },
}
</script>

<style scoped></style>
