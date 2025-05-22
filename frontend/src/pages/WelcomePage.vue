<template>
  <div class="lh-base">

    <h3>Welcome to the MICCAI structured challenge submission system!</h3>

    <p>
      This framework will ensure the completeness of the information for a high-quality
      challenge review as well as structured access to the challenge information. Additionally,
      it may help organizers improve the design of their challenge.
    </p>


    <h3 class="pt-4"><i class="bi bi-send-check"></i> Challenge proposal submission procedure</h3>
    <p>Submitting a challenge proposal is done in <b>two</b> steps:</p>
    <p class="pt-2"> <b class="text-bg-warning p-1 rounded-2"><i class="bi bi-file-earmark-pdf h5"></i> Step 1:</b> <b>
        Create and download your
        'Challenge Design' file</b></p>
    <p class="ms-4">Register and login to the structured challenge submission system. Then create your
      proposal. Prepare the
      challenge design by providing at least 90% and all required challenge parameters in this structured submission
      system. (See the <router-link :to="{ name: 'Workflow' }">workflow</router-link> page for more details). Finally,
      generate and download your Challenge Design (PDF) file.
    </p>
    <p class="pt-2"><b class="text-bg-success p-1 rounded-2"><i class="bi bi-cloud-upload h5"></i> Step 2:</b>
      <b> Upload/Submit
        generated
        Challenge Design file to CMT</b>
    </p>
    <p class="ms-4">The Conference Management Toolkit (CMT),
      which is specialized in peer review processes, will be used for the review process. Submit the generated and
      <b>unchanged</b>
      Challenge Design (PDF) file to the review platform:<br> <a
        href="https://cmt3.research.microsoft.com/MICCAISAT2025/"
        target="_blank">https://cmt3.research.microsoft.com/MICCAISAT2025/</a>
    </p>

    <!-- <p>The list of challenge parameters can be downloaded:</p>
        <p>

          <a :href="Suppl_2_StructuredDescriptionOfAChallengeDesignPdf" target="_blank"
            class="btn btn-info text-nowrap shadow mb-3" type="button">
            <i class="bi bi-download"></i>
            <span class="ps-2">Download parameter description</span>
          </a>
        </p> -->
    <!-- <p>
          The description of the overall workflow can be found by signing in as a challenge
          organizer or reviewer. To get started, sign in or register to the submission system.
        </p> -->

    <h3 class="pt-4"><i class="bi bi-alarm"></i> Submission timeline for MICCAI 2025</h3>
    <ul>
      <li>Challenge proposals submission due: <span class="text-danger fw-bold">09 Jan 2025 11:59 PM
          Pacific
          Time, UTC -7</span> (equivalent to <span class="fst-italic fw-bold">10 Jan 2025 09:00 Central European Time,
          UTC +1</span> )
      </li>
      <li><span class="text-danger fw-bold">Challenge submissions for MICCAI 2025 are now closed. Please upload your
          Challenge Design (PDF) file to the CMT platform if you haven't already done so.</span></li>
      <!-- <li><span class="text-danger fw-bold">Please note:</span> Technical support will be provided until 09 Jan 2025
        8:59 AM Pacific Time (equivalent to <span class="fst-italic">9 Jan 2025 18:00 Central European Time</span> ) We
        recommend that you complete your submission a few days before the deadline.</li> -->
      <!-- <li>Feedback and decisions due: 00 Jan 2025 11:59 PM Pacific Time (PT, UTC -7) /  09:00 Central European Time (CET, UTC +1)</li> -->
      <!-- <li>Revised challenge proposals due: 23 February 2024</li> -->
      <!-- <ul>
            <li>Revised documents are generated in this structured submission system and the unchanged PDF is uploaded
              to
              CMT.
            </li>
            <li>Rebuttals, including all changes to the design PDF, are written in CMT.</li>
          </ul> -->

    </ul>
    <h3 class="pt-4"><i class="bi bi-play-btn"></i> Get started!</h3>
    <p>
      To get started, <router-link class="link-primary" :to="{ name: 'Registration' }">Register</router-link> or
      <router-link :to="{ name: 'Login' }">Login</router-link> to the submission system.
    </p>






  </div>

</template>
<script setup>
import { useAuthStore } from '@/stores/auth'
</script>
<script>
import Suppl_2_StructuredDescriptionOfAChallengeDesignPdf from '@/assets/Suppl_2_StructuredDescriptionOfAChallengeDesign.pdf';
export default {
  computed: {
    userIsLoggedIn() {
      return useAuthStore().getUserLoginState
    },
  },
  data() {

    return {
      Suppl_2_StructuredDescriptionOfAChallengeDesignPdf,

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
