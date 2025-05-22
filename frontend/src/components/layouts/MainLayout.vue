<template>
  <div>

    <!-- <CountdownTimer ref="countdownTimer" /> -->
    <NavBar />
    <div class="container-fluid overflow-hidden">
      <div class="row">
        <SideBar />
        <main class="submission-system-main px-auto col-12 col-md-9 col-lg-10 px-lg-5 lh-base">

          <!-- <div>
            <div class="alert alert-info text-center py-1 m-1" role="alert"
              v-if="countdownTimer && !countdownTimer.isTargetReached">
              <i class="bi bi-info-circle"></i> The system will remain open until {{
                countdownTimer.remainingTime.days }} days {{ countdownTimer.remainingTime.hours }} hours {{
                countdownTimer.remainingTime.minutes }} minutes {{ countdownTimer.remainingTime.seconds }}
              seconds for new challenge proposals.
            </div>
            <div class="alert alert-danger text-center py-1 m-1" role="alert" v-else>
              <i class="bi bi-exclamation-triangle-fill"></i> The system is closed for new challenge proposals.
            </div>
          </div> -->
          <!-- </div> -->
          <TitleBar />
          <div class="col-12 col-md-9 col-lg-8" :class="[wideMainContent ? 'w-100' : '']" id="content">
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
// import CountdownTimer from "@/components/essentials/CountdownTimer.vue";


export default {
  name: 'MainLayout',
  // components: { TitleBar, SideBar, StickyHeader, CountdownTimer },
  components: { TitleBar, SideBar, StickyHeader, NavBar, Footer },
  data() {
    return {
      countdownTimer: null,
    };
  },
  computed: {
    wideMainContent() {
      return ['proposals', 'edit proposal', 'challenges', 'users', 'overview'].includes(
        this.$route.name.toLowerCase()
      )
    },
  },
  mounted() {
    // this.countdownTimer = this.$refs.countdownTimer;
    // this.countdownTimer.updateTargetDate("2024-06-01T23:59:00.000+02:00"); // +01:00 or Central European Time (CET) - Berlin. Use +02:00 for summer time months

  },
}
</script>

<style scoped>
/*ms-sm-auto*/
</style>
