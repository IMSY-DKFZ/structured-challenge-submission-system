<template>
  <div>
    <div class="d-flex justify-content-between" :class="[dataSelected ? 'flex-column' : '']">
      <p v-if="dataSelected">
        <router-link type="button" class="btn btn-secondary" @click="unselectData" :to="{ name: 'Overview' }">
          <i class="be bi-arrow-left pe-1" />
          Go Back
        </router-link>
      </p>
    </div>

    <div v-if="dataSelected">
      <VueTextSection>
        <div class="row">
          <div class="row col-12 col-md-8 mb-3 p-3">
            <div class="col-12 col-md-6">
              <h6 class="mb-0">Acronym</h6>
              <div class="mb-3 opacity-75">{{ selectedChallenge.data?.name }}</div>
            </div>
            <div class="col-12 col-md-6">
              <h6 class="mb-0">DOI</h6>
              <div class="mb-3 opacity-75">{{ selectedChallenge.data?.doi }}</div>
            </div>
            <div class="col-6" v-if="useAuthStore().adminSubOnly">
              <a :href="selectedChallenge?.data?.name" target="_blank" class="btn btn-info text-nowrap shadow mb-3"
                type="button">
                <i class="bi bi-download"></i>
                <span class="ps-2">Download complete challenge design</span>
              </a>
            </div>
            <div class="col-12 col-md-12">
              <h6 class="mb-0">Website</h6>
              <div class="mb-3 opacity-75">
                <a :href="selectedChallenge.data?.workshop">{{
                  selectedChallenge.data?.workshop
                  }}</a>
              </div>
            </div>
            <div class="col-12 col-md-12">
              <h6 class="mb-0">Abstract</h6>
              <div class="mb-3 opacity-75">{{ selectedChallenge.data?.abstract }}</div>
            </div>
          </div>
        </div>
      </VueTextSection>
    </div>

    <div v-else class="accordion" id="overviewList">
      <LoadingCircle :activated="LoadingCircleState"></LoadingCircle>
      <div v-if="!LoadingCircleState" class="accordion-item mb-3">
        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne"
          aria-expanded="false" aria-controls="collapseOne">
          <div class="d-flex align-items-center gap-3 w-100 pe-5">
            <div class="d-flex gap-2 w-100 justify-content-between">
              <div>
                <h6 class="mb-0">MICCAI 2022</h6>
              </div>
            </div>
          </div>
        </button>
        <div id="collapseOne" class="accordion-collapse collapse" data-bs-parent="#proposalList">
          <div class="accordion-body">
            <div v-for="(item, idx) in overviewList" :key="item" @click="selectData(item, idx)" class="py-2">
              <router-link class="list-group-item list-group-item-action d-flex gap-3 align-items-center"
                :to="getChallengeURL(idx)" aria-current="true">
                <img class="rounded-circle flex-shrink-0" src="@/assets/images/challengeLogo_Reg.png" width="32"
                  height="32" />
                <div class="d-flex gap-2 w-100 justify-content-between px-2">
                  <div>
                    <p class="mb-0">{{ item?.name }}</p>
                  </div>
                </div>
                <small class="text-muted">{{ item?.year }}</small>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import VueTextSection from '@/components/VueTextSection.vue'
import { apiGet } from '@/api/api'
import { useAuthStore } from '@/stores/auth'
import LoadingCircle from '@/components/LoadingCircle.vue'
import { useToastAlertStore } from '@/stores/toastAlert'

export default {
  name: 'ChallengeOverviewPage',
  components: { LoadingCircle, VueTextSection },
  data() {
    return {
      selectedChallenge: {},
      overviewList: [],
      LoadingCircleState: true,
    }
  },
  async created() {
    await this.getChallengeAllLimited()
    this.checkRouterPath()
  },
  computed: {
    dataSelected() {
      return this.selectedChallenge.data
    },
  },
  watch: {
    $route(val) {
      if (val.fullPath === '/overview') {
        this.selectedChallenge = {}
      }
    },
  },
  methods: {
    useAuthStore,
    async getChallengeAllLimited() {

      await apiGet('/challenge/all_limited')
        .then((resp) => {
          this.overviewList = resp["content"]
          this.LoadingCircleState = false
        })
        .catch((e) => {
          useToastAlertStore().showAlert(e, 'danger')
        })
    },
    checkRouterPath() {
      let index = this.$route.fullPath.slice(10, this.$route.fullPath.length)
      if (parseInt(index)) {
        if (!this.selectedChallenge.data) {
          this.getChallengeAllLimited()
          this.selectData(this.overviewList[parseInt(index)], parseInt(index))
        }
      }
    },
    selectData(item, idx) {
      this.selectedChallenge = {
        data: item,
        index: idx,
      }
    },
    unselectData() {
      this.selectedChallenge = {}
      this.searchString = ''
    },
    getChallengeURL(idx) {
      return `overview/${idx.toString()}`
    },
  },
}
</script>

<style scoped></style>
