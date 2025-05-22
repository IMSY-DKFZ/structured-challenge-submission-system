<template>
  <div class="bg-primary-subtle w-100 p-3 offcanvas d-flex flex-column flex-lg-row justify-content-between"
    data-bs-scroll="true" data-bs-backdrop="false" tabindex="-1" :class="{ show: !userAcceptedCookies }">
    <div class="lead">
      Our website uses essential cookies so that everything works as intended.
      <router-link :to="{ name: 'Usage of cookies' }">Learn more</router-link>
    </div>
    <div class="">
      <button class="btn btn-primary" @click="acceptCookies">
        Continue with Cookies
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CookieBanner',
  data() {
    return {
      userAcceptedCookies: false,
    }
  },
  mounted() {
    if (document.cookie.includes('readCookieNote')) {
      this.userAcceptedCookies = true
    }
  },
  methods: {
    acceptCookies() {
      document.cookie = `readCookieNote; expires=${new Date(new Date().getTime() + 1000 * 60 * 60 * 24 * 365).toGMTString()}; path=/`;
      this.userAcceptedCookies = true
    },
  },
}
</script>

<style scoped></style>
