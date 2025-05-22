<template>
  <div class="">
    <h1 class="text-center pb-4">Statistics</h1>
    <p>Several challenges have been proposed in the structured challenge submission system for multiple conferences. In
      this section, we will show statistics based on all (accepted) challenges in the system for MICCAI, ISBI and MIDL
      conferences.</p>
    <div class="pt-5 text-center">
      <div class="row pb-3 g-4">
        <div class="col-lg-4 col-md-6 ">
          <div class="card shadow h-100 p-1" style="">
            <lightbox-modal>
              <img :src="NumberOfChallenges" class="card-img-top" alt="Number of challenges">

              <div class="card-body">
                <p class="card-text small">Number of challenges that were accepted (red) or rejected (green).</p>
              </div>
            </lightbox-modal>
          </div>

        </div>
        <div class="col-lg-4 col-md-6">
          <div class="card shadow h-100 p-1" style="">
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
        <div class="col-lg-4 col-md-6">
          <div class="card shadow h-100 p-1" style="">
            <lightbox-modal>
              <img :src="FoA" class="card-img-top" alt="FoA">
              <div class="card-body">
                <p class="card-text small">Number of fields of application of accepted challenge tasks per year.</p>
              </div>
            </lightbox-modal>
          </div>
        </div>

        <div class="col-lg-4 col-md-6">
          <div class="card shadow h-100 p-1" style="">
            <lightbox-modal>
              <img :src="TaskCategories" class="card-img-top" alt="Task categories">
              <div class="card-body">
                <p class="card-text small">Number of task categories of accepted challenge tasks per year.</p>
              </div>
            </lightbox-modal>
          </div>
        </div>
        <div class="col-lg-4 col-md-6">
          <div class="card shadow h-100 p-1" style="">
            <lightbox-modal>
              <img :src="Modalities" class="card-img-top" alt="Modalities">
              <div class="card-body">
                <p class="card-text small">Number of imaging modalities of accepted challenge tasks.</p>
              </div>
            </lightbox-modal>
          </div>
        </div>
        <div class="col-lg-4 col-md-6">
          <div class="card shadow h-100 p-1" style="">
            <lightbox-modal>
              <img :src="NumberOfData" class="card-img-top" alt="Number of data">
              <div class="card-body">
                <p class="card-text small">Number of training (green) and test (red) cases of accepted challenge tasks.
                  The
                  plots are shown on a log scale.</p>
              </div>
            </lightbox-modal>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>
<script>
import LightboxModal from '@/components/LightboxModal.vue'
import NumberOfChallenges from '@/assets/images/statistics/NumberOfChallenges.png';
import NumberOfTasks from '@/assets/images/statistics/NumberOfTasks.png';
import FoA from '@/assets/images/statistics/FoA.png';
import TaskCategories from '@/assets/images/statistics/TaskCategories.png';
import Modalities from '@/assets/images/statistics/Modalities.png';
import NumberOfData from '@/assets/images/statistics/NumberOfData.png';


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