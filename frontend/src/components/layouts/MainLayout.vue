<template>
  <div>
    <NavBar />
    <div class="container-fluid overflow-hidden">
      <div class="row">
        <SideBar />
        <main class="submission-system-main px-auto col-12 col-md-9 col-lg-10 px-lg-5 lh-base">
          <div class="pt-2">
            <CountdownTimer ref="countdownTimer" />
            <div
              class="alert alert-info text-center py-1 m-1"
              role="alert"
              v-if="countdownTimer && countdownTimer.isCountdownActive">
              <i class="bi bi-info-circle"></i> The system will remain open until
              {{ countdownTimer.remainingTime.days }} days
              {{ countdownTimer.remainingTime.hours }} hours
              {{ countdownTimer.remainingTime.minutes }} minutes
              {{ countdownTimer.remainingTime.seconds }}
              seconds for new challenge proposals.
            </div>
            <div
              class="alert alert-warning text-center py-1 m-1"
              role="alert"
              v-else>
              <i class="bi bi-exclamation-triangle-fill"></i> The system is closed for new challenge
              proposals. Please checks submission timeline for more info.
            </div>
          </div>

          <TitleBar />
          <div
            class="col-12 col-md-9 col-lg-8"
            :class="[wideMainContent ? 'w-100' : '']"
            id="content">
            <div class="pb-5">
              <router-view></router-view>
            </div>
          </div>
        </main>
        <Footer />
      </div>
    </div>
  </div>
</template>

<script>
// DOKU https://github.com/vuejs/pinia/discussions/1043
// DON'T CALL ROUTER IN STORE, it will create a circular dependencies witch crashes hot reload
import SideBar from '@/components/SideBar.vue'
import TitleBar from '@/components/TitleBar.vue'
import StickyHeader from '@/components/StickyHeader.vue'
import NavBar from '@/components/essentials/NavBar.vue'
import Footer from '@/components/essentials/Footer.vue'
import CountdownTimer from '@/components/essentials/CountdownTimer.vue'

export default {
  name: 'MainLayout',
  components: { TitleBar, SideBar, StickyHeader, NavBar, Footer, CountdownTimer },
  data() {
    return {
      countdownTimer: null,
    }
  },
  computed: {
    wideMainContent() {
      return ['proposals', 'edit proposal', 'challenges', 'users', 'overview'].includes(
        this.$route.name.toLowerCase()
      )
    },
  },
  mounted() {
    this.countdownTimer = this.$refs.countdownTimer
    const countdownStartDate = '2025-12-15T00:00:00.000+01:00' // Align with the proposal opening (CET - Berlin)
    const countdownTargetDate = '2026-01-09T10:00:00.000+01:00' // +01:00 or Central European Time (CET) - Berlin. Use +02:00 for summer time months
    this.countdownTimer.updateTargetDate(countdownTargetDate, countdownStartDate)
  },
}
</script>

<style scoped>
/*ms-sm-auto*/
</style>
