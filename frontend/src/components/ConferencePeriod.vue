<template>
  <!-- Maybe build a Slider for multi on desktop -->
  <!--  <div class="lh-sm d-none d-md-block">-->
  <!--    <div-->
  <!--      @click="controlModal"-->
  <!--      style="cursor: pointer"-->
  <!--      class="text-light"-->
  <!--      :class="[timeline ? 'py-2' : 'py-3']">-->
  <!--      <small class="m-0 p-0">{{ title }}</small-->
  <!--      ><br />-->
  <!--      <small-->
  <!--        class="fw-bold m-0 p-0 text-nowrap"-->
  <!--        v-html="timeline"></small>-->
  <!--    </div>-->
  <!--  </div>-->

  <button type="button" class="btn btn-primary d-flex gap-1 py-3" @click="controlModal">
    <i class="bi d-block d-md-none bi-info-circle"></i>
    Conference Period
  </button>

  <!-- Dialog -->
  <confirm-dialogue ref="modalDialogue">
    <hr />
    <section v-for="(item, idx) in conferences" :key="idx">
      <div class="row g-3 pb-3">
        <div class="col-12" v-if="item?.title">
          <h6 class="mb-0 text-nowrap">Title</h6>
          <small class="mb-0 opacity-75">{{ item?.title }}</small>
        </div>
        <div class="col-12" v-if="item?.timeline">
          <h6 class="mb-0 text-nowrap">Timeline</h6>
          <small class="mb-0 opacity-75">{{ item?.timelime }}</small>
        </div>
        <div class="col-12 col-md-6" v-if="item?.name">
          <h6 class="mb-0 text-nowrap">Name</h6>
          <small class="mb-0 opacity-75">{{ item?.name }}</small>
        </div>
        <div class="col-12 col-md-6" v-if="item?.city">
          <h6 class="mb-0 text-nowrap">City</h6>
          <small class="mb-0 opacity-75">{{ item?.city }}</small>
        </div>
        <div class="col-12 col-md-6" v-if="item?.country">
          <h6 class="mb-0 text-nowrap">Country</h6>
          <small class="mb-0 opacity-75">{{ item?.country }}</small>
        </div>
        <div class="col-12 col-md-6" v-if="item?.venue">
          <h6 class="mb-0 text-nowrap">Venue</h6>
          <small class="mb-0 opacity-75">{{ item?.venue }}</small>
        </div>
        <hr v-if="idx > 1" />
      </div>
    </section>
  </confirm-dialogue>
</template>
<script>
import ConfirmDialogue from '@/components/ConfirmDialogue.vue'
import { apiGet } from '@/api/api'
import StringToPrettyDate from '@/helper/format'
import { isAfter, isBefore } from 'date-fns'
import { useProposalStore } from '@/stores/proposal'

export default {
  name: 'ConferencePeriod',
  components: { ConfirmDialogue },
  data() {
    return {
      conferences: [],
      title: '',
      timeline: '',
    }
  },
  // title: 'Challenge submissions for MICCAI 2024 will be open between:',
  // timeline: '01.05.2023 00:00 CMT and 20.05.2023 00:00 CMT',
  async created() {
    await this.getConferenceAllLimited()
  },
  methods: {
    async getConferenceAllLimited() {
      //user/my_confluences...
      const currentConferences = []
      await apiGet('/conference/all_limited?limit=0&offset=0')
        .then((resp) => {
          if (resp) {
            resp["content"].forEach((x, idx) => {
              if (
                isBefore(new Date(), new Date(x.proposal_end_date)) &&
                isAfter(new Date(), new Date(x.proposal_start_date))
              ) {
                const item = {
                  ...x,
                  id: idx + 1,
                  title: x.information,
                  timelime:
                    'From ' +
                    StringToPrettyDate(x.start_date) +
                    ' till ' +
                    StringToPrettyDate(x.end_date),
                }
                currentConferences.push(item)
                this.conferences.push(item)
              }
            })
          }
          useProposalStore().setConferences(currentConferences)
        })
        .catch(() => {
          this.title = 'Conference Period could not be loaded'
          this.timeline = ''
        })
    },
    async controlModal() {
      await this.$refs.modalDialogue.show({
        title: 'Overview of current active Conferences',
        message: 'You will be able to create proposals for only one of those Conferences.',
      })
    },
  },
}
</script>
