<template>
  <div>
    <div class="d-flex justify-content-between" :class="[dataSelected ? 'flex-column' : '']">
      <div class="pb-3"><collapse-section name="info">
          <VueTextSection>
            <template #text>
              <p>
                In this view, you can see all users (including yourself). For more details, press the
                show details button below.<br />
                As an administrator you can change the roles of users. Following roles exist in the
                system:
              </p>
              <ul>
                <li>
                  <span class="text-info fw-bold">Administrator:</span> This is your role. You see all
                  challenges and all users. You can allocate roles to each user, delete users and
                  restore deleted challenges. Besides, it is your duty to assign challenges to
                  reviewers.
                </li>
                <li>
                  <span class="text-info fw-bold">Sub-Administrator:</span> The sub-administrator is
                  reserved for the MICCAI board members. They have many rights, but they can not
                  delete users or challenges due to privacy constraints.
                </li>
                <li>
                  <span class="text-info fw-bold">Organizer:</span> The organizer can create challenge
                  proposals.
                </li>
              </ul>
              <p>
                In some cases a user might want to be deleted. You can do this by pressing the delete
                user button. It will remove the user, his challenges and related data from the
                database.<br />
                In case that the email service is not available, users might forget their passwords.
                Only if the user asks you to reset the password, you are allowed to use the button
                below!
              </p>
            </template>
          </VueTextSection>
        </collapse-section></div>
      <p v-if="dataSelected">
        <router-link type="button" class="btn btn-secondary" @click="unselectData" :to="{ name: 'Users' }">
          <i class="be bi-arrow-left pe-1" />
          Go Back
        </router-link>
      </p>
    </div>
    <div v-if="dataSelected">
      <VueTextSection>
        <div class="row">
          <div class="row col-12 mb-3 p-3">
            <div class="col-12 col-md-4 mb-3">
              <h6 class="mb-0">Email address</h6>
              <div class="mb-3 opacity-75">{{ dataSelected?.email }}</div>
            </div>
            <div class="col-12 col-md-1 mb-3">
              <h6 class="mb-0">ID</h6>
              <div class="mb-3 opacity-75">{{ dataSelected?.id }}</div>
            </div>
            <div class="col-12 col-md-3 mb-3">
              <h6 class="mb-0">Disabled?</h6>
              <div class="mb-3 opacity-75" style="text-transform: capitalize">{{ dataSelected?.disabled }}</div>
            </div>

            <div class="col-12 col-md-4 mb-3">
              <h6 class="mb-0">Roles</h6>
              <div class="mb-3 opacity-75">
                <span v-for="role in dataSelected?.roles" :key="role" class="badge text-bg-primary me-1">{{ role
                }}</span>
              </div>
            </div>
            <div class="col-12 col-md-4 mb-3">
              <h6 class="mb-0">Full name</h6>
              <div class="mb-3 opacity-75">{{ dataSelected?.first_name }} {{ dataSelected?.last_name }}</div>
            </div>
            <div class="col-12 col-md-4 mb-3">
              <h6 class="mb-0">City</h6>
              <div class="mb-3 opacity-75">{{ dataSelected?.city }}</div>
            </div>
            <div class="col-12 col-md-4 mb-3">
              <h6 class="mb-0">Country</h6>
              <div class="mb-3 opacity-75">{{ dataSelected?.country }}</div>
            </div>
            <div class="col-12 col-md-4 mb-3">
              <h6 class="mb-0">Crated time</h6>
              <div class="mb-3 opacity-75 small">{{ StringToPrettyDate(dataSelected?.created_time) }}</div>
            </div>
            <div class="col-12 col-md-4 mb-3">
              <h6 class="mb-0">Modified time</h6>
              <div class="mb-3 opacity-75 small">{{ StringToPrettyDate(dataSelected?.modified_time) }}</div>
            </div>
            <div class="col-12 col-md-4 mb-3">
              <h6 class="mb-0">Last login</h6>
              <div class="mb-3 opacity-75 small">{{ StringToPrettyDate(dataSelected?.last_login_time) }}</div>
            </div>

          </div>
          <div class="col-12 col-md-8">
            <hr>
            <VueTextSection title-size="h4">
              <template #title>Change users roles</template>
              <VueForm @submit="changeRoles(dataSelected.id)" :action-btn-fullwidth="false" action-btn="Send"
                name="roles">
                <VueInput label="Organizer" type="checkbox" v-model="isOrganizer">
                </VueInput>
                <VueInput label="Sub Admin" type="checkbox" v-model="isSubAdmin">
                </VueInput>
                <VueInput label="Admin" type="checkbox" v-model="isAdmin">
                </VueInput>
              </VueForm>
            </VueTextSection>
            <hr>
            <VueTextSection v-if="useAuthStore().adminOnly" title-size="h4">
              <template #title>Disable/Enable user</template>
              <div class="mb opacity-75">
                Disabled users cannot access any source. It is a security precaution in case of leaking user
                information.
              </div>
              <VueForm action-btn="Apply" name="enableDisableUser" :action-btn-fullwidth="false"
                @submit-event="setEnableDisableUser(dataSelected.id)">
                <VueInput v-model="enableDisableUser" type="select" :options="['Disable user', 'Enable user']">
                </VueInput>
              </VueForm>
            </VueTextSection>
            <hr>
            <VueTextSection v-if="useAuthStore().adminOnly" title-size="h4">
              <template #title>Request new password reset token</template>
              <div class="mb opacity-75">
                Create a new token for resetting password. The token will be sent by e-mail to user. Then user can
                define
                new password.
              </div>
              <button type="button" class="btn btn-warning  mt-3" @click="resetPasswordToken(dataSelected.email)">
                <i class="be bi-trash2-fill" />
                Request new reset token
              </button>
            </VueTextSection>
            <hr>
            <VueTextSection v-if="useAuthStore().adminOnly" title-size="h4">
              <VueTextSection :highlight="true">
                <template #title>Delete user</template>
                <div class="mb opacity-75">
                  Please enter your current password if you want to delete this user.
                </div>
                <template #text>This action can not be undone!</template>
                <VueInput label="Current password" type="password" v-model="current_password"></VueInput>
                <button type="button" :disabled="!current_password" class="btn btn-danger mt-3"
                  @click="deleteUser(dataSelected.id)">
                  <i class="be bi-fire" />
                  Delete user
                </button>
              </VueTextSection>
              <AlertModal></AlertModal>
            </VueTextSection>
            <hr>
            <div class="alert alert-info" role="alert">
              For more admin operations for users please visit:<br> <a :href="docsURL" target="_blank">{{ docsURL
              }}</a>
            </div>
          </div>
        </div>
      </VueTextSection>
    </div>
    <div v-else>
      <div class="input-group pb-4">
        <VueInput v-model="searchString" class="form-control" type="text" icon="search"
          :placeholder="'Filter parameters: ID, First name, Last name, Email, Roles'"></VueInput>
        <span class="input-group-text">Total record: {{ totalItems }} </span>
        <button class="btn btn-outline-dark dropdown-toggle " type="button" data-bs-toggle="dropdown"
          aria-expanded="false">Items per page:</button>

        <ul class="dropdown-menu">
          <li v-for="option in itemsPerPageOptions" :key="option">
            <a class="dropdown-item" :class="{ 'active': option === this.itemsPerPage }" @click="changeItemsPerPage(option)"
              href="#">{{ option }}</a>
          </li>
        </ul>
      </div>
      <div>
        <hr>
        <ul class="pagination justify-content-center">
          <li class="page-item" :class="{ 'disabled': currentPage === 1 }">
            <a class="page-link" @click="changePage(currentPage - 1)" aria-label="Previous" href="#">
              <span aria-hidden="true">&laquo;</span>
            </a>
          </li>
          <li class="page-item" v-for="page in Math.ceil(totalItems / itemsPerPage)" :key="page">
            <a class="page-link" @click="changePage(page)" href="#">{{ page }}</a>
          </li>
          <li class="page-item" :class="{ 'disabled': currentPage === Math.ceil(totalItems / itemsPerPage) }">
            <a class="page-link" @click="changePage(currentPage + 1)" aria-label="Next" href="#">
              <span aria-hidden="true">&raquo;</span>
            </a>
          </li>
        </ul>
      </div>


      <div class="table-responsive">
        <table class="table table-striped table-hover">
          <thead>
            <tr>
              <th v-for="(item, idx) in tableHeader" :key="idx">
                {{ item }}
              </th>
            </tr>
          </thead>
          <tbody v-if="!LoadingCircleState">
            <tr v-for="(item, idx) in list" class="lh-base" :key="idx" style="cursor: pointer"
              @click="selectData(item, idx)">
              <th scope="row">{{ item.id }}</th>
              <td>{{ item.first_name }} {{ item.last_name }}</td>
              <td>{{ item.email }}</td>
              <td>
                <span v-for="role in item.roles" :key="role" class="badge text-bg-primary mx-2">{{ role }}</span>
              </td>
            </tr>
          </tbody>
        </table>
        <LoadingCircle :activated="LoadingCircleState"></LoadingCircle>
        <div v-if="list.length === 0" class="text-center">
          <p class="lead">No data found</p>
        </div>
      </div>
      <div>
        <hr>
        <ul class="pagination justify-content-center">
          <li class="page-item" :class="{ 'disabled': currentPage === 1 }">
            <a class="page-link" @click="changePage(currentPage - 1)" aria-label="Previous" href="#">
              <span aria-hidden="true">&laquo;</span>
            </a>
          </li>
          <li class="page-item" v-for="page in Math.ceil(totalItems / itemsPerPage)" :key="page">
            <a class="page-link" @click="changePage(page)" href="#">{{ page }}</a>
          </li>
          <li class="page-item" :class="{ 'disabled': currentPage === Math.ceil(totalItems / itemsPerPage) }">
            <a class="page-link" @click="changePage(currentPage + 1)" aria-label="Next" href="#">
              <span aria-hidden="true">&raquo;</span>
            </a>
          </li>
        </ul>
      </div>
    </div>
    <confirm-dialogue ref="confirmDialogue"></confirm-dialogue>
  </div>
</template>

<script>
import VueTextSection from '@/components/VueTextSection.vue'
import CollapseSection from '@/components/CollapseSection.vue'
import VueInput from '@/components/essentials/VueInput.vue'
import VueForm from '@/components/essentials/VueForm.vue'
import AlertModal from '@/components/AlertModal.vue'
import ConfirmDialogue from '@/components/ConfirmDialogue.vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'
import { apiDelete, apiGet, apiPost, apiPut } from '@/api/api'
import LoadingCircle from '@/components/LoadingCircle.vue'
import { useToastAlertStore } from '@/stores/toastAlert'
import StringToPrettyDate from '../../helper/format'
export default {
  name: 'UsersPage',
  components: {
    LoadingCircle,
    ConfirmDialogue,
    AlertModal,
    VueInput,
    CollapseSection,
    VueTextSection,
    VueForm,
  },
  mounted() {
    if (this.$route.params.id && !this.dataSelected) {
      this.$router.push({ name: 'Users' })
    }
  },
  data() {
    return {
      isOrganizer: false,
      isSubAdmin: false,
      isAdmin: false,
      LoadingCircleState: true,
      data: {},
      current_password: '',
      searchString: '',
      tableHeader: ['ID', 'Name', 'Email', 'Roles'],
      usersList: [],
      currentPage: 1,
      itemsPerPage: 100,
      itemsPerPageOptions: [20, 50, 100, 200],
      totalItems: 0,
      enableDisableUser: '',
    }
  },
  async created() {
    await this.getAndSetUserAll()
  },
  methods: {
    useAuthStore,
    StringToPrettyDate,
    async getAndSetUserAll() {
      const offset = (this.currentPage - 1) * this.itemsPerPage;
      const apiEndpoint = `/admin/user/all/?limit=${this.itemsPerPage}&offset=${offset}`;
      await apiPost(apiEndpoint).then((resp) => {
        this.usersList = resp["content"]
        this.totalItems = resp["total_records"];
        this.LoadingCircleState = false
      })
    },
    selectData(item, idx) {
      this.data = {
        data: item,
        index: idx,
      }
      this.setUserRolesCheckbox()
      this.$router.push(`users/${idx}`)
    },
    unselectData() {
      this.data = {}
      this.searchString = ''
    },
    async changeRoles(userId) {
      this.dataSelected.roles = this.setNewUserRoles
      await apiPut(`admin/user/update/${userId}`, { roles: this.dataSelected.roles })
        .then(() => {
          useToastAlertStore().showAlert('The roles were changed', 'success')
        })
        .catch((e) => {
          useToastAlertStore().showAlert(e, 'danger', 6000)
        })
    },
    async setEnableDisableUser(userId) {
      let user_disabled
      if (this.enableDisableUser === 'Disable user') {
        user_disabled = true
        this.data.data.disabled = true
      } else {
        user_disabled = false
        this.data.data.disabled = false
      }
      let data = {
        disabled: user_disabled
      }
      await apiPut(`admin/user/update/${userId}`, data)
        .then(() => {
          useToastAlertStore().showAlert('User updated', 'success')

        })
        .catch((e) => {
          useToastAlertStore().showAlert(e, 'danger', 6000)
        })
    },
    async resetPasswordToken(userEmail) {
      await apiPost(`user/reset_password_request?email=${encodeURIComponent(userEmail)}`)
        .then(() => {
          useToastAlertStore().showAlert('A new password reset token was sent to user', 'success')
        })
        .catch((e) => {
          useToastAlertStore().showAlert(e, 'danger', 6000)
        })
    },
    async deleteUser(userId) {
      const ok = await this.$refs.confirmDialogue.show({
        title: 'Delete user',
        message: 'Are you sure you want to delete this user? It cannot be undone.',
        okButton: 'Delete forever',
        okButtonTheme: 'btn-danger',
      })
      if (ok) {
        await apiDelete(`admin/user/delete/${userId}?active_user_password=${this.current_password}`)
          .then(() => {
            useToastAlertStore().showAlert('The user was permanently deleted', 'success')
            setTimeout(1000);
            location.reload();
          })
          .catch((e) => {
            useToastAlertStore().showAlert(e, 'danger', 6000)
          })
      } else {
      }
    },
    getUsers() {
      const request = apiGet('admin/user/all')
      this.usersList = request ? request : []
    },
    setUserRolesCheckbox() {
      this.isAdmin = false
      this.isOrganizer = false
      this.isSubAdmin = false

      this.dataSelected.roles.forEach((x) => {
        if (x === 'Admin') {
          this.isAdmin = true
        } else if (x === 'Organizer') {
          this.isOrganizer = true
        } else if (x === 'SubAdmin') {
          this.isSubAdmin = true
        }
      })
    },
    changePage(page) {
      if (page >= 1 && page <= Math.ceil(this.totalItems / this.itemsPerPage)) {
        this.currentPage = page;
      }
    },
    changeItemsPerPage(option) {
      this.itemsPerPage = option
      this.currentPage = 1; // Reset to the first page when items per page changes
      this.getAndSetUserAll();
    },
  },
  computed: {
    docsURL() {
      return new URL('/api/docs', api.defaults.baseURL).href
    },
    dataSelected() {
      return this.data.data
    },
    list() {
      const filteredList = this.searchString === ''
        ? this.usersList
        : this.usersList.filter((item) =>
          item.id.toString() === this.searchString ||
          item.first_name.toLowerCase().includes(this.searchString.toLowerCase().trim()) ||
          item.last_name.toLowerCase().includes(this.searchString.toLowerCase().trim()) ||
          item.email.toLowerCase().includes(this.searchString.toLowerCase().trim()) ||
          (Array.isArray(item.roles) && item.roles.toString().toLowerCase().includes(this.searchString.toLowerCase().trim()))
        );

      return filteredList;



      // return this.searchString === ''
      //   ? this.usersList
      //   : this.usersList.filter(
      //     (item) =>
      //       item.first_name.toLowerCase().includes(this.searchString.toLowerCase()) ||
      //       item.last_name.toLowerCase().includes(this.searchString.toLowerCase()) ||
      //       item.email.toLowerCase().includes(this.searchString.toLowerCase()) ||
      //       item.roles.toString().toLowerCase().includes(this.searchString.toLowerCase())
      //   )
    },
    setNewUserRoles() {
      let newRoles = []
      if (this.isAdmin) {
        newRoles.push('Admin')
      }
      if (this.isOrganizer) {
        newRoles.push('Organizer')
      }
      if (this.isSubAdmin) {
        newRoles.push('SubAdmin')
      }
      return newRoles
    },
  },
  watch: {
    $route(val) {
      if (val.fullPath === '/users') {
        this.data = {}
        this.searchString = ''
      }
    },
    currentPage: 'getAndSetUserAll',
  },
}
</script>
<style scoped></style>
