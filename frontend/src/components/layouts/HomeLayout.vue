<template>
  <div class="row">
    <div class="position-relative layout-height d-flex flex-column  vh-100">
      <NavBar />
      <NewsBanner />
      <router-view class="container p-5 pt-3 mb-5"></router-view>
      <Footer />
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeLayout',
  components: { NavBar, Footer, NewsBanner },
}
import NavBar from '@/components/essentials/NavBar.vue'
import Footer from '@/components/essentials/Footer.vue'
import NewsBanner from '@/components/essentials/NewsBanner.vue'
</script>

<style scoped></style>
