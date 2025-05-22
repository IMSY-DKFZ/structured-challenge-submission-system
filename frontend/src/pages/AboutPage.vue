<template>
  <div class="lh-base">
    <!-- <VueTextSection>
      <template #title>News and updates</template>
<div class="ps-0 ps-md-3 py-0 py-md-3">
  <VueTextSection v-for="(x, index) in news" :key="index" titleSize="h4">
    <template #title>{{ x.titel }}</template>
    <template #text>{{ x.text }}</template>
  </VueTextSection>
</div>
</VueTextSection> -->

    <VueTextSection>
      <template #title>About</template>
      <template #text>
        <p>
          A recent MICCAI paper [<a href="https://link.springer.com/chapter/10.1007/978-3-030-00937-3_45"
            target="_blank">Reinke, A. et al. (2018)</a>] showed that common practice in biomedical challenge
          organization can be exploited
          to tune challenge rankings. To prevent such incidences and to improve the quality of
          challenges, the
          <a href="https://miccai.org/index.php/special-interest-groups/challenges/" target="_blank">MICCAI Board
            Challenge Working Group (now:
            Special Interest Group (SIG) for Challenges)
          </a>
          and the MICCAI 2020 satellite event team decided to introduce the concept of challenge
          registration. Similar to how clinical trials have to be registered before starting, the
          complete design of accepted MICCAI challenges will be put online before the challenges
          take place. Changes to the design (e.g., to the metrics or ranking schemes applied) must
          be well-justified and officially be registered online (as a new version of the challenge
          design).
        </p>
        <p>
          To facilitate this process for the challenge organizers, this system has been updated in
          a way that allows for straightforward PDF export of the challenge design. The satellite
          event team will export the document and have it signed by the contact person of the
          challenge before uploading it on the submission system.
        </p>
        <p>
          Registering challenges is a big step towards higher quality challenges. It not only has
          the potential to lead to more thoughtful challenge designs but also provides all the
          information necessary for challenge participants. Furthermore, all changes will be
          transparent to the community, ensuring increased quality control.
        </p>
      </template>
    </VueTextSection>


    <VueTextSection>
      <template #title>Selection criteria</template>
      <template #text>
        <p>
          Due to the limited number of rooms available, and to remain relevant to the conference
          participants, the submitted challenge proposals will be selected based on the following
          criteria:
        </p>
        <ul>
          <li>Potential scientific, economic and social impact,</li>
          <li>Expected interest in the topic by the MICCAI audience,</li>
          <li>Quality of the challenge design.</li>
        </ul>
        <p>
          Proposals will be reviewed by at least two reviewers chosen based on their expertise in
          the area of a proposal. Reviewers will provide feedback and assist the challenge
          organizing committee in making a final decision. To ensure a rich and diverse program,
          we reserve the right to ask the applicants of proposals with substantial overlaps to
          merge or alter their scopes. We also reserve the right to ask applicants to provide
          supplementary materials and to revise their proposals in order to ensure the quality and
          standard of the MICCAI challenges.
        </p>
      </template>
    </VueTextSection>
    <VueTextSection>
      <template #title>Copyright</template>
      <template #text>Authors will assign to the MICCAI Society the right to distribute challenge materials
        (such as the agenda or the challenge design document) to MICCAI members and to challenge
        and conference attendees, independently of the copyright ownership planned by the
        challenge organizers.</template>
    </VueTextSection>
    <!-- <VueTextSection>
        <template #title>Budget</template>
        <template #text>MICCAI 2024 will not pay for travel arrangements or stipends for the organizers of
          satellite events nor provide concessions on registration fees. The MICCAI 2024 Satellite
          Events Committee has limited funds for waiving the registration fees for a number of
          speakers, including those from outside the MICCAI community. Organizers and speakers who
          only plan to attend the satellite event in which they are involved are expected to
          register for the event unless registration fee waivers have been requested and
          granted.</template>
      </VueTextSection> -->


  </div>
</template>

<script setup>
import VueTextSection from '@/components/VueTextSection.vue'
import { useAuthStore } from '@/stores/auth'
</script>
<script>
export default {
  computed: {
    userIsLoggedIn() {
      return useAuthStore().getUserLoginState
    },
  },
  data() {

    return {

      news: [
        {
          titel: 'News 1',
          text: 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.',
        },
        {
          titel: 'News 2',
          text: 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At',
        },
        {
          titel: 'News 3',
          text: 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.',
        },
        {
          titel: 'News 4',
          text: 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At',
        },
      ],
    }
  },
}
</script>
<style scoped></style>
