<template>
  <div>
    <VueTextSection>
      <template #text>
        <div>
          <h4>Description and scope of data processing</h4>
          <p>
            Our website uses cookies. Cookies are text files that are placed in or by the internet
            browser on the user's computer system. If a user accesses a site, a cookie may be placed
            on the user's operating system. This cookie contains a characterisitc string that
            follows clear identification of the browser for any subsequent visits of the website.
          </p>
          <h4>Purpose of data processing</h4>
          <p>
            Our website only uses essential cookies that are absolutely necessary to ensure the
            essential functions of the website. Without essential cookies, our website cannot be
            used as intended. We are only storing the seesion ID that is necessary to enable the
            website to work as intended.
          </p>
        </div>
      </template>
    </VueTextSection>
  </div>
</template>

<script setup>
import VueTextSection from '@/components/VueTextSection.vue'
</script>

<style scoped></style>
