<template>
  <div>
    <div
      class="d-flex justify-content-between"
      :class="[dataSelected ? 'flex-column' : '']">
      <div class="pb-3">
        <collapse-section name="info">
          <VueTextSection>
            <template #text>
              <p>
                In this view, you can see all users (including yourself). For more details, press
                the show details button below.<br />
                As an administrator you can change the roles of users. Following roles exist in the
                system:
              </p>
              <ul>
                <li>
                  <span class="text-info fw-bold">Administrator:</span> This is your role. You see
                  all challenges and all users. You can allocate roles to each user, delete users
                  and restore deleted challenges. Besides, it is your duty to assign challenges to
                  reviewers.
                </li>
                <li>
                  <span class="text-info fw-bold">Sub-Administrator:</span> The sub-administrator is
                  reserved for the MICCAI board members. They have many rights, but they can not
                  delete users or challenges due to privacy constraints.
                </li>
                <li>
                  <span class="text-info fw-bold">Organizer:</span> The organizer can create
                  challenge proposals.
                </li>
              </ul>
              <p>
                In some cases a user might want to be deleted. You can do this by pressing the
                delete user button. It will remove the user, his challenges and related data from
                the database.<br />
                In case that the email service is not available, users might forget their passwords.
                Only if the user asks you to reset the password, you are allowed to use the button
                below!
              </p>
            </template>
          </VueTextSection>
        </collapse-section>
      </div>
      <p v-if="dataSelected">
        <router-link
          type="button"
          class="btn btn-secondary"
          @click="unselectData"
          :to="{ name: 'Users' }">
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
              <div
                class="mb-3 opacity-75"
                style="text-transform: capitalize">
                {{ dataSelected?.disabled }}
              </div>
            </div>

            <div class="col-12 col-md-4 mb-3">
              <h6 class="mb-0">Roles</h6>
              <div class="mb-3 opacity-75">
                <span
                  v-for="role in dataSelected?.roles"
                  :key="role"
                  class="badge me-1"
                  :class="getRoleBadgeClass(role)"
                  >{{ role }}</span
                >
              </div>
            </div>
            <div class="col-12 col-md-4 mb-3">
              <h6 class="mb-0">Full name</h6>
              <div class="mb-3 opacity-75">
                {{ dataSelected?.first_name }} {{ dataSelected?.last_name }}
              </div>
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
              <div class="mb-3 opacity-75 small">
                {{ StringToPrettyDate(dataSelected?.created_time) }}
              </div>
            </div>
            <div class="col-12 col-md-4 mb-3">
              <h6 class="mb-0">Modified time</h6>
              <div class="mb-3 opacity-75 small">
                {{ StringToPrettyDate(dataSelected?.modified_time) }}
              </div>
            </div>
            <div class="col-12 col-md-4 mb-3">
              <h6 class="mb-0">Last login</h6>
              <div class="mb-3 opacity-75 small">
                {{ StringToPrettyDate(dataSelected?.last_login_time) }}
              </div>
            </div>
          </div>
          <div class="col-12 col-md-8">
            <hr />
            <VueTextSection title-size="h4">
              <template #title>Change users roles</template>
              <VueForm
                @submit="changeRoles(dataSelected.id)"
                :action-btn-fullwidth="false"
                action-btn="Send"
                name="roles">
                <VueInput
                  label="Organizer"
                  type="checkbox"
                  v-model="isOrganizer">
                </VueInput>
                <VueInput
                  label="Sub Admin"
                  type="checkbox"
                  v-model="isSubAdmin">
                </VueInput>
                <VueInput
                  label="Admin"
                  type="checkbox"
                  v-model="isAdmin">
                </VueInput>
              </VueForm>
            </VueTextSection>
            <hr />
            <VueTextSection
              v-if="useAuthStore().adminOnly"
              title-size="h4">
              <template #title>Disable/Enable user</template>
              <div class="mb opacity-75">
                Disabled users cannot access any source. It is a security precaution in case of
                leaking user information.
              </div>
              <VueForm
                action-btn="Apply"
                name="enableDisableUser"
                :action-btn-fullwidth="false"
                @submit-event="setEnableDisableUser(dataSelected.id)">
                <VueInput
                  v-model="enableDisableUser"
                  type="select"
                  :options="['Disable user', 'Enable user']">
                </VueInput>
              </VueForm>
            </VueTextSection>
            <hr />
            <VueTextSection
              v-if="useAuthStore().adminOnly"
              title-size="h4">
              <template #title>Request new password reset token</template>
              <div class="mb opacity-75">
                Create a new token for resetting password. The token will be sent by e-mail to user.
                Then user can define new password.
              </div>
              <button
                type="button"
                class="btn btn-warning mt-3"
                @click="resetPasswordToken(dataSelected.email)">
                <i class="be bi-trash2-fill" />
                Request new reset token
              </button>
            </VueTextSection>
            <hr />
            <VueTextSection
              v-if="useAuthStore().adminOnly"
              title-size="h4">
              <VueTextSection :highlight="true">
                <template #title>Delete user</template>
                <div class="mb opacity-75">
                  Please enter your current password if you want to delete this user.
                </div>
                <template #text>This action can not be undone!</template>
                <VueInput
                  label="Current password"
                  type="password"
                  v-model="current_password"></VueInput>
                <button
                  type="button"
                  :disabled="!current_password"
                  class="btn btn-danger mt-3"
                  @click="deleteUser(dataSelected.id)">
                  <i class="be bi-fire" />
                  Delete user
                </button>
              </VueTextSection>
              <AlertModal></AlertModal>
            </VueTextSection>
            <hr />
            <div
              class="alert alert-info"
              role="alert">
              For more admin operations for users please visit:<br />
              <a
                :href="docsURL"
                target="_blank"
                >{{ docsURL }}</a
              >
            </div>
          </div>
        </div>
      </VueTextSection>
    </div>
    <div v-else>
      <div class="admin-list-shell">
        <div class="card mb-3">
          <div
            class="card-header bg-light cursor-pointer"
            @click="showSearchPanel = !showSearchPanel">
            <div class="d-flex justify-content-between align-items-center">
              <h6 class="mb-0">
                <i class="bi bi-funnel me-2"></i>Advanced Search
                <span
                  v-if="hasActiveFilters"
                  class="badge bg-primary ms-2"
                  >Active</span
                >
              </h6>
              <i :class="showSearchPanel ? 'bi bi-chevron-up' : 'bi bi-chevron-down'"></i>
            </div>
          </div>

          <div
            v-show="showSearchPanel"
            class="card-body">
            <div class="d-flex gap-2 mb-2 p-2 text-bg-light border border-secondary-subtle rounded">
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">ID</label>
                <input
                  v-model="searchFilters.id"
                  type="number"
                  class="form-control form-control-sm"
                  placeholder="ID" />
              </div>
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">Email</label>
                <input
                  v-model="searchFilters.email"
                  type="text"
                  class="form-control form-control-sm"
                  placeholder="Email contains..." />
              </div>
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">First Name</label>
                <input
                  v-model="searchFilters.first_name"
                  type="text"
                  class="form-control form-control-sm"
                  placeholder="Name contains..." />
              </div>
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">Last Name</label>
                <input
                  v-model="searchFilters.last_name"
                  type="text"
                  class="form-control form-control-sm"
                  placeholder="Name contains..." />
              </div>
            </div>

            <div class="d-flex gap-2 mb-2">
              <div class="w-100 p-2 text-bg-light border border-secondary-subtle rounded">
                <label class="form-label small fw-bold text-nowrap">Role</label>
                <select
                  v-model="searchFilters.role"
                  class="form-select form-select-sm">
                  <option value="">All</option>
                  <option value="Admin">Admin</option>
                  <option value="SubAdmin">SubAdmin</option>
                  <option value="Organizer">Organizer</option>
                </select>
              </div>
              <div class="w-100 p-2 text-bg-light border border-secondary-subtle rounded">
                <label class="form-label small fw-bold text-nowrap">Disabled?</label>
                <select
                  v-model="searchFilters.disabled"
                  class="form-select form-select-sm">
                  <option value="">All</option>
                  <option value="true">Yes (Disabled)</option>
                  <option value="false">No (Enabled)</option>
                </select>
              </div>
              <div class="w-100 border-0"></div>
            </div>

            <div class="d-flex gap-2 mb-2 p-2 text-bg-light border border-secondary-subtle rounded">
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">Created Time</label>
                <select
                  v-model="searchFilters.created_time_operator"
                  class="form-select form-select-sm">
                  <option value="">No filter</option>
                  <option value="lt">Before</option>
                  <option value="gt">After</option>
                  <option value="between">Between</option>
                </select>
              </div>
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">Date</label>
                <input
                  v-model="searchFilters.created_time_date1"
                  type="date"
                  class="form-control form-control-sm"
                  :disabled="!searchFilters.created_time_operator" />
              </div>
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">To Date</label>
                <input
                  v-model="searchFilters.created_time_date2"
                  type="date"
                  class="form-control form-control-sm"
                  :disabled="searchFilters.created_time_operator !== 'between'" />
              </div>
            </div>

            <div class="mt-3 d-flex gap-2">
              <button
                type="button"
                class="btn btn-primary btn-sm"
                @click="applySearch">
                <i class="bi bi-search me-2"></i>Apply Search
              </button>
              <button
                type="button"
                class="btn btn-secondary btn-sm"
                @click="clearSearch">
                <i class="bi bi-x-circle me-2"></i>Clear Filters
              </button>
            </div>
          </div>
        </div>
        <div class="input-group pb-4">
          <VueInput
            v-model="searchString"
            :disabled="LoadingCircleState"
            class="form-control"
            type="text"
            icon="search"
            info-text="This filter only checks rows on the current page. Use Advanced Search to search all records."
            :placeholder="'Filter current page by ID, first name, last name, email, roles'"></VueInput>
          <span class="input-group-text">Total record: {{ totalItems }} </span>

          <button
            class="btn btn-outline-primary border-secondary-subtle"
            type="button"
            data-bs-toggle="dropdown"
            aria-expanded="false">
            Items per page: {{ itemsPerPage }} <i class="bi bi-caret-down-fill"></i>
          </button>

          <ul class="dropdown-menu">
            <li
              v-for="option in itemsPerPageOptions"
              :key="option">
              <a
                class="dropdown-item"
                :class="{ active: Number(itemsPerPage) === Number(option) }"
                href="#"
                @click.prevent="changeItemsPerPage(option)">
                {{ option }}
              </a>
            </li>
          </ul>

          <button
            class="btn btn-outline-primary border-secondary-subtle"
            type="button"
            data-bs-toggle="dropdown"
            aria-expanded="false"
            :disabled="selectedRows.length === 0">
            Bulk operations <i class="bi bi-caret-down-fill"></i>
          </button>

          <ul class="dropdown-menu">
            <li>
              <a
                class="dropdown-item"
                @click="openBulkRolesModal"
                :class="{ disabled: selectedRows.length === 0 }"
                href="#"
                ><i class="bi bi-person-gear me-2"></i>Change Roles Selected ({{
                  selectedRows.length
                }})</a
              >
            </li>
            <li>
              <a
                class="dropdown-item"
                @click="openBulkEnableDisableModal"
                :class="{ disabled: selectedRows.length === 0 }"
                href="#"
                ><i class="bi bi-toggle-on me-2"></i>Disable/Enable Selected ({{
                  selectedRows.length
                }})</a
              >
            </li>
            <li>
              <a
                class="dropdown-item"
                @click="bulkResetPasswordToken"
                :class="{ disabled: selectedRows.length === 0 }"
                href="#"
                ><i class="bi bi-key me-2"></i>Request Password Reset ({{ selectedRows.length }})</a
              >
            </li>
            <li>
              <hr class="dropdown-divider" />
            </li>
            <li>
              <a
                class="dropdown-item bg-danger text-white"
                @click="openBulkDeleteModal"
                :class="{ disabled: selectedRows.length === 0 }"
                href="#"
                ><i class="bi bi-trash2-fill me-2"></i>Delete Selected ({{
                  selectedRows.length
                }})</a
              >
            </li>
          </ul>
        </div>
        <div>
          <hr />
          <ul class="pagination justify-content-center">
            <li
              class="page-item"
              :class="{ disabled: currentPage === 1 }">
              <a
                class="page-link"
                @click="changePage(currentPage - 1)"
                aria-label="Previous"
                href="#">
                <span aria-hidden="true">&laquo;</span>
              </a>
            </li>
            <li
              class="page-item"
              v-for="page in Math.ceil(totalItems / itemsPerPage)"
              :key="page">
              <a
                class="page-link"
                @click="changePage(page)"
                href="#"
                >{{ page }}</a
              >
            </li>
            <li
              class="page-item"
              :class="{
                disabled: currentPage === Math.ceil(totalItems / itemsPerPage) || totalItems === 0,
              }">
              <a
                class="page-link"
                @click="changePage(currentPage + 1)"
                aria-label="Next"
                href="#">
                <span aria-hidden="true">&raquo;</span>
              </a>
            </li>
          </ul>
        </div>

        <div class="table-responsive">
          <table class="table table-striped table-hover w-auto admin-list-table">
            <thead>
              <tr class="table-primary">
                <th>
                  <input
                    type="checkbox"
                    v-model="selectAll"
                    @change="selectAllRows" />
                </th>
                <th
                  v-for="(item, idx) in tableHeader"
                  :key="idx"
                  @click="sortTable(item)">
                  <a
                    href="#"
                    class="link-underline-primary link-offset-2 link-underline-opacity-50"
                    >{{ item }}
                    <span v-if="sortColumn === item">
                      <i
                        :class="
                          sortDirection === 'asc' ? 'bi bi-caret-up-fill' : 'bi bi-caret-down-fill'
                        "></i>
                    </span>
                  </a>
                </th>
              </tr>
            </thead>
            <tbody v-if="!LoadingCircleState">
              <tr
                v-for="(item, idx) in list"
                class="lh-base"
                :key="idx"
                style="cursor: pointer"
                @click="selectData(item, idx)">
                <td @click.stop>
                  <input
                    type="checkbox"
                    v-model="selectedRows"
                    :value="item.id" />
                </td>
                <th
                  scope="row"
                  class="table-col-id">
                  {{ item.id }}
                </th>
                <td class="table-col-name">
                  <div class="cell-truncate">{{ item.first_name }} {{ item.last_name }}</div>
                </td>
                <td class="table-col-email">
                  <div class="cell-truncate">{{ item.email }}</div>
                </td>
                <td class="table-col-roles">
                  <div class="roles-wrap">
                    <span
                      v-for="role in item.roles"
                      :key="role"
                      class="badge mx-1"
                      :class="getRoleBadgeClass(role)"
                      >{{ role }}</span
                    >
                    <span
                      v-if="item.disabled"
                      class="badge text-bg-danger ms-1"
                      >Disabled</span
                    >
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
          <LoadingCircle :activated="LoadingCircleState"></LoadingCircle>
          <div
            v-if="list.length === 0 && !LoadingCircleState"
            class="text-center">
            <p class="lead">No data found</p>
          </div>
        </div>
        <div>
          <hr />
          <ul class="pagination justify-content-center">
            <li
              class="page-item"
              :class="{ disabled: currentPage === 1 }">
              <a
                class="page-link"
                @click="changePage(currentPage - 1)"
                aria-label="Previous"
                href="#">
                <span aria-hidden="true">&laquo;</span>
              </a>
            </li>
            <li
              class="page-item"
              v-for="page in Math.ceil(totalItems / itemsPerPage)"
              :key="page">
              <a
                class="page-link"
                @click="changePage(page)"
                href="#"
                >{{ page }}</a
              >
            </li>
            <li
              class="page-item"
              :class="{
                disabled: currentPage === Math.ceil(totalItems / itemsPerPage) || totalItems === 0,
              }">
              <a
                class="page-link"
                @click="changePage(currentPage + 1)"
                aria-label="Next"
                href="#">
                <span aria-hidden="true">&raquo;</span>
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <confirm-dialogue ref="confirmDialogue"></confirm-dialogue>

    <!-- Bulk Operations Modals -->
    <!-- Bulk Change Roles Modal -->
    <div
      class="modal fade"
      :class="{ show: showBulkRolesPanel, 'd-block': showBulkRolesPanel }"
      tabindex="-1"
      @click.self="showBulkRolesPanel = false">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-warning text-white">
            <h5 class="modal-title"><i class="bi bi-person-gear me-2"></i>Bulk Change Roles</h5>
            <button
              type="button"
              class="btn-close btn-close-white"
              @click="showBulkRolesPanel = false"></button>
          </div>
          <div class="modal-body">
            <p class="mb-3">
              <strong>{{ selectedRows.length }}</strong> user(s) selected
            </p>
            <div class="mb-3">
              <label class="form-label fw-bold">Select Roles to Apply</label>
              <div class="form-check">
                <input
                  class="form-check-input"
                  type="checkbox"
                  v-model="bulkRoles.isOrganizer"
                  id="bulkOrganizer" />
                <label
                  class="form-check-label"
                  for="bulkOrganizer"
                  >Organizer</label
                >
              </div>
              <div class="form-check">
                <input
                  class="form-check-input"
                  type="checkbox"
                  v-model="bulkRoles.isSubAdmin"
                  id="bulkSubAdmin" />
                <label
                  class="form-check-label"
                  for="bulkSubAdmin"
                  >Sub Admin</label
                >
              </div>
              <div class="form-check">
                <input
                  class="form-check-input"
                  type="checkbox"
                  v-model="bulkRoles.isAdmin"
                  id="bulkAdmin" />
                <label
                  class="form-check-label"
                  for="bulkAdmin"
                  >Admin</label
                >
              </div>
            </div>
            <div class="alert alert-info small">
              Note: These roles will replace the current roles of all selected users.
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              @click="showBulkRolesPanel = false">
              Cancel
            </button>
            <button
              type="button"
              class="btn btn-warning"
              @click="bulkChangeRoles">
              <i class="bi bi-check-circle me-2"></i>Apply Roles
            </button>
          </div>
        </div>
      </div>
    </div>
    <div
      v-if="showBulkRolesPanel"
      class="modal-backdrop fade show"></div>

    <!-- Bulk Disable/Enable Modal -->
    <div
      class="modal fade"
      :class="{ show: showBulkEnableDisablePanel, 'd-block': showBulkEnableDisablePanel }"
      tabindex="-1"
      @click.self="showBulkEnableDisablePanel = false">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-info text-white">
            <h5 class="modal-title"><i class="bi bi-toggle-on me-2"></i>Bulk Disable/Enable</h5>
            <button
              type="button"
              class="btn-close btn-close-white"
              @click="showBulkEnableDisablePanel = false"></button>
          </div>
          <div class="modal-body">
            <p class="mb-3">
              <strong>{{ selectedRows.length }}</strong> user(s) selected
            </p>
            <div class="mb-3">
              <label class="form-label fw-bold">Select Action</label>
              <select
                v-model="bulkEnableDisableSelection"
                class="form-select">
                <option value="">-- Select Action --</option>
                <option value="disable">Disable User(s)</option>
                <option value="enable">Enable User(s)</option>
              </select>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              @click="showBulkEnableDisablePanel = false">
              Cancel
            </button>
            <button
              type="button"
              class="btn btn-info"
              :disabled="!bulkEnableDisableSelection"
              @click="bulkEnableDisable">
              <i class="bi bi-check-circle me-2"></i>Apply
            </button>
          </div>
        </div>
      </div>
    </div>
    <div
      v-if="showBulkEnableDisablePanel"
      class="modal-backdrop fade show"></div>

    <!-- Bulk Delete Modal -->
    <div
      class="modal fade"
      :class="{ show: showBulkDeletePanel, 'd-block': showBulkDeletePanel }"
      tabindex="-1"
      @click.self="showBulkDeletePanel = false">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-danger text-white">
            <h5 class="modal-title"><i class="bi bi-trash2-fill me-2"></i>Delete Multiple Users</h5>
            <button
              type="button"
              class="btn-close btn-close-white"
              @click="showBulkDeletePanel = false"></button>
          </div>
          <div class="modal-body">
            <p class="mb-3">
              <strong>{{ selectedRows.length }}</strong> user(s) selected
            </p>
            <div class="alert alert-danger mb-3">
              <strong>⚠️ Warning:</strong> This will permanently delete the selected users. This
              action CANNOT be undone!
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold">Enter Your Password to Confirm</label>
              <input
                v-model="bulkCurrentPassword"
                type="password"
                class="form-control"
                placeholder="Enter your current password"
                @keyup.enter="bulkDeleteUsers" />
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              @click="showBulkDeletePanel = false">
              Cancel
            </button>
            <button
              type="button"
              class="btn btn-danger"
              :disabled="!bulkCurrentPassword"
              @click="bulkDeleteUsers">
              <i class="bi bi-exclamation-triangle me-2"></i>Delete Forever
            </button>
          </div>
        </div>
      </div>
    </div>
    <div
      v-if="showBulkDeletePanel"
      class="modal-backdrop fade show"></div>
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
      showSearchPanel: false,
      searchFilters: {
        id: '',
        email: '',
        first_name: '',
        last_name: '',
        role: '',
        disabled: '',
        created_time_operator: '',
        created_time_date1: '',
        created_time_date2: '',
      },
      activeSearchFilters: null,
      sortColumn: 'ID',
      sortDirection: 'asc',
      selectedRows: [],
      selectAll: false,
      tableHeaderColumnNames: ['id', 'first_name', 'email', 'roles'], // Map headers to keys

      // Bulk Modals state
      showBulkRolesPanel: false,
      showBulkEnableDisablePanel: false,
      showBulkDeletePanel: false,
      bulkRoles: {
        isOrganizer: false,
        isSubAdmin: false,
        isAdmin: false,
      },
      bulkEnableDisableSelection: '',
      bulkCurrentPassword: '',
    }
  },
  async created() {
    await this.getAndSetUserAll()
  },
  methods: {
    useAuthStore,
    StringToPrettyDate,
    async getAndSetUserAll() {
      const offset = (this.currentPage - 1) * this.itemsPerPage
      const apiEndpoint = `/admin/user/all?limit=${this.itemsPerPage}&offset=${offset}`

      let payload = {
        search_filters: this.activeSearchFilters || {}, // Pass active filters
      }

      // Add sorting params to URL or payload?
      // admin_user.py route accepts sort_by and sort_desc query params
      // Let's append them to URL
      const sortParams = `&sort_by=${
        this.tableHeaderColumnNames[this.tableHeader.indexOf(this.sortColumn)] || 'id'
      }&sort_desc=${this.sortDirection === 'desc'}`

      await apiPost(apiEndpoint + sortParams, payload)
        .then((resp) => {
          this.usersList = resp['content']
          this.totalItems = resp['total_records']
          this.LoadingCircleState = false
        })
        .catch((e) => {
          this.LoadingCircleState = false
          if (e.message.includes('No User found') || e.message.includes('not found')) {
            this.usersList = []
            this.totalItems = 0
            useToastAlertStore().showAlert('No users found matching criteria', 'info', 3000)
          } else {
            useToastAlertStore().showAlert(e.message, 'danger', 6000)
          }
        })
    },
    selectData(item, idx) {
      this.data = {
        data: item,
        index: idx,
      }
      this.setUserRolesCheckbox()
      this.$router.push({ name: 'User Overview', params: { id: item.id } })
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
        disabled: user_disabled,
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
            setTimeout(1000)
            location.reload()
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
        this.currentPage = page
      }
    },
    changeItemsPerPage(option) {
      this.itemsPerPage = option
      this.currentPage = 1 // Reset to the first page when items per page changes
      this.getAndSetUserAll()
    },
    buildSearchFilters() {
      const filters = {}
      if (this.searchFilters.id) {
        filters.id = this.searchFilters.id
      }
      if (this.searchFilters.email) {
        filters.email__ilike = `%${this.searchFilters.email}%`
      }
      if (this.searchFilters.first_name) {
        filters.first_name__ilike = `%${this.searchFilters.first_name}%`
      }
      if (this.searchFilters.last_name) {
        filters.last_name__ilike = `%${this.searchFilters.last_name}%`
      }
      if (this.searchFilters.role) {
        // roles is usually a JSON or array column. Assuming checking presence.
        // admin_user.py service might need specific handling but we'll try contains logic or exact if supported
        // If roles is a list string in DB:
        // filters.roles__contains = this.searchFilters.role
        // But let's try strict equality for now or leave it if unclear.
        // Given existing pattern: filters.roles__contains might work if implemented in backend generic filtering
        filters.roles__contains = this.searchFilters.role
      }
      if (this.searchFilters.disabled !== '') {
        filters.disabled = this.searchFilters.disabled === 'true'
      }
      // Created Time
      if (this.searchFilters.created_time_operator && this.searchFilters.created_time_date1) {
        const date1 = new Date(this.searchFilters.created_time_date1).toISOString()
        if (this.searchFilters.created_time_operator === 'lt') {
          filters.created_time__lt = date1
        } else if (this.searchFilters.created_time_operator === 'gt') {
          filters.created_time__gt = date1
        } else if (
          this.searchFilters.created_time_operator === 'between' &&
          this.searchFilters.created_time_date2
        ) {
          const date2 = new Date(this.searchFilters.created_time_date2).toISOString()
          filters.created_time__between = [date1, date2]
        }
      }
      return Object.keys(filters).length > 0 ? filters : null
    },
    applySearch() {
      this.activeSearchFilters = this.buildSearchFilters()
      this.currentPage = 1
      this.getAndSetUserAll()
      if (this.activeSearchFilters) {
        useToastAlertStore().showAlert('Search filters applied', 'success', 3000)
      } else {
        useToastAlertStore().showAlert('No filters to apply', 'info', 3000)
      }
    },
    clearSearch() {
      this.searchFilters = {
        id: '',
        email: '',
        first_name: '',
        last_name: '',
        role: '',
        disabled: '',
        created_time_operator: '',
        created_time_date1: '',
        created_time_date2: '',
      }
      this.activeSearchFilters = null
      this.currentPage = 1
      this.getAndSetUserAll()
      useToastAlertStore().showAlert('Search filters cleared', 'success', 3000)
    },
    sortTable(column) {
      if (this.sortColumn === column) {
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc'
      } else {
        this.sortDirection = 'asc'
      }
      this.sortColumn = column
      this.getAndSetUserAll() // Reload with server-side sorting
    },
    selectAllRows() {
      if (this.selectAll) {
        this.selectedRows = this.usersList.map((item) => item.id)
      } else {
        this.selectedRows = []
      }
    },
    openBulkRolesModal() {
      this.showBulkRolesPanel = true
      this.bulkRoles = { isOrganizer: false, isSubAdmin: false, isAdmin: false }
    },
    openBulkEnableDisableModal() {
      this.showBulkEnableDisablePanel = true
      this.bulkEnableDisableSelection = ''
    },
    openBulkDeleteModal() {
      this.showBulkDeletePanel = true
      this.bulkCurrentPassword = ''
    },
    async bulkChangeRoles() {
      if (this.selectedRows.length === 0) return

      let newRoles = []
      if (this.bulkRoles.isAdmin) newRoles.push('Admin')
      if (this.bulkRoles.isOrganizer) newRoles.push('Organizer')
      if (this.bulkRoles.isSubAdmin) newRoles.push('SubAdmin')

      const updates = this.selectedRows.map((id) => ({
        id: id,
        roles: newRoles,
      }))

      try {
        await apiPut('/admin/user/bulk-update', updates).then((resp) => {
          useToastAlertStore().showAlert(
            `Roles updated for ${this.selectedRows.length} user(s)`,
            'success'
          )
          this.showBulkRolesPanel = false
          this.selectedRows = []
          this.selectAll = false
          this.getAndSetUserAll()
        })
      } catch (e) {
        useToastAlertStore().showAlert(e, 'danger', 6000)
      }
    },
    async bulkEnableDisable() {
      if (this.selectedRows.length === 0 || !this.bulkEnableDisableSelection) return

      const disableUser = this.bulkEnableDisableSelection === 'disable'
      const updates = this.selectedRows.map((id) => ({
        id: id,
        disabled: disableUser,
      }))

      try {
        await apiPut('/admin/user/bulk-update', updates).then(() => {
          useToastAlertStore().showAlert(
            `Users ${disableUser ? 'disabled' : 'enabled'} successfully`,
            'success'
          )
          this.showBulkEnableDisablePanel = false
          this.selectedRows = []
          this.selectAll = false
          this.getAndSetUserAll()
        })
      } catch (e) {
        useToastAlertStore().showAlert(e, 'danger', 6000)
      }
    },
    async bulkResetPasswordToken() {
      if (this.selectedRows.length === 0) return

      const ok = await this.$refs.confirmDialogue.show({
        title: 'Reset Password Tokens',
        message: `Are you sure you want to request password reset for ${this.selectedRows.length} user(s)? Emails will be sent.`,
        okButton: 'Request',
        okButtonTheme: 'btn-warning',
      })
      if (!ok) return

      // Need to find emails for selected IDs
      // usersList might only have current page. If selectedRows contains IDs from current page (which it does), we can find them.
      const selectedUsers = this.usersList.filter((u) => this.selectedRows.includes(u.id))

      let successCount = 0
      for (const user of selectedUsers) {
        try {
          await apiPost(`user/reset_password_request?email=${encodeURIComponent(user.email)}`)
          successCount++
        } catch (e) {
          console.error(`Failed to reset for ${user.email}`, e)
        }
      }
      useToastAlertStore().showAlert(`Reset tokens requested for ${successCount} users`, 'success')
      this.selectedRows = []
      this.selectAll = false
    },
    async bulkDeleteUsers() {
      if (this.selectedRows.length === 0) return
      if (!this.bulkCurrentPassword) {
        useToastAlertStore().showAlert('Password required', 'warning')
        return
      }

      try {
        await api
          .delete(`/admin/user/bulk-delete`, {
            params: { active_user_password: this.bulkCurrentPassword },
            data: this.selectedRows,
          })
          .then(() => {
            useToastAlertStore().showAlert('Users deleted successfully', 'success')
            this.showBulkDeletePanel = false
            this.selectedRows = []
            this.selectAll = false
            this.bulkCurrentPassword = ''
            this.getAndSetUserAll()
          })
      } catch (e) {
        useToastAlertStore().showAlert(e?.response?.data?.detail || e.message, 'danger', 6000)
      }
    },
    getRoleBadgeClass(role) {
      if (role === 'Admin') return 'text-bg-danger'
      if (role === 'SubAdmin') return 'text-bg-warning'
      return 'text-bg-primary'
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
      if (this.activeSearchFilters !== null) {
        return this.usersList
      }
      const filteredList =
        this.searchString === ''
          ? this.usersList
          : this.usersList.filter(
              (item) =>
                item.id.toString() === this.searchString ||
                item.first_name.toLowerCase().includes(this.searchString.toLowerCase().trim()) ||
                item.last_name.toLowerCase().includes(this.searchString.toLowerCase().trim()) ||
                item.email.toLowerCase().includes(this.searchString.toLowerCase().trim()) ||
                (Array.isArray(item.roles) &&
                  item.roles
                    .toString()
                    .toLowerCase()
                    .includes(this.searchString.toLowerCase().trim()))
            )

      return filteredList
    },
    hasActiveFilters() {
      return this.activeSearchFilters !== null
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
      if (val.name === 'Users') {
        this.data = {}
        this.searchString = ''
      }
    },
    currentPage: 'getAndSetUserAll',
  },
}
</script>
<style scoped>
.admin-list-shell {
  width: fit-content;
  max-width: 100%;
}

.admin-list-table {
  table-layout: fixed;
}

.admin-list-table th,
.admin-list-table td {
  vertical-align: middle;
}

.table-col-id {
  width: 80px;
  min-width: 80px;
}

.table-col-name {
  width: 240px;
  min-width: 240px;
}

.table-col-email {
  width: 280px;
  min-width: 280px;
}

.table-col-roles {
  width: 260px;
  min-width: 260px;
}

.cell-truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.roles-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
  max-width: 240px;
}
</style>
