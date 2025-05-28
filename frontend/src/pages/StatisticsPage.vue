<template>
  <div class="">
    <h1 class="text-center pb-4">Statistics</h1>
    <p>Several challenges have been proposed in the structured challenge submission system for multiple conferences. In
      this section, we will show statistics based on all (accepted) challenges in the system for MICCAI, ISBI and MIDL
      conferences.</p>
    <div class="pt-5 text-center">
      <div class="row pb-3 g-4">
        <div class="col-12 col-lg-8 ">
          <div
            class="d-flex flex-md-row flex-column align-items-center align-items-md-stretch justify-content-lg-between justify-content-center">
            <div class="card shadow p-1 m-2 flex-fill" style="max-width: 19rem; min-width: 19rem;">
              <lightbox-modal>
                <img :src="NumberOfChallenges" class="card-img-top" alt="Number of challenges">

                <div class="card-body">
                  <p class="card-text small">Number of challenges that were accepted (red) or rejected (green).</p>
                </div>
              </lightbox-modal>
            </div>



            <div class="card shadow p-1 m-2" style="max-width: 19rem; min-width: 19rem;">
              <lightbox-modal>
                <img :src="NumberOfTasks" class="card-img-top" alt="Number of tasks">
                <div class="card-body">
                  <p class="card-text small">Number of tasks/sub-challenges of accepted challenges. The density of the
                    number of
                    tasks is visualized by a violin plot per year.</p>
                </div>
              </lightbox-modal>
            </div>

          </div>
          <div
            class="d-flex flex-md-row flex-column align-items-center align-items-md-stretch justify-content-lg-between justify-content-center">
            <div class="card shadow p-1 m-2" style="max-width: 19rem; min-width: 19rem;">
              <lightbox-modal>
                <img :src="FoA" class="card-img-top" alt="FoA">
                <div class="card-body">
                  <p class="card-text small">Number of fields of application of accepted challenge tasks per year.</p>
                </div>
              </lightbox-modal>
            </div>


            <div class="card shadow p-1 m-2" style="max-width: 19rem; min-width: 19rem;">
              <lightbox-modal>
                <img :src="TaskCategories" class="card-img-top" alt="Task categories">
                <div class="card-body">
                  <p class="card-text small">Number of task categories of accepted challenge tasks per year.</p>
                </div>
              </lightbox-modal>
            </div>
          </div>
          <div
            class="d-flex flex-md-row flex-column align-items-center align-items-md-stretch justify-content-lg-between justify-content-center">
            <div class="card shadow  p-1 m-2" style="max-width: 19rem; min-width: 19rem;">
              <lightbox-modal>
                <img :src="Modalities" class="card-img-top" alt="Modalities">
                <div class="card-body">
                  <p class="card-text small">Number of imaging modalities of accepted challenge tasks.</p>
                </div>
              </lightbox-modal>
            </div>

          </div>

        </div>
        <div class="col-12 col-lg-4">
          <div
            class="d-flex flex-md-row flex-column align-items-center align-items-md-stretch justify-content-lg-between justify-content-center">
            <div class="card shadowp-1 m-2 flex-fill" style="max-width: 19rem; min-width: 19rem;">
              <lightbox-modal>
                <img :src="NumberOfData" class="card-img-top" alt="Number of data">
                <div class="card-body">
                  <p class="card-text small">Number of training (green) and test (red) cases of accepted challenge
                    tasks.
                    The
                    plots are shown on a log scale.</p>
                </div>
              </lightbox-modal>
            </div>
          </div>

        </div>
      </div>

    </div>
  </div>
</template>
<script>
import LightboxModal from '@/components/LightboxModal.vue'
import NumberOfChallenges from '@/assets/images/statistics/NumberOfChallenges_Stati_white.png';
import NumberOfTasks from '@/assets/images/statistics/NumberOfTasks_white.png';
import FoA from '@/assets/images/statistics/FoA_white.png';
import TaskCategories from '@/assets/images/statistics/TaskCategories_weight.png';
import Modalities from '@/assets/images/statistics/Modalities_white.png';
import NumberOfData from '@/assets/images/statistics/NumberOfData_white.png';


export default {
  name: 'StatisticsPage',
  components: { LightboxModal },
  data() {
    return {
      NumberOfChallenges, NumberOfTasks, FoA, TaskCategories, Modalities, NumberOfData
    };
  },
};
</script>