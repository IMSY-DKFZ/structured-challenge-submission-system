<template>
  <div>
    <div class="row gx-5">
      <div class="col-md-12 col-lg-4 order-lg-last lh-sm pb-5" id="">
        <StickySidebar>
          <div class=" " style="">

            <div class="card bg-body-tertiary p-2 d-flex gap-2" style="box-shadow: 0 0 10px rgba(0, 0, 0, 0.15);">
              <h5 class="text-center m-0">Categories</h5>
              <ul class="list-group mb-3 ">
                <!-- <button v-for="(item, idx) in contentTabs" :key="item.formName" @click="selectTab(idx)"
              class="list-group-item list-group-item-action d-flex justify-content-between align-items-center lh-sm"
              :class="[
                item.progress >= this.neededPercentages
                  ? isActive(idx)
                    ? 'active border-success'
                    : 'list-group-item-success'
                  : item.hasError
                    ? isActive(idx)
                      ? 'list-group-item-danger border-danger border-2'
                      : 'list-group-item-danger'
                    : isActive(idx)
                      ? 'active'
                      : !isNaN(item.progress) ? 'list-group-item-warning' : 'list-group-item-success',
              ]"> -->
                <button v-for="(item, idx) in contentTabs" :key="item.formName" @click="selectTab(idx)"
                  class="list-group-item list-group-item-action d-flex justify-content-between align-items-center lh-sm"
                  :class="[isActive(idx) ? ' fw-bold border border-dark-subtle' : '', item.hasError || (isNaN(item.progress) && item.useTaskForm) ? 'list-group-item-danger border-danger border-1' : (!isNaN(item.progress) && item.progress >= this.neededPercentages) ? 'list-group-item-success' : 'list-group-item-warning'].join(' ')">
                  <div>
                    <h6 class="my-0">{{ item.formName }}</h6>
                  </div>
                  <div>
                    <div v-if="item.hasError || (isNaN(item.progress) && item.useTaskForm)">
                      <i class="bi bi-exclamation-triangle-fill"></i>
                    </div>
                    <span v-else><span v-if="!isNaN(item.progress)">{{ item.progress }}%</span>
                    </span>
                  </div>
                </button>

              </ul>
              <h5 class="text-center m-0">Proposal Status</h5>
              <div class="card d-flex justify-content-between " :class="[
                this.returnFormProgress >= this.neededPercentages ? 'bg-success-subtle' : 'bg-warning-subtle']">
                <div class="card-body">


                  <!-- <strong>{{ returnFormProgress }}%</strong> -->
                  <div v-if="this.returnFormProgress >= this.neededPercentages" class="d-flex justify-content-between">
                    <div>
                      <p>Ready to be generated</p>
                      <p class="muted small">
                        At least {{ neededPercentages }}% of
                        the required<span class="text-danger">*</span> fields filled in
                        each category.
                      </p>
                      <p class="muted small">
                        The proposal is ready to be generated.
                      </p>
                    </div>
                    <div>✔️</div>
                  </div>
                  <div v-else class="d-flex justify-content-between">
                    <div>
                      <p>Missing mandatory fields</p>
                      <p class="muted small">
                        To submit a proposal, you must create at least one task and complete {{ neededPercentages }}% of
                        the required<span class="text-danger">*</span> fields in each category.
                      </p>

                    </div>

                    <div>⚠️</div>
                  </div>




                  <!--
          <p class="muted small">
            Questions not marked as required<span class="text-danger">*</span> count as completed.
          </p>
          -->


                </div>
              </div>
              <div class="py-0">
                <AutoSaveInterval :timeout="30000" :show="canSaveProposal" @end-of-time-period="saveProposal" />
              </div>

              <button :disabled="!canSaveProposal" class="btn btn-success" @click="saveProposal(showMessage = true)">
                <i class="bi bi-floppy"></i><span class="ps-2">Save proposal</span>
              </button>
              <button :disabled="!canSubmitProposal" class="btn btn-primary" data-bs-toggle="modal"
                data-bs-target="#submitProposalPopup">
                <i class="bi bi-send-arrow-down"></i> Generate proposal</button>
              <!-- <button class="btn btn-outline-danger" @click="resetProposal">
              Reset proposal
            </button> -->
            </div>
          </div>
        </StickySidebar>
      </div>
      <div class="col-md-12 col-lg-8 mb-5 " id="content">
        <div class="alert alert-secondary bg-body-tertiary text-center py-2 mb-3 fw-semibold" role="alert">
          <i class="bi bi-info-circle"></i> We recommend keeping a local copy of the content you create here.
        </div>
        <div v-for="(tab, index) in contentTabs" :key="tab + index">
          <div v-show="isActive(index)">
            <h2 class="mb-3">{{ tab.formName }}</h2>
            <div v-if="tab.useTaskForm">
              <TaskForm :name="tab.formName" :show-action-btn="false"></TaskForm>
              <div class="card p-3 bg-light-subtle" :hidden="!taskAvailable">
                <h3><i class="bi bi-file-earmark-text"></i> Fill task details: <br /><br /></h3>

                <VueForm v-if="taskAvailable" :show-missing-input-top="true" :name="tab.formName" :ref="tab.formName"
                  :show-action-btn="false">
                  <VueTextSection :show-missing-input-top="true" title-size="h4"
                    v-for="(question, index) in tab.questions" :key="question.key">
                    <!-- <template #title>{{ index + 1 }}) {{ question.title }}</template> -->
                    <template #title>{{ question.title }}<small v-if="question.validation.required"
                        class="text-danger"><b>*</b></small></template>

                    <template #text>
                      <div v-html="question.text"></div>
                    </template>
                    <VueInput @errorState="updateErrorState" v-for="(task, index) in question.value"
                      :key="`taskId${task.task_name + index}`" :questionKey="question.key"
                      :uniqueId="question.value[index].uniqueId" :label="`<span class='badge bg-dark me-1'>Task ${index
                        + 1}</span>`" :has-error="question.value[index].errorState" :type="question.type"
                      :options="question.options" :text-min-length="question.validation.minlength"
                      :text-max-length="question.validation.maxlength" :required="question.validation.required"
                      :allow-special-characters="question.validation.allowSpecialCharacters" :icon="question.icon"
                      v-model="question.value[index].value" @input=question.input>
                    </VueInput>
                  </VueTextSection>
                </VueForm>
              </div>
            </div>
            <div v-else>
              <VueForm :ref="tab.formName" :name="tab.formName" :show-action-btn="false">
                <VueTextSection title-size="h4" v-for="question in tab.questions" :key="question.key">
                  <template #title>{{ question.title }}<small v-if="question.validation.required"
                      class="text-danger"><b>*</b></small></template>
                  <template #text>
                    <div v-html="question.text"></div>
                  </template>
                  <VueInput @errorState="updateErrorState" :questionKey="question.key" :label="question.label"
                    :has-error="question.errorState" :type="question.type" :options="question.options"
                    :text-min-length="question.validation.minlength" :text-max-length="question.validation.maxlength"
                    :required="question.validation.required"
                    :allow-special-characters="question.validation.allowSpecialCharacters" :icon="question.icon"
                    v-model="question.value"></VueInput>
                </VueTextSection>
              </VueForm>
            </div>
          </div>
        </div>
        <div class="d-flex gap-5 my-5 justify-content-between align-content-center">
          <button :disabled="activeTab === 0" @click="activeTab--" type="button" class="btn btn-lg w-25"
            :class="activeTab === 0 ? 'btn-outline-light' : 'btn-outline-primary'">
            <i class="bi bi-arrow-left"></i>Back
          </button>
          <button :disabled="(activeTab === contentTabs.length - 1) || (activeTab === 2 && !taskAvailable)"
            @click="activeTab++" type="button" class="btn btn-lg w-25"
            :class="activeTab === contentTabs.length - 1 ? 'btn-outline-light' : 'btn-outline-primary'">
            Next<i class="bi bi-arrow-right"></i>
          </button>
        </div>
      </div>
    </div>
    <!-- Modal -->
    <div class="modal fade" id="submitProposalPopup" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
      aria-labelledby="submitProposalPopupLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-light-subtle">
            <h1 class="modal-title fs-5" id="submitProposalPopupLabel">Important note</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">

            <!-- <div v-html="proposalConferenceSubmitMessage"></div> -->
            <p>Thank you for preparing your structured challenge design document.</p>
            <p>Once generated, you will be able to download the PDF file. It will also be sent by e-mail.</p>
            <p>Please download your PDF file and upload it to the CMT link provided.</p>


          </div>

          <div class="modal-footer bg-light-subtle">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button class="btn btn-primary" data-bs-dismiss="modal" @click="submitProposal">
              <i class="bi bi-send-arrow-down"></i> Generate proposal file</button>
          </div>
        </div>
      </div>
    </div>




    <!-- <popup-modal ref="submitProposalPopup">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Important note</h5>
          </div>
          <div class="modal-body lh-sm py-3">
            <p>Thanks for preparing your structured challenge design document. Please download the PDF generated by this
              system and upload it (unchanged!) to the review platform (<a target="_blank" href="https://cmt3.research.microsoft.com/MICCAISAT2024/">CMT</a>).</p>
            <p><i>Note:</i> Uploading a challenge design document to <a target="_blank" href="https://cmt3.research.microsoft.com/MICCAISAT2024/">CMT</a> that is incomplete or different from the one
              generated with the structured submission system will lead to a <b>desk rejection</b> of the challenge.</p>
            <slot></slot>
          </div>
          <div class="modal-footer d-flex justify-content-between">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button class="btn btn-primary" @click="submitProposal">
              <i class="bi bi-send-arrow-down"></i> Generate proposal file
            </button>

          </div>
        </div>
      </div>
    </popup-modal> -->
  </div>
</template>
<script>
import VueInput from '@/components/essentials/VueInput.vue'
import VueForm from '@/components/essentials/VueForm.vue'
import StickySidebar from '@/components/essentials/StickySidebar.vue'
import VueTextSection from '@/components/VueTextSection.vue'
import { useProposalStore } from '@/stores/proposal'
import { storeToRefs } from 'pinia'
import TaskForm from '@/components/proposal/TaskForm.vue'
import AutoSaveInterval from '@/components/AutoSaveInterval.vue'
import { apiPost, apiPut } from '@/api/api'
import { useToastAlertStore } from '@/stores/toastAlert'
// import ConfirmDialogue from '@/components/ConfirmDialogue.vue'
// import PopupModal from '@/components/PopupModal.vue'

const proposalStore = useProposalStore()
const { proposal, tasks } = storeToRefs(proposalStore)



export default {

  name: 'ProposalTemplate',
  props: {
    tabs: {
      typ: Array,
      default: () => [],
    },
  },
  components: { AutoSaveInterval, TaskForm, VueForm, VueInput, VueTextSection, StickySidebar },
  mounted() {
    // Use Vue's $el to get the current component's element
    window.addEventListener('scroll', () => {
      this.windowTop = this.$el.scrollTop;
    });

  },

  computed: {

    taskAvailable() {
      return proposalStore.getTasks.length > 0
    },
    proposalConferenceSubmitMessage() {
      let proposalConference = proposalStore.getProposalConference
      return proposalConference['submitMessage']
    },
    canSaveProposal() {
      // return this.proposalContainsError
      return true
    },
    canSubmitProposal() {
      //TO BE set later by the admin
      //check for missing input on required fields
      //check if progress fits percentage
      const tasksLength = tasks.value.length


      // return tasksLength === 0
      //   ? false
      //   : !(this.proposalContainsError
      //     ? proposalStore.isInputStillRequired
      //       ? false
      //       : this.userReachedNeededPercentages
      //     : false)


      // if (tasksLength === 0 ||
      //   !this.userReachedNeededPercentages ||
      //   this.proposalContainsError ||
      //   proposalStore.isInputStillRequired) {
      //   return false;
      // }
      if (tasksLength === 0 ||
        !this.userReachedNeededPercentages ||
        this.proposalContainsError) {
        return false;
      }

      return true;

    },
    userReachedNeededPercentages() {
      return this.returnFormProgress >= this.neededPercentages
    },
    returnFormProgress() {
      let progressList = []
      this.contentTabs.forEach(item => { if (item.hasOwnProperty('progress')) { progressList.push(item.progress) } })
      return Math.min(...progressList)
    },
    returnFormProgressOLD() {
      // let amountOfForms = this.contentTabs.length * 100
      let amountOfForms = 0
      this.contentTabs.flatMap(tab => {
        if (!tab.useTaskForm) {
          amountOfForms = amountOfForms + tab.questions.flatMap(y =>
            y.validation && y.validation.required).reduce(function (a, b) {
              return a + b;
            }, 0);
        } else {
          amountOfForms = amountOfForms + tab.questions.flatMap(question =>
            question.value.flatMap(y => y.validation && y.validation.required)).reduce(function (a, b) {
              return a + b;
            }, 0);
        }
      })


      // let amountOfForms = this.contentTabs.reduce((total, tab) => {
      //   const requiredQuestions = tab.questions.filter(question => question.validation && question.validation.required);
      //   return total + requiredQuestions.length;
      // }, 0);
      // totalAmountOfForms = totalAmountOfForms + amountOfForms

      // let sum = this.contentTabs
      //   .map((x) => (!isNaN(x.progress) ? x.progress : 0))
      //   .reduce(function (a, b) {
      //     return a + b;
      //   });
      let sum = 0
      this.contentTabs.flatMap(tab => {
        if (!tab.useTaskForm) {
          sum = sum + tab.questions.flatMap(y =>
            y.mapIsAnswered).reduce(function (a, b) {
              return a + b;
            }, 0);
        } else {
          sum = sum + tab.questions.flatMap(question =>
            question.value.flatMap(y => y.mapIsAnswered)).reduce(function (a, b) {
              return a + b;
            }, 0);
        }
      })




      return Math.round((sum / amountOfForms) * 100)
    },
    proposalContainsError() {
      return this.contentTabs.map((x) => x.hasError).includes(true)
    },
    contentTabs() {
      return proposal
        ? proposal.value.map((x, idx) => {
          return {
            ...x,
            hasError: x.questions.map((i) => i.errorState).includes(true),
            progress: this.returnProgress(x),
            active: this.activeTab === idx,
          }
        })
        : []
    },
  },
  watch: {
    activeTab() {
      window.scrollTo({
        top: 0,
        left: 0,
        behavior: "smooth",
      })
      sessionStorage.setItem('editProposalActiveTab', this.activeTab);

    },
  },
  created() {
    this.activeTab = parseInt(sessionStorage.getItem('editProposalActiveTab')) || 0
  },
  data() {
    return {
      activeTab: 0,
      neededPercentages: 90,
      proposalContainer: {},
      tasksContainer: [],
      windowTop: 0,
    }
  },
  methods: {


    async submitProposal() {
      if (proposalStore.getProposalId) {
        await this.saveProposal()
        setTimeout(1000);
        await apiPut(`/challenge/${proposalStore.getProposalId}/submit`, {
          accept: 'application/json',
        })
          .then(() => {
            this.$router.push({ name: 'Proposals' })
            useToastAlertStore().showAlert('Challenge proposal submitted successfully. You can download your submission file.', 'success', 6000);


          })
          .catch((e) => {
            this.$router.push({ name: 'Proposals' })
            useToastAlertStore().showAlert(e, 'danger', 6000);

          });

      }
    },


    async saveProposal(showMessage = false) {
      if (proposalStore.getProposalId) {
        // let taskCreated = false;
        proposalStore.proposal.forEach(async (proposalItem, index) => {
          let container = {};
          proposalItem.questions.forEach((x) => {
            // if (x.type === 'text' && x.convertToList && x.value.length > 0 && !Array.isArray(x.value)) {
            if (x.type === 'text' && x.convertToList && !Array.isArray(x.value)) {
              if (x.value !== null) {
                x.value = x.value.split(',').map(item => item.trim());
              } else {
                x.value = [];
              }

            } else if (proposalItem.useTaskForm && x.convertToList) {
              for (let i = 0; i < x.value.length; i++) {
                if (x.value[i].type === 'text' && x.value[i].convertToList && !Array.isArray(x.value[i].value)) {
                  if (x.value[i].value !== null) {
                    x.value[i].value = x.value[i].value.split(',').map(item => item.trim());
                  } else {
                    x.value[i].value = [];
                  }
                }
              };
            }
            container[x.key] = x.value;
          });

          if (proposalItem.formName === 'Tasks') {

            let taskNames = container.task_name;
            const taskList = proposalStore.getTasks
            for (let i = 0; i < taskNames.length; i++) {
              let subcontainer = {};
              for (let key in container) {
                subcontainer[key] = container[key][i].value;
              };
              const taskId = taskList[i].id


              const taskItemIndex = taskList.findIndex(task => task.id === taskId);
              if (taskItemIndex !== -1) {
                // Task found, update existing task

                // this.tasksContainer[taskItemIndex] = subcontainer;
                // let taskId = this.tasksContainer[taskItemIndex].id;
                await apiPut(`/task/${taskId}/update`, subcontainer, {
                  accept: 'application/json',
                })
                  .then(() => {
                    // if (!autoSave) {
                    //   useToastAlertStore().showAlert('Task updated successfully.', 'success');
                    // }
                  })
                  .catch((e) => {
                    useToastAlertStore().showAlert(e, 'danger', 6000);
                  });
              }
            }
          } else {
            // Handle non-task proposal
            this.proposalContainer = container;
            await apiPut(`/challenge/${proposalStore.getProposalId}/update`, container, {
              accept: 'application/json',
            })
              .then(() => {
                if (showMessage) {
                  useToastAlertStore().showAlert('Challenge proposal updated successfully.', 'success');
                }

              })
              .catch((e) => {
                useToastAlertStore().showAlert(e, 'danger', 6000);
              });
          }
          // if (taskCreated) {
          // setTimeout(500);
          // location.reload()
          // setTimeout(500);
          // this.activeTab = 2
          // }
        });
      }
    },



    resetProposal() {
      proposalStore.newProposal()
    },
    returnProgress(form) {
      const tasksLength = tasks.value.length
      //return 0 of input is needed or false, 1 if no further input is needed
      if (form.useTaskForm) {
        const requiredQuestions = form.questions
          .flatMap(question => (question.value || []).filter(subQuestion => subQuestion.validation && subQuestion.validation.required));
        const questionLength = requiredQuestions.length || 0;
        const mapIsAnswered = form.questions.map((x) => {
          if (tasksLength === 0) {
            x.value.forEach((y) => y.mapIsAnswered = 0);
            x.errorState = true
          } else if (x.errorState || !x.validation.required) {
            x.value.forEach((y) => y.mapIsAnswered = 0);
          } else if (Array.isArray(x.value)) {
            // x.value.forEach((y) => y.mapIsAnswered = 0);
            x.value.map((y) => (y.value === '' || y.value === null) ? y.mapIsAnswered = 0 : y.mapIsAnswered = 1)
          } else if (typeof x.value === 'string' && x.value === '') {
            x.value.forEach((y) => y.mapIsAnswered = 0);
          } else if (x.value.some((y) => Array.isArray(y.value) && y.value.includes(null))) {
            x.value.forEach((y) => y.mapIsAnswered = 0);
          } else {
            x.value.forEach((y) => y.mapIsAnswered = 1);
          }

          return x.value.map(y => y.mapIsAnswered);
        });



        let sum = mapIsAnswered.flat().reduce(function (a, b) {
          return a + b;
        }, 0);

        return Math.round((sum / questionLength) * 100);
      } else {
        const requiredQuestions = form.questions.filter(question => question.validation && question.validation.required);
        const questionLength = requiredQuestions.length || 0;
        if (questionLength > 0) {
          const mapIsAnswered = form.questions.map((x) => {
            if (
              x.errorState ||
              !x.validation.required ||
              (Array.isArray(x.value) && x.value.every(value => value === '')) ||
              (typeof x.value === 'string' && x.value === '')
            ) {
              x.mapIsAnswered = 0;
            } else {
              x.mapIsAnswered = 1;
            }
            return x.mapIsAnswered;
          });
          let sum = mapIsAnswered.reduce(function (a, b) {
            return a + b
          }, 0)
          return Math.round((sum / questionLength) * 100);
        }
        else { return 100 }
      }
    },
    updateErrorState(obj) {
      let indexOfTask = null
      proposal.value.forEach((form) => {
        form.questions.forEach((question) => {
          if (form.formName === 'Tasks') {
            if (question.value.map((x) => x.questionKey).includes(obj.questionKey)) {
              indexOfTask = question.value.map((y) => y.uniqueId).indexOf(obj.uniqueId)
              question.value[indexOfTask].errorState = obj.value
            }
          }
          if (question.key === obj.questionKey || obj.questionKey.includes(question.key)) {
            question.errorState =
              indexOfTask !== null
                ? question.value.map((item) => item.errorState).includes(true)
                : obj.value
          }
        })
      })
    },
    selectTab(index) {
      this.activeTab = index
    },
    isActive(idx) {
      return this.contentTabs[idx].active
    },
  }

}
</script>

<style scoped>
[data-bs-theme="dark"] {
  --list-group-bg: #ffffff;
  --bs-list-group-bg: #ffffff;
}
</style>
