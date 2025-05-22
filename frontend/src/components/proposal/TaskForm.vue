<template>
  <div>
    <!-- <VueForm :action-btn-fullwidth="false" action-btn="Create a task" @submit="createTask" name="createTask"
      class="card p-3 bg-light">
      <VueTextSection size="h6">
        <template #title>
          <h4><i class="bi bi-plus-square"></i> Create your task(s):</h4>
        </template>
<template #text>
          <p><b>Task</b>: A challenge may deal with multiple different tasks for which separate assessment
            results are provided. For example, a challenge may target the problem of segmentation of
            human organs in computed tomography (CT) images. It may include several tasks
            corresponding to the different organs of interest.</p>
          <div class="alert alert-primary">
            <i class="bi bi-info-circle"></i> <b>Tip</b>: Our recommendation is to create all tasks first and then fill
            in the necessary information. This way you can complete everything in one step and save time.
          </div>


        </template>
<VueInput v-model="newTaskName" type="textarea" label="Enter task name here" text-max-length="100" :required="true"
  text-min-length="2"></VueInput>
</VueTextSection>


<div class="alert alert-danger" v-if="errorMessage" role="alert">
  {{ errorMessage }}
</div>
</VueForm> -->
    <!--  -->
    <div class="accordion mb-3" id="accordionCreateTask">
      <div class="accordion-item bg-light-subtle border-success-subtle">
        <h2 class="accordion-header">
          <button class="accordion-button bg-success-subtle" :class="{ 'collapsed': taskAvailable }" type="button"
            data-bs-toggle="collapse" data-bs-target="#collapseAccordionCreateTask" aria-expanded="false"
            aria-controls="collapseAccordionCreateTask">
            <h4><i class="bi bi-plus-square"></i> Create your task(s):</h4>
          </button>
        </h2>
        <div id="collapseAccordionCreateTask" class="accordion-collapse collapse" :class="{ 'show': !taskAvailable }"
          data-bs-parent="#accordionCreateTask">
          <div class="accordion-body">
            <VueForm :action-btn-fullwidth="false" action-btn="Create a task" @submit="createTask" name="createTask"
              class="">
              <VueTextSection size="h6">
                <template #text>
                  <p><b>Task</b>: A challenge may deal with multiple different tasks for which separate assessment
                    results are provided. For example, a challenge may target the problem of segmentation of
                    human organs in computed tomography (CT) images. It may include several tasks
                    corresponding to the different organs of interest.</p>
                  <div class="alert alert-primary">
                    <i class="bi bi-info-circle"></i> <b>Tip</b>: Our recommendation is to create all tasks first and
                    then fill
                    in the necessary information. This way you can complete everything in one step and save time.
                  </div>
                </template>
                <VueInput v-model="newTaskName" type="textarea" label="Enter task name here" text-max-length="100"
                  :required="true" text-min-length="2"></VueInput>
              </VueTextSection>
              <div class="alert alert-danger" v-if="errorMessage" role="alert">
                {{ errorMessage }}
              </div>
            </VueForm>

          </div>
        </div>
      </div>
    </div>

    <!--  -->
    <!-- <div class="mb-3 card bg-danger-subtle" :hidden="!taskAvailable">
      <div class="card-header text-danger">
        <h4><i class="bi bi-exclamation-triangle-fill"></i> Delete task(s):</h4>
      </div>
      <div class="card-body">
        <p>You can delete your tasks here. Please note that, this is an <b>irreversible</b> action! All of the
          data will be deleted <b>permanently</b>.</p>

        <div class="px-3 py-1 my-2 d-flex justify-content-between align-items-center"
          v-for="(task, index) in proposalStore.tasks" :key="task.task_name">
          <div><span class='badge bg-danger fs-6 p-2 pt-1 '>Task {{ index + 1 }} :</span> {{ task.task_name }}</div>
          <button class="btn btn-danger me-2" @click="deleteTask(task.id, task.task_name)">
            <i class="bi bi-trash2-fill"></i>
          </button>
        </div>
      </div>
    </div> -->


    <div class="accordion mb-3" id="accordionDeleteTask" :hidden="!taskAvailable">
      <div class="accordion-item bg-danger-subtle border-danger-subtle">
        <h4 class="accordion-header">
          <button class="accordion-button collapsed bg-danger-subtle text-danger" type="button"
            data-bs-toggle="collapse" data-bs-target="#collapseAccordionDeleteTask" aria-expanded="false"
            aria-controls="collapseAccordionDeleteTask">
            <h4><i class="bi bi-exclamation-triangle-fill"></i> Delete task(s):</h4>
          </button>
        </h4>
        <div id="collapseAccordionDeleteTask" class="accordion-collapse collapse" data-bs-parent="#accordionDeleteTask">
          <div class="accordion-body">
            <p>You can delete your tasks here. Please note that, this is an <b>irreversible</b> action! All of the
              data will be deleted <b>permanently</b>.</p>

            <div class="px-3 py-1 my-2 d-flex justify-content-between align-items-center"
              v-for="(task, index) in proposalStore.tasks" :key="task.task_name">
              <div><span class='badge bg-danger fs-6 p-2 pt-1 '>Task {{ index + 1 }} :</span> {{ task.task_name }}</div>
              <button class="btn btn-danger me-2" @click="deleteTask(task.id, task.task_name)">
                <i class="bi bi-trash2-fill"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>



    <confirm-dialogue ref="confirmDialogue"></confirm-dialogue>
  </div>
</template>

<script setup>
import VueForm from '@/components/essentials/VueForm.vue'
import VueInput from '@/components/essentials/VueInput.vue'
import VueTextSection from '@/components/VueTextSection.vue'
import ConfirmDialogue from '@/components/ConfirmDialogue.vue'
</script>
<script>
import { useProposalStore } from '@/stores/proposal'
import { storeToRefs } from 'pinia'
const proposalStore = useProposalStore()
const { tasks } = storeToRefs(proposalStore)
import { apiDelete, apiGet, apiPut, apiPost } from '@/api/api'
// import { useToastAlertStore } from '@/stores/toastAlert'
import { useToastAlertStore } from '@/stores/toastAlert'
export default {
  name: 'TaskForm',
  props: {
    form: {
      typ: Array,
      default: () => [],
    },
  },
  data() {
    return {
      newTaskName: '',
      errorMessage: '',
    }
  },
  computed: {
    taskAvailable() {
      return tasks.value.length > 0
    },
  },
  methods: {
    async createTask() {
      if (tasks.value.map((x) => x.task_name).includes(this.newTaskName)) {
        this.errorMessage = 'Task name already exists, pls try another one'
      } else {

        let task_name = this.newTaskName
        let task_challenge_id = proposalStore.getProposalId
        if (typeof task_name === 'string' && task_name.length > 0) {
          await apiPost(`/task/create?challenge_id=${task_challenge_id}`, { "task_name": task_name }, {
            accept: 'application/json',
          })
            .then(() => {
              proposalStore.createTask(task_name)
              this.errorMessage = ''
              this.newTaskName = ''
              useToastAlertStore().showAlert('Task created successfully.', 'success');
              setTimeout(1000);
              location.reload();
            })
            .catch((e) => {
              useToastAlertStore().showAlert(e, 'danger', 6000);
            })
        };



      }
    },
    async deleteTask(id, name) {

      const ok = await this.$refs.confirmDialogue.show({
        title: 'Delete task',
        message: 'Are you sure you want to delete this task? It cannot be undone.',
        okButton: 'Delete task forever',
        okButtonTheme: 'btn-danger',
      })
      if (ok) {
        await apiDelete(
          `task/${id}/delete`
        )
          .then(() => {
            proposalStore.deleteTask(name)
            useToastAlertStore().showAlert('The task was deleted', 'success')
            setTimeout(1000);
            location.reload()

          })
          .catch((e) => {
            useToastAlertStore().showAlert(e, 'danger')
          })



      }
    },
  },
}
</script>

<style scoped></style>
