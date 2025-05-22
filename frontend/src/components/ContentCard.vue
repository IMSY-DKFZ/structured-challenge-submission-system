<template>
  <div class="card">
    <div class="card-header" v-if="validBacklink">
      <router-link :to="backlink.to" class="card-link">{{ backlink.text }}</router-link>
    </div>
    <div class="card-body">
      <div v-if="showLogo" class="text-center py-3">

        <router-link class="dropdown-item" :to="{ path: '/' }"><img alt="logo" src="@/assets/images/MICCAI_logo_bkg_1.png"
            class="card-logo" /></router-link>
      </div>
      <h2 class="card-title">
        {{ headline }}
      </h2>
      <p class="card-subtitle" v-if="subtitle">
        {{ subtitle }}
      </p>
      <div class="text-start" :class="[{ 'pb-5': showFooter }]">
        <slot></slot>
      </div>
      <p class="card-text pb-3" v-if="text">
        {{ text }}
      </p>
      <div v-if="showLinks" class="pb-3 text-center  small">
        <router-link :to="{ name: 'Imprint' }" class="link-secondary px-1">Imprint</router-link>
        <router-link :to="{ name: 'Data protection policy' }" class="link-secondary px-1">Data
          protection
          policy</router-link>
        <router-link :to="{ name: 'Privacy policy' }" class="link-secondary px-1">Privacy
          policy</router-link>
        <router-link :to="{ name: 'Usage of cookies' }" class="link-secondary px-1">Usage of
          cookies</router-link>
      </div>
    </div>
    <div v-if="showFooter" class="card-footer lh-sm">
      <small>®Copyright German Cancer Research Center. All rights reserved.</small>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ContentCard',
  props: {
    headline: {
      typ: String,
      required: true,
    },
    text: {
      typ: String,
      default: '',
    },
    subtitle: {
      typ: String,
      default: '',
    },
    showLogo: {
      typ: Boolean,
      default: false,
    },
    showLinks: {
      typ: Boolean,
      default: true,
    },
    showFooter: {
      typ: Boolean,
      default: true,
    },
    backlink: {
      typ: Object,
      default: {
        to: '',
        text: 'Back',
      },
    },
  },
  computed: {
    validBacklink() {
      return this.backlink.to !== ''
    },
  },
}
</script>

<style scoped>
.card {
  max-width: 450px !important;
}
</style>
