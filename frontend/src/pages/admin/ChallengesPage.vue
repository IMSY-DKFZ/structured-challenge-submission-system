<template>
  <div>
    <p v-if="dataSelected">
      <router-link type="button" class="btn btn-secondary" @click="unselectData" :to="{ name: 'Challenges' }">
        <i class="be bi-arrow-left pe-1" />
        Go Back
      </router-link>
    </p>
    <div v-if="dataSelected">
      <VueTextSection>
        <div class="row">
          <div class="row col-12 col-md-12 mb-3 p-3">

            <div class="col-12 p-2">
              <h6 class="mb-0">Name</h6>
              <div class="overflow-auto" style="max-height: 150px;">{{ dataSelected?.challenge_name }}</div>
            </div>

            <!-- <div class="col-12 p-2">
              <h6 class="mb-0">Autor names</h6>
              <div class="mb-3 opacity-75">
                <div class="overflow-auto" style="max-height: 150px;">{{ dataSelected?.challenge_author_names }}</div>
              </div>
            </div> -->
            <!-- <div class="col-12 p-2">
              <h6 class="mb-0">Autor emails</h6>
              <div class="mb-3 opacity-75">
                <div class="overflow-auto" style="max-height: 150px;">{{
                  dataSelected?.challenge_author_emails }}</div>
              </div>
            </div> -->



            <!-- <div class="col-12 col-md-3 p-2">
              <h6 class="mb-0">Year</h6>
              <div class="mb-3 opacity-75">{{ dataSelected?.challenge_year }}</div>
            </div> -->
            <div class="col-12 col-md-3 p-2">
              <h6 class="mb-0">Acronym</h6>
              <div class="mb-3 opacity-75">{{ dataSelected?.challenge_acronym }}</div>
            </div>
            <div class="col-12 col-md-2 p-2">
              <h6 class="mb-0">Owner ID</h6>
              <div class="mb-3 opacity-75">{{ dataSelected?.challenge_owner_id }}</div>
            </div>
            <div class="col-12 col-md-7 p-2">
              <h6 class="mb-0">Status</h6>
              <div class="mb-3 opacity-75">{{ dataSelected?.challenge_status }}</div>
            </div>


            <div class="col-12 col-md-4 p-2">
              <h6 class="mb-0">Created time</h6>
              <div class="mb-3 opacity-75">
                {{ StringToPrettyDate(dataSelected?.challenge_created_time) }}
              </div>
            </div>
            <div class="col-12 col-md-4 p-2">
              <h6 class="mb-0">Last modified time</h6>
              <div class="mb-3 opacity-75">
                {{ StringToPrettyDate(dataSelected?.challenge_modified_time) }}
              </div>
            </div>
            <div class="col-12 col-md-4 p-2">
              <h6 class="mb-0">Submitted time</h6>
              <div class="mb-3 opacity-75">
                {{ StringToPrettyDate(dataSelected?.challenge_submission_time) }}
              </div>
            </div>


          </div>
          <div class="row col-12 col-md-8 mb-3">
            <hr>
            <VueTextSection title-size="h4">
              <template #title>Download proposal</template>
              <button type="button" class="btn btn-info downloadFile" :disabled="!dataSelected.challenge_file"
                @click="downloadChallenge(dataSelected?.id)">
                <i v-if="!LoadingCircleStateDownload" class="be bi-download" />

                <div v-if="LoadingCircleStateDownload" class="d-flex align-items-center justify-content-around">
                  <div class="spinner-border spinner-border-sm me-3" role="status" aria-hidden="true"></div>
                  <span>Downloading...</span>
                </div>
                {{ btnTitle }}
              </button>
              <div class="mb-3 opacity-75" v-if="!dataSelected.challenge_file">
                No file submitted yet
              </div>
            </VueTextSection>
            <!-- <VueTextSection title-size="h4" v-if="useAuthStore().adminOnly">
              <template #title>Register challenge</template>
              <button type="button" class="btn btn-success">
                <i class="be bi-patch-check-fill" @click="registerChallenge" />
                Register challenge
              </button>
            </VueTextSection> -->
            <hr>
            <VueTextSection v-if="useAuthStore().adminOnly" title-size="h4">
              <template #title>Change Status</template>
              <VueForm action-btn="Change Status" name="status" :action-btn-fullwidth="false" @submit-event="setStatus">
                <VueInput v-model="status" type="select" :options="statusList"></VueInput>
              </VueForm>
            </VueTextSection>
            <hr>
            <VueTextSection v-if="useAuthStore().adminOnly" title-size="h4">
              <template #title>Allow for further modifications after deadline</template>
              <div class="mb opacity-75">
                The owner can edit proposal even conference is closed for further submissions.
              </div>
              <VueForm action-btn="Apply" name="allowModification" :action-btn-fullwidth="false"
                @submit-event="setAllowModification">
                <VueInput v-model="allowModification" type="select" :options="allowModificationList"></VueInput>
              </VueForm>
            </VueTextSection>
            <!-- <VueTextSection v-if="useAuthStore().adminOnly" title-size="h4">
              <template #title>Assign to other user</template>
              <VueForm action-btn="Change creator" name="creator" :action-btn-fullwidth="false" @submit-event="setCreator"
                :errorMessage="failMessageCreator">
                <VueInput v-model="creator" type="select" :options="creatorListText"></VueInput>
              </VueForm>
            </VueTextSection> -->
            <hr>
            <VueTextSection v-if="useAuthStore().adminOnly" title-size="h4">
              <VueTextSection :highlight="true">
                <template #title>☢️ Prune challenge</template>
                <div class="mb opacity-75">
                  Please enter your current password if you want to prune this challenge.
                </div>
                <template #text>Delete this challenge with its all tasks, and all histories in database. ☢️ This action
                  can
                  not be undone! ☢️</template>
                <VueInput label="Current password" type="password" v-model="current_password"></VueInput>
                <button type="button" :disabled="!current_password" class="mt-3 btn btn-danger"
                  @click="deleteChallenge">
                  <i class="be bi-trash2-fill" />
                  Prune challenge
                </button>
              </VueTextSection>
            </VueTextSection>
            <hr>
            <div class="alert alert-info" role="alert">
              For more admin operations for challenges please visit:<br> <a :href="docsURL" target="_blank">{{ docsURL
              }}</a>
            </div>
          </div>
        </div>
      </VueTextSection>
    </div>
    <div v-else>

      <div class="input-group pb-4">
        <VueInput v-model="searchString" :disabled="!loadingCircle" class="form-control" type="text" icon="search"
          :placeholder="'Filter parameters'">
        </VueInput>
        <span class="input-group-text">Total record: {{ totalItems }} </span>

        <!-- <button class="btn btn-outline-primary border-secondary-subtle" type="button" data-bs-toggle="dropdown"
          aria-expanded="false">Bulk operations <i class="bi bi-caret-down-fill"></i></button> -->

        <ul class="dropdown-menu">

          <li><a class="dropdown-item" @click="changeStatusSelectedRows" :disabled="selectedRows.length === 0"
              href="#">Change
              Status Selected</a></li>
          <!-- <li>
            <hr class="dropdown-divider">
          </li> -->

          <li class=""><a class="dropdown-item bg-danger text-white" @click="deleteSelectedRows"
              :disabled="selectedRows.length === 0" href="#">Delete
              Selected</a></li>

        </ul>
        <button class="btn btn-outline-primary border-secondary-subtle rounded-end" type="button"
          data-bs-toggle="dropdown" aria-expanded="false">Items per page <i class="bi bi-caret-down-fill"></i></button>

        <ul class="dropdown-menu">
          <li v-for="option in itemsPerPageOptions" :key="option">
            <a class="dropdown-item" :class="{ 'active': option === this.itemsPerPage }"
              @click="changeItemsPerPage(option)" href="#">{{ option }}</a>
          </li>
        </ul>
      </div>
      <div>
        <hr>
        <ul class="pagination justify-content-center">
          <li class="page-item" :class="{ 'disabled': currentPage === 1 }">
            <a class="page-link" @click="changePage(currentPage - 1)" aria-label="Previous" href="#">
              <span aria-hidden="true">&laquo;</span>
            </a>
          </li>
          <li class="page-item" v-for="page in Math.ceil(totalItems / itemsPerPage)" :key="page">
            <a class="page-link" @click="changePage(page)" href="#">{{ page }}</a>
          </li>
          <li class="page-item" :class="{ 'disabled': currentPage === Math.ceil(totalItems / itemsPerPage) }">
            <a class="page-link" @click="changePage(currentPage + 1)" aria-label="Next" href="#">
              <span aria-hidden="true">&raquo;</span>
            </a>
          </li>
        </ul>
      </div>

      <div class="table-responsive">
        <table class="table table-striped table-hover">
          <thead>
            <tr class="table-primary">
              <th>
                <input type="checkbox" v-model="selectAll" @change="selectAllRows">
              </th>
              <th v-for="(item, idx) in tableHeader" :key="idx" @click="sortTable(item)">
                <a href="#" class="link-underline-primary link-offset-2 link-underline-opacity-50">{{ item }}<span
                    v-if="sortColumn === item">
                    <i :class="sortDirection === 'asc' ? 'bi bi-caret-up-fill' : 'bi bi-caret-down-fill'"></i>
                  </span>
                </a>
              </th>
            </tr>
          </thead>
          <tbody v-if="!LoadingCircleState">
            <tr v-for="(item, idx) in list" class="lh-base" :key="idx" style="cursor: pointer; max-width: 50px;"
              @click="selectData(item, idx)">
              <td @click.stop>
                <input type="checkbox" v-model="selectedRows" :value="item.id">
              </td>
              <td style="min-width: 10px; max-width: 10px;">{{ item?.id }}</td>
              <td style="min-width: 10px; max-width: 10px;">{{ item?.challenge_owner_id }}</td>
              <td style="min-width: 60px; max-width: 60px;">{{ item?.challenge_year }}</td>
              <td>{{ item?.challenge_name !== null ? item?.challenge_name.length > 80 ? item?.challenge_name.slice(0,
                80) + "..." : item?.challenge_name : null }}</td>
              <!-- <td>{{ item?.challenge_progress }}</td> -->
              <td style="min-width: 170px;">{{ setStatusPretty(item?.challenge_status) }}</td>
              <td style="min-width: 110px;">
                <small>{{ StringToPrettyDate(item?.challenge_modified_time) }}</small>
              </td>
              <!-- <td>
                <div class="mx-2">{{ item?.challenge_author_names !== null ? item?.challenge_author_names.length > 100 ?
                  item?.challenge_author_names.slice(0,
                    100) + "..." : item?.challenge_author_names : null }}</div>
              </td> -->
            </tr>
          </tbody>
        </table>
        <LoadingCircle :activated="LoadingCircleState"></LoadingCircle>

        <div v-if="list?.length === 0" class="text-center">
          <p class="lead">No data found</p>
        </div>
      </div>
      <div>
        <hr>
        <ul class="pagination justify-content-center">
          <li class="page-item" :class="{ 'disabled': currentPage === 1 }">
            <a class="page-link" @click="changePage(currentPage - 1)" aria-label="Previous" href="#">
              <span aria-hidden="true">&laquo;</span>
            </a>
          </li>
          <li class="page-item" v-for="page in Math.ceil(totalItems / itemsPerPage)" :key="page">
            <a class="page-link" @click="changePage(page)" href="#">{{ page }}</a>
          </li>
          <li class="page-item" :class="{ 'disabled': currentPage === Math.ceil(totalItems / itemsPerPage) }">
            <a class="page-link" @click="changePage(currentPage + 1)" aria-label="Next" href="#">
              <span aria-hidden="true">&raquo;</span>
            </a>
          </li>
        </ul>
      </div>
    </div>

    <confirm-dialogue ref="confirmDialogue"></confirm-dialogue>
  </div>
</template>

<script>
import VueTextSection from '@/components/VueTextSection.vue'
import VueInput from '@/components/essentials/VueInput.vue'
import VueForm from '@/components/essentials/VueForm.vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'
import { apiDelete, apiGetDownload, apiPut, apiPost } from '@/api/api'
import ConfirmDialogue from '@/components/ConfirmDialogue.vue'
import LoadingCircle from '@/components/LoadingCircle.vue'
import loadingCircle from '@/components/LoadingCircle.vue'
import { useToastAlertStore } from '@/stores/toastAlert'
import StringToPrettyDate from '../../helper/format'

function convertInBlob(base64) {
  base64 = base64.replace('data:application/pdf;base64,', '')
  const contentType = 'application/pdf'
  const sliceSize = 512

  const byteCharacters = atob(base64)
  const byteArrays = []

  for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
    const slice = byteCharacters.slice(offset, offset + sliceSize)

    const byteNumbers = new Array(slice.length)
    for (let i = 0; i < slice.length; i++) {
      byteNumbers[i] = slice.charCodeAt(i)
    }

    const byteArray = new Uint8Array(byteNumbers)
    byteArrays.push(byteArray)
  }

  const blob = new Blob(byteArrays, { type: contentType })
  const blobUrl = URL.createObjectURL(blob)
  return blobUrl
}
function downloadFilePdf(blob, fileName) {
  const link = document.createElement('a')
  link.href = blob
  link.download = fileName
  document.body.append(link)
  link.click()
  link.remove()
  setTimeout(() => URL.revokeObjectURL(link.href), 7000)
}

export default {
  name: 'ChallengesPage',
  components: { LoadingCircle, ConfirmDialogue, VueForm, VueInput, VueTextSection },
  computed: {
    docsURL() {
      return new URL('/api/docs', api.defaults.baseURL).href
    },
    loadingCircle() {
      return loadingCircle
    },
    dataSelected() {
      return this.data.data
    },
    tableHeaders() {
      return this.tableHeaders
    },
    btnTitle() {
      let defaultText = 'Download proposal'
      return this.LoadingCircleStateDownload ? null : defaultText
    },
    list() {
      const filteredList = this.searchString === ''
        ? this.challengesList
        : this.challengesList.filter((item) =>
          item.id.toString() === this.searchString ||
          (item.challenge_year && typeof item.challenge_year == 'string' && item.challenge_year.toLowerCase().includes(this.searchString.toLowerCase().trim())) ||
          (item.challenge_progress && typeof item.challenge_progress == 'string' && item.challenge_progress.toLowerCase().includes(this.searchString.toLowerCase().trim())) ||
          (item.challenge_name && typeof item.challenge_name == 'string' && item.challenge_name.toLowerCase().includes(this.searchString.toLowerCase().trim())) ||
          (item.challenge_author_emails && typeof item.challenge_author_emails == 'string' && item.challenge_author_emails.toLowerCase().includes(this.searchString.toLowerCase().trim())) ||
          item.challenge_status.toLowerCase().includes(this.searchString.toLowerCase().trim())
        );
      return filteredList;
    }
  },
  data() {
    return {
      searchString: '',
      data: {},
      status: '',
      allowModification: '',
      creator: '',
      tableHeader: ['ID', 'Owner ID', 'Year', 'Name', 'Status', 'Last modified'],
      tableHeaderColumnNames: ['id', 'challenge_owner_id', 'challenge_year', 'challenge_name', 'challenge_status', 'challenge_modified_time'],
      sortColumn: 'ID',        // Track the current sort column
      sortDirection: 'asc',  // Track the current sort direction
      selectedRows: [],  // Track the selected rows
      selectAll: false,  // Track whether all rows are selected
      statusList: [

        "Draft",
        "DraftUpdated",
        "DraftSubmitted",
        "MinorRevisionRequired",
        "MajorRevisionRequired",
        "RevisionUpdated",
        "RevisionSubmitted",
        "Locked",
        "Accept",
        "Reject",
        "AcceptAsLighthouseChallenge",
        "AcceptAsStandardChallenge",
        "AcceptedModified",
        "PrelimAcceptAsStandardChallenge",
        "PrelimAcceptAsLighthouseChallenge",
        "RevisionUpdatedPrelimAccept",
        "RevisionSubmittedPrelimAccept",
        "AcceptedModifiedDraft",
        "AcceptedModifiedUpdated",
        "AcceptedModifiedSubmitted",
        "Deleted",
        "CleanProposal"
      ],
      allowModificationList: [
        "Allow further modification",
        "Don't allow further modification",
      ],
      challengesList: [],
      // creatorList: [],
      // creatorListText: [],
      failMessageCreator: null,
      current_password: null,
      LoadingCircleState: true,
      LoadingCircleStateDownload: false,
      currentPage: 1,
      itemsPerPage: 100,
      itemsPerPageOptions: [20, 50, 100, 200],
      totalItems: 0,
    }
  },
  mounted() {
    if (this.$route.params.id && !this.dataSelected) {
      this.$router.push({ name: 'Challenges' })
    }
  },
  async created() {
    await this.getAndSetChallengeAll()
    // await this.getAndSetUserAll()
  },
  methods: {
    StringToPrettyDate,
    useAuthStore,
    async getAndSetChallengeAll() {
      const offset = (this.currentPage - 1) * this.itemsPerPage;
      const apiEndpoint = `/admin/challenge/all/?limit=${this.itemsPerPage}&offset=${offset}`;
      const output_filters = [
        "id",
        "challenge_name",
        "challenge_author_names",
        "challenge_author_emails",
        "challenge_year",
        "challenge_acronym",
        "challenge_owner_id",
        "challenge_status",
        "challenge_created_time",
        "challenge_modified_time",
        "challenge_submission_time",
        "challenge_file"
      ]
      let payload = { output_filters }
      await apiPost(apiEndpoint, payload).then((resp) => {
        this.challengesList = resp["content"]
        this.totalItems = resp["total_records"];
        this.LoadingCircleState = false
      })
    },
    // async getAndSetUserAll() {
    //   await apiPost('/admin/user/all/?limit=10&offset=0').then((resp) => {
    //     this.creatorList = resp["content"]
    //     this.getCreatorText()
    //   })
    // },
    selectData(item, idx) {
      this.data = {
        data: item,
        index: idx,
      }
      this.status = this.setStatusText()
      // this.creator = this.dataSelected?.challenge_author_names[0] !== null ? this.dataSelected.challenge_author_names[0] : "No author name";
      // this.creator = this.dataSelected?.challenge_author_names !== null ? this.dataSelected.challenge_author_names : "No author name";
      this.$router.push(`challenges/${idx}`)
    },
    unselectData() {
      this.data = {}
      this.searchString = ''
      this.failMessageCreator = null
    },
    async downloadChallenge(id) {
      if (Number.isInteger(id)) {
        this.LoadingCircleStateDownload = true
        await apiGetDownload(`/admin/challenge/${id}/download`, {
          responseType: 'blob',
        })
          .then((response) => {
            const contentType = response.headers['content-type'];
            const blob = new Blob([response.data], { type: "application/pdf" });
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');

            link.href = url;
            const filenameSection = response.headers['x-content-filename'] || "Challenge_proposal.pdf";
            let decodedFilename = decodeURIComponent(filenameSection);
            link.setAttribute('download', decodedFilename);
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.URL.revokeObjectURL(url);
            this.LoadingCircleStateDownload = false
          })
          .catch((e) => {
            this.LoadingCircleStateDownload = false
            useToastAlertStore().showAlert(e, 'danger', 6000)
          })
      }
    },
    async registerChallenge() {
      // await apiGet(`challenge/${challengeId}/download`)
      //   .then(() => {
      //     useToastAlertStore().showAlert('The challenge was registered', 'success')
      //   })
      //   .catch((resp) => {
      //     useToastAlertStore().showAlert(resp, 'danger', 6000)
      //   })
    },

    async setAllowModification() {
      let is_allowed_for_further_editing = false
      if (this.allowModification === this.allowModificationList[0]) {
        is_allowed_for_further_editing = true
      }
      // let challenge_locked = this.setLocked(challenge_status)
      let data = {
        is_allowed_for_further_editing: is_allowed_for_further_editing
      }
      await apiPut(`admin/challenge/${this.dataSelected?.id}/update`, data)
        .then(() => {
          useToastAlertStore().showAlert('Challenge updated', 'success')
        })
        .catch((e) => {
          useToastAlertStore().showAlert(e, 'danger', 6000)
        })
    },
    async setStatus() {
      let challenge_status = this.setStatusCamelCase()
      // let challenge_locked = this.setLocked(challenge_status)
      let newStatus = {
        challenge_status: challenge_status
      }
      await apiPut(`admin/challenge/${this.dataSelected?.id}/status`, newStatus)
        .then(() => {
          useToastAlertStore().showAlert('The status was changed', 'success')
        })
        .catch((e) => {
          useToastAlertStore().showAlert(e, 'danger', 6000)
        })
    },
    setStatusCamelCase() {
      switch (this.status) {
        case 'Draft submitted':
          return 'DraftSubmitted'
        case 'Draft updated':
          return 'DraftUpdated'
        case 'Revision updated':
          return 'RevisionUpdated'
        case 'Revision submitted':
          return 'RevisionSubmitted'
        case 'Registered but submitted':
          return 'RevisionSubmitted'
        case 'Major revision required':
          return 'MajorRevisionRequired'
        case 'Minor revision required':
          return 'MinorRevisionRequired'
        case 'Submitted new parameters and waiting for feedback':
          return 'SubmittedNewParametersAndWaitingForFeedback'
        case 'Revision of submitted new parameters':
          return 'RevisionOfSubmittedNewParameters'
        case 'Accept as lighthouse challenge':
          return 'AcceptAsLighthouseChallenge'
        case 'Accept as standard challenge':
          return 'AcceptAsStandardChallenge'
        case 'Preliminary accept as lighthouse challenge (subject to minor revision)':
          return 'PrelimAcceptAsLighthouseChallenge'
        case 'Preliminary accept as standard challenge (subject to minor revision)':
          return 'PrelimAcceptAsStandardChallenge'
        case 'Accepted modified':
          return 'AcceptedModified'
        case 'Revision updated for preliminary accept':
          return 'RevisionUpdatedPrelimAccept'
        case 'Revision submitted for preliminary accept':
          return 'RevisionSubmittedPrelimAccept'
        case 'Accepted modified draft':
          return 'AcceptedModifiedDraft'
        case 'Accepted modified updated':
          return 'AcceptedModifiedUpdated'
        case 'Accepted modified submitted':
          return 'AcceptedModifiedSubmitted'
        case "Clean/Unmark proposal":
          return "CleanProposal"
        default:
          return this.status
      }
    },
    setStatusPretty(status) {
      switch (status) {
        case 'Draft':
          return 'Draft ⚪'
        case 'DraftSubmitted':
          return 'Draft submitted 🟢'
        case 'DraftUpdated':
          return 'Draft updated 🟡'
        case 'RevisionSubmitted':
          return 'Revision submitted 🟢'
        case 'MajorRevisionRequired':
          return 'Major revision required ‼️'
        case 'MinorRevisionRequired':
          return 'Minor revision required ❗'
        case 'SubmittedNewParametersAndWaitingForFeedback':
          return 'Submitted new parameters and waiting for feedback 🟢'
        case 'RevisionOfSubmittedNewParameters':
          return 'Revision of submitted new parameters'
        case 'Accept':
          return 'Accept ✔️'
        case 'Reject':
          return 'Reject ❌'
        case 'AcceptAsLighthouseChallenge':
          return 'Accept as lighthouse challenge ✔️'
        case 'AcceptAsStandardChallenge':
          return 'Accept as standard challenge ✔️'
        case 'PrelimAcceptAsLighthouseChallenge':
          return 'Preliminary accept as lighthouse challenge (subject to minor revision)'
        case 'PrelimAcceptAsStandardChallenge':
          return 'Preliminary accept as standard challenge (subject to minor revision)'
        case "CleanProposal":
          return "Clean/Unmark proposal 🧹"
        default:
          return status
      }
    },
    // setLocked(challenge_status) {
    //   const validStatuses = ['DraftSubmitted', 'RevisionSubmitted', 'Accept', 'Reject', 'Deleted'];
    //   return validStatuses.includes(challenge_status);
    // },
    setStatusText() {
      switch (this.dataSelected?.challenge_status) {
        case 'DraftSubmitted':
          return 'Draft submitted'
        case 'DraftUpdated':
          return 'Draft updated'
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
        case "CleanProposal":
          return "Clean/Unmark proposal"
        default:
          return this.dataSelected?.challenge_status
      }
    },
    async setCreator() {
      this.failMessageCreator = null
      // this.dataSelected.challenge_author_names = [this.creator]
      await apiPut(`admin/challenge/${this.dataSelected?.id}/update`, this.dataSelected)
        .then((resp) => {
          if (resp?.name && resp?.name === 'AxiosError') {
            this.failMessageCreator = resp?.response?.data.detail
          } else {
            useToastAlertStore().showAlert('Another user has been assigned', 'success')
          }
        })
        .catch((e) => {
          useToastAlertStore().showAlert(e, 'danger', 6000)
        })
    },
    // getCreatorText() {
    //   this.creatorList.forEach((creator) => {
    //     this.creatorListText.push(creator.first_name + ' ' + creator.last_name)
    //   })
    // },
    async deleteChallenge() {
      const ok = await this.$refs.confirmDialogue.show({
        title: 'Prune challenge proposal',
        message: 'Are you sure you want to prune this challenge? It cannot be undone.',
        okButton: 'Prune forever',
        okButtonTheme: 'btn-danger',
      })
      if (ok) {
        await apiDelete(
          `admin/challenge/${this.dataSelected?.id}/prune?active_user_password=${encodeURIComponent(
            this.current_password
          )}`
        )
          .then(() => {
            useToastAlertStore().showAlert('The challenge was finally deleted', 'success')
            setTimeout(1000);
            location.reload();
          })
          .catch((e) => {
            useToastAlertStore().showAlert(e, 'danger', 6000)
          })
      } else {
      }
    },
    changePage(page) {
      if (page >= 1 && page <= Math.ceil(this.totalItems / this.itemsPerPage)) {
        this.currentPage = page;
      }
    },
    changeItemsPerPage(option) {
      this.itemsPerPage = option
      this.currentPage = 1; // Reset to the first page when items per page changes
      this.getAndSetChallengeAll();
    },
    sortTable(column) {
      // Toggle sort direction if the same column is clicked again
      if (this.sortColumn === column) {
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
      } else {
        // Reset sort direction if a new column is clicked
        this.sortDirection = 'asc';
      }

      this.sortColumn = column;
      let idx = this.tableHeader.indexOf(column)

      // Perform sorting based on the selected column and direction
      this.list.sort((a, b) => {
        const valueA = this.getSortableValue(a[this.tableHeaderColumnNames[idx]]);
        const valueB = this.getSortableValue(b[this.tableHeaderColumnNames[idx]]);

        if (valueA < valueB) {
          return this.sortDirection === 'asc' ? -1 : 1;
        }
        if (valueA > valueB) {
          return this.sortDirection === 'asc' ? 1 : -1;
        }
        return 0;
      });
    },
    getSortableValue(value) {
      // Convert values to a common type for proper sorting
      if (typeof value === 'string') {
        return value.toLowerCase();
      } else if (value instanceof Date) {
        return value.getTime();
      } else {
        return value;
      }
    },
    selectAllRows() {
      // Toggle the selection of all rows
      if (this.selectAll) {
        this.selectedRows = this.challengesList.map(item => item.id);
      } else {
        this.selectedRows = [];
      }
    },
    deleteSelectedRows() {
      // Implement your logic to delete selected rows
      // You can use this.selectedRows array to get the selected rows

    },
    changeStatusSelectedRows() {
      // Implement your logic to change status of selected rows
      // You can use this.selectedRows array to get the selected rows

    },
  },
  watch: {
    $route(val) {
      if (val.fullPath === '/challenges') {
        this.data = {}
        this.searchString = ''
      }
    },
    currentPage: 'getAndSetChallengeAll',
  },
}
</script>

<style scoped>
input[type="checkbox"] {
  transform: scale(1.4);
}
</style>
