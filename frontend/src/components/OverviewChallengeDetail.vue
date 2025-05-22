<template>
  <div class="py-3">
    <div class="row">
      <VueTextSection title-size="h2">
        <template #title>Diabetic Foot Ulcers Grand Challenge 2022 </template>
      </VueTextSection>
      <div class="col-12 col-lg-6">
        <VueTextSection>
          <template #title>Acronym</template>
          <template #text>BabySteps</template>
        </VueTextSection>
        <VueTextSection>
          <template #title>Website</template>
          <template #text><a href="#">https://babysteps.grand-challenge.org/</a></template>
        </VueTextSection>
      </div>
      <div class="col-12 col-lg-6">
        <VueTextSection>
          <template #title>DOI</template>
          <template #text>10.5281/zenodo.4575215</template>
        </VueTextSection>

      </div>
      <div class="col-12">
        <VueTextSection>
          <template #title>Abstract</template>
          <template #text>There has been a recent increase in high quality and large sample studies of the
            neonatal and infant brain (exemplified in studies such as the developing and baby Human
            Connectome Projects). The brain develops extremely rapidly over the perinatal period and
            much more than any other time in postnatal life. This presents challenges in image
            processing (both shape and intensity is changing) and image statistics. Standard
            neuroimaging pipelines, tailored for child or adult populations, do not work.
            Developmental trajectories are highly non-linear so typical statistical approaches are
            imprecise or in many cases inappropriate. The combination of these difficulties mean
            that analysis pipelines for the developing brain are highly innovative. This challenge
            proposal will seek to draw and develop pipelines built at sites internationally into one
            place while addressing 3 crucial questions in the field: 1. Can we detect lesions or
            abnormalities in a way that is robust to the age of a neonate at time of scan. 2. Can we
            estimate the age at birth of preterm neonates scanned at later age. 3. Can we use
            classification tools to encapsulate qualitative clinical radiological scores of brain
            injury.</template>
        </VueTextSection>
      </div>
    </div>
  </div>
</template>

<script>
import VueTextSection from '@/components/VueTextSection.vue'

export default {
  name: 'OverviewChallengeDetail',
  components: { VueTextSection },
  props: {
    title: {
      typ: String,
      default: '',
    },
    acronym: {
      typ: String,
      default: false,
    },
    website: {
      typ: String,
      default: false,
    },
    abstract: {
      typ: String,
      default: false,
    },
    doi: {
      typ: String,
      default: false,
    },
    pdfDownloadPath: {
      typ: String,
      default: false,
    },
  },
}
</script>

<style scoped></style>
