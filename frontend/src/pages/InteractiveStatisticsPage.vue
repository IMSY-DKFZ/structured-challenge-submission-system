<template>
  <div>
    <VueTextSection>
      <template #title>Number of accepted and rejected challenges </template>
      <template #text
        >Number of challenges from 2018 to 2022 that were accepted (red) or rejected (green) within
        the structured challenge submission system.
      </template>
      <lightbox-modal>
        <img
          class=""
          src="@/assets/images/statistics/NumberOfChallenges_Stati.svg"
          style="max-width: 100%"
          alt="" />
      </lightbox-modal> </VueTextSection
    ><VueTextSection>
      <template #title>Number of tasks</template>
      <template #text>
        Number of tasks/sub-challenges of accepted challenges within the structured challenge
        submission system. The density of the number of tasks is visualized by a violin plot per
        year. The median number per year is given by the black horizontal line within the white box,
        the first and third quartile as the lower and upper border of the white box, the 1.5
        interquartile range by the vertical black lines and outliers by black dots.</template
      >
      <lightbox-modal>
        <img
          class=""
          src="@/assets/images/statistics/NumberOfTasks1.svg"
          style="max-width: 100%"
          alt="" /> </lightbox-modal></VueTextSection
    ><VueTextSection>
      <template #title>Number of training and test cases</template>
      <template #text
        >Number of training (green) and test (red) cases of accepted challenge tasks within the
        structured challenge submission system. As the number of data may differ across tasks, the
        data is displayed per task rather than per challenge. The density of the number of cases is
        visualized by a violin plot per type (training/test) per year. The median number per year is
        given by the black horizontal line within the box, the first and third quartile as the lower
        and upper border of the box, the 1.5 interquartile range by the vertical black lines and
        outliers by black dots.</template
      >
      <lightbox-modal>
        <img
          class=""
          src="@/assets/images/statistics/NumberOfData1.svg"
          style="max-width: 100%"
          alt="" /> </lightbox-modal></VueTextSection
    ><VueTextSection>
      <template #title>Task categories IMG MISSING</template>
      <template #text
        >Number of task categories of accepted challenge tasks within the structured challenge
        submission system per year. As the task category may differ across tasks, the data is
        displayed per task rather than per challenge.
      </template>
      <!--      img is missing <img-->
      <!--        class=""-->
      <!--        src="@/assets/images/statistics/"-->
      <!--        style="max-width: 100%"-->
      <!--        alt="" />--> </VueTextSection
    ><VueTextSection>
      <template #title>Imaging modalities</template>
      <template #text
        >Number of imaging modalities of accepted challenge tasks within the structured challenge
        submission system per year. As the imaging modality may differ across tasks, the data is
        displayed per task rather than per challenge. Please note that a task may contain multiple
        imaging modalities.
      </template>
      <lightbox-modal>
        <img
          class=""
          src="@/assets/images/statistics/Modalities.svg"
          style="max-width: 100%"
          alt="" /> </lightbox-modal></VueTextSection
    ><VueTextSection>
      <template #title>Fields of application</template>
      <template #text
        >Number of fields of application of accepted challenge tasks within the structured challenge
        submission system per year. As the field of application may differ across tasks, the data is
        displayed per task rather than per challenge. Please note that a task may contain multiple
        fields of application.</template
      >
      <lightbox-modal>
        <img
          class=""
          src="@/assets/images/statistics/FoA.svg"
          style="max-width: 100%"
          alt="" />
      </lightbox-modal>
    </VueTextSection>
  </div>
</template>

<script setup>
import VueTextSection from '@/components/VueTextSection.vue'
import LightboxModal from '@/components/LightboxModal.vue'
</script>

<style scoped></style>
