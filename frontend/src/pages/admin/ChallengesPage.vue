<template>
  <div>
    <p v-if="dataSelected">
      <router-link
        type="button"
        class="btn btn-secondary"
        @click="unselectData"
        :to="{ name: 'Challenges' }">
        <i class="be bi-arrow-left pe-1" />
        Go Back
      </router-link>
    </p>
    <div v-if="dataSelected">
      <VueTextSection>
        <div class="row">
          <div class="row col-12 col-md-12 mb-3 p-3">
            <div class="col-12 p-2">
              <h6 class="mb-0">Name</h6>
              <div
                class="overflow-auto"
                style="max-height: 150px">
                {{ dataSelected?.challenge_name }}
              </div>
            </div>

            <!-- <div class="col-12 p-2">
              <h6 class="mb-0">Autor names</h6>
              <div class="mb-3 opacity-75">
                <div class="overflow-auto" style="max-height: 150px;">{{ dataSelected?.challenge_author_names }}</div>
              </div>
            </div>
            <div class="col-12 p-2">
              <h6 class="mb-0">Autor emails</h6>
              <div class="mb-3 opacity-75">
                <div class="overflow-auto" style="max-height: 150px;">{{
                  dataSelected?.challenge_author_emails }}</div>
              </div>
            </div> -->

            <div class="col-12 col-md-3 p-2">
              <h6 class="mb-0">Year</h6>
              <div class="mb-3 opacity-75">{{ dataSelected?.challenge_year }}</div>
            </div>
            <!-- <div class="col-12 col-md-3 p-2">
              <h6 class="mb-0">Acronym</h6>
              <div class="mb-3 opacity-75">{{ dataSelected?.challenge_acronym }}</div>
            </div> -->
            <div class="col-12 col-md-2 p-2">
              <h6 class="mb-0">Owner ID</h6>
              <div class="mb-3 opacity-75">{{ dataSelected?.challenge_owner_id }}</div>
            </div>
            <div class="col-12 col-md-7 p-2">
              <h6 class="mb-0">Status</h6>
              <div class="mb-3 opacity-75">{{ dataSelected?.challenge_status }}</div>
            </div>

            <div class="col-12 col-md-4 p-2">
              <h6 class="mb-0">Created time</h6>
              <div class="mb-3 opacity-75">
                {{ StringToPrettyDate(dataSelected?.challenge_created_time) }}
              </div>
            </div>
            <div class="col-12 col-md-4 p-2">
              <h6 class="mb-0">Last modified time</h6>
              <div class="mb-3 opacity-75">
                {{ StringToPrettyDate(dataSelected?.challenge_modified_time) }}
              </div>
            </div>
            <div class="col-12 col-md-4 p-2">
              <h6 class="mb-0">Submitted time</h6>
              <div class="mb-3 opacity-75">
                {{ StringToPrettyDate(dataSelected?.challenge_submission_time) }}
              </div>
            </div>
          </div>
          <div class="row col-12 col-md-8 mb-3">
            <hr />
            <VueTextSection title-size="h4">
              <template #title>Download proposal</template>
              <button
                type="button"
                class="btn btn-info downloadFile"
                :disabled="!dataSelected.challenge_file"
                @click="downloadChallenge(dataSelected?.id)">
                <i
                  v-if="!LoadingCircleStateDownload"
                  class="be bi-download" />

                <div
                  v-if="LoadingCircleStateDownload"
                  class="d-flex align-items-center justify-content-around">
                  <div
                    class="spinner-border spinner-border-sm me-3"
                    role="status"
                    aria-hidden="true"></div>
                  <span>Downloading...</span>
                </div>
                {{ btnTitle }}
              </button>
              <div
                class="mb-3 opacity-75"
                v-if="!dataSelected.challenge_file">
                No file submitted yet
              </div>
            </VueTextSection>
            <!-- <VueTextSection title-size="h4" v-if="useAuthStore().adminOnly">
              <template #title>Register challenge</template>
              <button type="button" class="btn btn-success">
                <i class="be bi-patch-check-fill" @click="registerChallenge" />
                Register challenge
              </button>
            </VueTextSection> -->
            <hr />
            <VueTextSection
              v-if="useAuthStore().adminOnly"
              title-size="h4">
              <template #title>Change Status</template>
              <VueForm
                action-btn="Change Status"
                name="status"
                :action-btn-fullwidth="false"
                @submit-event="setStatus">
                <VueInput
                  v-model="status"
                  type="select"
                  :options="statusList"></VueInput>
              </VueForm>
            </VueTextSection>
            <hr />
            <VueTextSection
              v-if="useAuthStore().adminOnly"
              title-size="h4">
              <template #title>Allow for further modifications after deadline</template>
              <div class="mb opacity-75">
                The owner can edit proposal even conference is closed for further submissions.
              </div>
              <VueForm
                action-btn="Apply"
                name="allowModification"
                :action-btn-fullwidth="false"
                @submit-event="setAllowModification">
                <VueInput
                  v-model="allowModification"
                  type="select"
                  :options="allowModificationList"></VueInput>
              </VueForm>
            </VueTextSection>
            <!-- <VueTextSection v-if="useAuthStore().adminOnly" title-size="h4">
              <template #title>Assign to other user</template>
              <VueForm action-btn="Change creator" name="creator" :action-btn-fullwidth="false" @submit-event="setCreator"
                :errorMessage="failMessageCreator">
                <VueInput v-model="creator" type="select" :options="creatorListText"></VueInput>
              </VueForm>
            </VueTextSection> -->
            <hr />
            <VueTextSection
              v-if="useAuthStore().adminOnly"
              title-size="h4">
              <VueTextSection :highlight="true">
                <template #title>☢️ Prune challenge</template>
                <div class="mb opacity-75">
                  Please enter your current password if you want to prune this challenge.
                </div>
                <template #text
                  >Delete this challenge with its all tasks, and all histories in database. ☢️ This
                  action can not be undone! ☢️</template
                >
                <VueInput
                  label="Current password"
                  type="password"
                  v-model="current_password"></VueInput>
                <button
                  type="button"
                  :disabled="!current_password"
                  class="mt-3 btn btn-danger"
                  @click="deleteChallenge">
                  <i class="be bi-trash2-fill" />
                  Prune challenge
                </button>
              </VueTextSection>
            </VueTextSection>
            <hr />
            <div
              class="alert alert-info"
              role="alert">
              For more admin operations for challenges please visit:<br />
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
                <label class="form-label small fw-bold text-nowrap">Challenge ID</label>
                <input
                  v-model="searchFilters.id"
                  type="number"
                  class="form-control form-control-sm"
                  placeholder="ID" />
              </div>
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">Challenge Name</label>
                <input
                  v-model="searchFilters.challenge_name"
                  type="text"
                  class="form-control form-control-sm"
                  placeholder="Search..." />
              </div>
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">Owner ID</label>
                <input
                  v-model="searchFilters.challenge_owner_id"
                  type="number"
                  class="form-control form-control-sm"
                  placeholder="Owner ID" />
              </div>
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">Status</label>
                <select
                  v-model="searchFilters.challenge_status"
                  class="form-select form-select-sm">
                  <option value="">All</option>
                  <option
                    v-for="status in statusList"
                    :key="status"
                    :value="status">
                    {{ status }}
                  </option>
                </select>
              </div>
            </div>

            <div class="d-flex gap-2 mb-2 p-2 text-bg-light border border-secondary-subtle rounded">
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">Challenge Year</label>
                <select
                  v-model="searchFilters.year_operator"
                  class="form-select form-select-sm">
                  <option value="">No filter</option>
                  <option value="eq">Equals</option>
                  <option value="lt">Before</option>
                  <option value="gt">After</option>
                  <option value="between">Between</option>
                </select>
              </div>
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">{{
                  searchFilters.year_operator === 'between' ? 'From Year' : 'Year'
                }}</label>
                <input
                  v-model="searchFilters.challenge_year"
                  type="number"
                  class="form-control form-control-sm"
                  :disabled="!searchFilters.year_operator" />
              </div>
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">To Year</label>
                <input
                  v-model="searchFilters.challenge_year2"
                  type="number"
                  class="form-control form-control-sm"
                  :disabled="searchFilters.year_operator !== 'between'" />
              </div>
            </div>

            <div class="d-flex gap-2 mb-2 p-2 text-bg-light border border-secondary-subtle rounded">
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">Submission Time</label>
                <select
                  v-model="searchFilters.submission_time_operator"
                  class="form-select form-select-sm">
                  <option value="">No filter</option>
                  <option value="lt">Before</option>
                  <option value="gt">After</option>
                  <option value="between">Between</option>
                </select>
              </div>
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">{{
                  searchFilters.submission_time_operator === 'between' ? 'From Date' : 'Date'
                }}</label>
                <input
                  v-model="searchFilters.submission_time_date1"
                  type="date"
                  class="form-control form-control-sm"
                  :disabled="!searchFilters.submission_time_operator" />
              </div>
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">To Date</label>
                <input
                  v-model="searchFilters.submission_time_date2"
                  type="date"
                  class="form-control form-control-sm"
                  :disabled="searchFilters.submission_time_operator !== 'between'" />
              </div>
            </div>

            <div class="d-flex gap-2">
              <div class="w-100 p-2 text-bg-light border border-secondary-subtle rounded">
                <label class="form-label small fw-bold text-nowrap">Lighthouse</label>
                <select
                  v-model="searchFilters.challenge_is_lighthouse_challenge"
                  class="form-select form-select-sm">
                  <option value="">All</option>
                  <option value="true">Yes</option>
                  <option value="false">No</option>
                </select>
              </div>
              <div class="w-100 border-0"></div>
              <div class="w-100 border-0"></div>
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
            :placeholder="'Filter current page by ID, name, year, status...'">
          </VueInput>
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
                @click="bulkDownloadChallenges"
                :class="{ disabled: selectedRows.length === 0 }"
                href="#"
                ><i class="bi bi-download me-2"></i>Download Selected ({{ selectedRows.length }})</a
              >
            </li>
            <li>
              <a
                class="dropdown-item"
                @click="bulkChangeStatus"
                :class="{ disabled: selectedRows.length === 0 }"
                href="#"
                ><i class="bi bi-arrow-repeat me-2"></i>Change Status Selected ({{
                  selectedRows.length
                }})</a
              >
            </li>
            <li>
              <a
                class="dropdown-item"
                @click="bulkAllowModifications"
                :class="{ disabled: selectedRows.length === 0 }"
                href="#"
                ><i class="bi bi-unlock me-2"></i>Allow/Disallow Modifications ({{
                  selectedRows.length
                }})</a
              >
            </li>
            <li>
              <hr class="dropdown-divider" />
            </li>
            <li class="">
              <a
                class="dropdown-item bg-danger text-white"
                @click="bulkPruneChallenges"
                :class="{ disabled: selectedRows.length === 0 }"
                href="#"
                ><i class="bi bi-trash2-fill me-2"></i>Prune Selected ({{ selectedRows.length }})</a
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
                    >{{ item
                    }}<span v-if="sortColumn === item">
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
                style="cursor: pointer; max-width: 50px"
                @click="selectData(item, idx)">
                <td @click.stop>
                  <input
                    type="checkbox"
                    v-model="selectedRows"
                    :value="item.id" />
                </td>
                <td class="table-col-id">{{ item?.id }}</td>
                <td class="table-col-owner">{{ item?.challenge_owner_id }}</td>
                <td class="table-col-year">{{ item?.challenge_year }}</td>
                <td class="table-col-conference">
                  <div class="cell-truncate">
                    {{ getConferenceShortName(item?.challenge_conference_id) }}
                  </div>
                </td>
                <td class="table-col-name">
                  <div class="cell-truncate">
                    {{
                      item?.challenge_name !== null
                        ? item?.challenge_name.length > 80
                          ? item?.challenge_name.slice(0, 80) + '...'
                          : item?.challenge_name
                        : null
                    }}
                  </div>
                </td>
                <!-- <td>{{ item?.challenge_progress }}</td> -->
                <td class="table-col-status">
                  <div class="cell-truncate">{{ setStatusPretty(item?.challenge_status) }}</div>
                </td>
                <td class="table-col-modified">
                  <small>{{ StringToPrettyDate(item?.challenge_modified_time) }}</small>
                </td>
                <!-- <td>
                <div class="mx-2">{{ item?.challenge_author_names !== null ? item?.challenge_author_names.length > 100 ?
                  item?.challenge_author_names.slice(0,
                    100) + "..." : item?.challenge_author_names : null }}</div>
              </td> -->
              </tr>
            </tbody>
          </table>
          <LoadingCircle :activated="LoadingCircleState"></LoadingCircle>

          <div
            v-if="list?.length === 0 && !LoadingCircleState"
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

    <!-- Bulk Operations Modals -->
    <!-- Bulk Change Status Modal -->
    <div
      class="modal fade"
      :class="{ show: showBulkStatusPanel, 'd-block': showBulkStatusPanel }"
      tabindex="-1"
      @click.self="showBulkStatusPanel = false">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-warning text-white">
            <h5 class="modal-title"><i class="bi bi-arrow-repeat me-2"></i>Bulk Change Status</h5>
            <button
              type="button"
              class="btn-close btn-close-white"
              @click="showBulkStatusPanel = false"></button>
          </div>
          <div class="modal-body">
            <p class="mb-3">
              <strong>{{ selectedRows.length }}</strong> challenge(s) selected
            </p>
            <div class="mb-3">
              <label class="form-label fw-bold">Select New Status</label>
              <select
                v-model="bulkStatusSelected"
                class="form-select">
                <option value="">-- Select Status --</option>
                <option
                  v-for="status in statusList"
                  :key="status"
                  :value="status">
                  {{ status }}
                </option>
              </select>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              @click="showBulkStatusPanel = false">
              Cancel
            </button>
            <button
              type="button"
              class="btn btn-warning"
              :disabled="!bulkStatusSelected"
              @click="bulkChangeStatus">
              <i class="bi bi-check-circle me-2"></i>Apply Status Change
            </button>
          </div>
        </div>
      </div>
    </div>
    <div
      v-if="showBulkStatusPanel"
      class="modal-backdrop fade show"></div>

    <!-- Bulk Allow/Disallow Modifications Modal -->
    <div
      class="modal fade"
      :class="{ show: showBulkAllowModPanel, 'd-block': showBulkAllowModPanel }"
      tabindex="-1"
      @click.self="showBulkAllowModPanel = false">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-info text-white">
            <h5 class="modal-title"><i class="bi bi-unlock me-2"></i>Bulk Modify Permissions</h5>
            <button
              type="button"
              class="btn-close btn-close-white"
              @click="showBulkAllowModPanel = false"></button>
          </div>
          <div class="modal-body">
            <p class="mb-3">
              <strong>{{ selectedRows.length }}</strong> challenge(s) selected
            </p>
            <div class="mb-3">
              <label class="form-label fw-bold">Select Permission Setting</label>
              <select
                v-model="bulkAllowModificationSelected"
                class="form-select">
                <option value="">-- Select Option --</option>
                <option
                  v-for="option in allowModificationList"
                  :key="option"
                  :value="option">
                  {{ option }}
                </option>
              </select>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              @click="showBulkAllowModPanel = false">
              Cancel
            </button>
            <button
              type="button"
              class="btn btn-info"
              :disabled="!bulkAllowModificationSelected"
              @click="bulkAllowModifications">
              <i class="bi bi-check-circle me-2"></i>Apply Permission
            </button>
          </div>
        </div>
      </div>
    </div>
    <div
      v-if="showBulkAllowModPanel"
      class="modal-backdrop fade show"></div>

    <!-- Bulk Prune Modal -->
    <div
      class="modal fade"
      :class="{ show: showBulkPrunePanel, 'd-block': showBulkPrunePanel }"
      tabindex="-1"
      @click.self="showBulkPrunePanel = false">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-danger text-white">
            <h5 class="modal-title">
              <i class="bi bi-trash2-fill me-2"></i>☢️ Bulk Prune Challenges
            </h5>
            <button
              type="button"
              class="btn-close btn-close-white"
              @click="showBulkPrunePanel = false"></button>
          </div>
          <div class="modal-body">
            <p class="mb-3">
              <strong>{{ selectedRows.length }}</strong> challenge(s) selected
            </p>
            <div class="alert alert-danger mb-3">
              <strong>⚠️ Warning:</strong> This will permanently delete the selected challenges,
              their tasks, and all histories. This action CANNOT be undone!
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold">Enter Your Password to Confirm</label>
              <input
                v-model="bulkCurrentPassword"
                type="password"
                class="form-control"
                placeholder="Enter your current password"
                @keyup.enter="bulkPruneChallenges" />
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              @click="showBulkPrunePanel = false">
              Cancel
            </button>
            <button
              type="button"
              class="btn btn-danger"
              :disabled="!bulkCurrentPassword"
              @click="bulkPruneChallenges">
              <i class="bi bi-exclamation-triangle me-2"></i>Prune Forever
            </button>
          </div>
        </div>
      </div>
    </div>
    <div
      v-if="showBulkPrunePanel"
      class="modal-backdrop fade show"></div>

    <confirm-dialogue ref="confirmDialogue"></confirm-dialogue>
  </div>
</template>

<script>
import VueTextSection from '@/components/VueTextSection.vue'
import VueInput from '@/components/essentials/VueInput.vue'
import VueForm from '@/components/essentials/VueForm.vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'
import { apiDelete, apiGetDownload, apiPut, apiPost } from '@/api/api'
import ConfirmDialogue from '@/components/ConfirmDialogue.vue'
import LoadingCircle from '@/components/LoadingCircle.vue'
import loadingCircle from '@/components/LoadingCircle.vue'
import { useToastAlertStore } from '@/stores/toastAlert'
import StringToPrettyDate from '../../helper/format'

function convertInBlob(base64) {
  base64 = base64.replace('data:application/pdf;base64,', '')
  const contentType = 'application/pdf'
  const sliceSize = 512

  const byteCharacters = atob(base64)
  const byteArrays = []

  for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
    const slice = byteCharacters.slice(offset, offset + sliceSize)

    const byteNumbers = new Array(slice.length)
    for (let i = 0; i < slice.length; i++) {
      byteNumbers[i] = slice.charCodeAt(i)
    }

    const byteArray = new Uint8Array(byteNumbers)
    byteArrays.push(byteArray)
  }

  const blob = new Blob(byteArrays, { type: contentType })
  const blobUrl = URL.createObjectURL(blob)
  return blobUrl
}
function downloadFilePdf(blob, fileName) {
  const link = document.createElement('a')
  link.href = blob
  link.download = fileName
  document.body.append(link)
  link.click()
  link.remove()
  setTimeout(() => URL.revokeObjectURL(link.href), 7000)
}

export default {
  name: 'ChallengesPage',
  components: { LoadingCircle, ConfirmDialogue, VueForm, VueInput, VueTextSection },
  computed: {
    docsURL() {
      return new URL('/api/docs', api.defaults.baseURL).href
    },
    loadingCircle() {
      return loadingCircle
    },
    dataSelected() {
      return this.data.data
    },
    tableHeaders() {
      return this.tableHeaders
    },
    btnTitle() {
      let defaultText = 'Download proposal'
      return this.LoadingCircleStateDownload ? null : defaultText
    },
    list() {
      // If advanced search is active, return API results directly (already filtered server-side)
      if (this.activeSearchFilters !== null) {
        return this.challengesList
      }

      // Otherwise, apply client-side quick search filter
      const filteredList =
        this.searchString === ''
          ? this.challengesList
          : this.challengesList.filter(
              (item) =>
                item.id.toString() === this.searchString ||
                (item.challenge_year &&
                  typeof item.challenge_year == 'string' &&
                  item.challenge_year
                    .toLowerCase()
                    .includes(this.searchString.toLowerCase().trim())) ||
                (item.challenge_progress &&
                  typeof item.challenge_progress == 'string' &&
                  item.challenge_progress
                    .toLowerCase()
                    .includes(this.searchString.toLowerCase().trim())) ||
                (item.challenge_name &&
                  typeof item.challenge_name == 'string' &&
                  item.challenge_name
                    .toLowerCase()
                    .includes(this.searchString.toLowerCase().trim())) ||
                (item.challenge_author_emails &&
                  typeof item.challenge_author_emails == 'string' &&
                  item.challenge_author_emails
                    .toLowerCase()
                    .includes(this.searchString.toLowerCase().trim())) ||
                this.getConferenceShortName(item.challenge_conference_id)
                  .toLowerCase()
                  .includes(this.searchString.toLowerCase().trim()) ||
                item.challenge_status.toLowerCase().includes(this.searchString.toLowerCase().trim())
            )
      return filteredList
    },
    hasActiveFilters() {
      return this.activeSearchFilters !== null
    },
  },
  data() {
    return {
      searchString: '',
      data: {},
      status: '',
      allowModification: '',
      creator: '',
      tableHeader: ['ID', 'Owner ID', 'Year', 'Conference', 'Name', 'Status', 'Last modified'],
      tableHeaderColumnNames: [
        'id',
        'challenge_owner_id',
        'challenge_year',
        'challenge_conference_id',
        'challenge_name',
        'challenge_status',
        'challenge_modified_time',
      ],
      sortColumn: 'ID', // Track the current sort column
      sortDirection: 'asc', // Track the current sort direction
      selectedRows: [], // Track the selected rows
      selectAll: false, // Track whether all rows are selected
      statusList: [
        'Draft',
        'DraftUpdated',
        'DraftSubmitted',
        'MinorRevisionRequired',
        'MajorRevisionRequired',
        'RevisionUpdated',
        'RevisionSubmitted',
        'Locked',
        'Accept',
        'Reject',
        'AcceptAsLighthouseChallenge',
        'AcceptAsStandardChallenge',
        'AcceptedModified',
        'PrelimAcceptAsStandardChallenge',
        'PrelimAcceptAsLighthouseChallenge',
        'RevisionUpdatedPrelimAccept',
        'RevisionSubmittedPrelimAccept',
        'AcceptedModifiedDraft',
        'AcceptedModifiedUpdated',
        'AcceptedModifiedSubmitted',
        'Deleted',
        'CleanProposal',
      ],
      allowModificationList: ['Allow further modification', "Don't allow further modification"],
      challengesList: [],
      // creatorList: [],
      // creatorListText: [],
      failMessageCreator: null,
      current_password: null,
      LoadingCircleState: true,
      LoadingCircleStateDownload: false,
      currentPage: 1,
      itemsPerPage: 100,
      itemsPerPageOptions: [20, 50, 100, 200],
      totalItems: 0,
      bulkStatusSelected: '',
      bulkAllowModificationSelected: '',
      bulkCurrentPassword: '',
      showBulkStatusPanel: false,
      showBulkAllowModPanel: false,
      showBulkPrunePanel: false,
      showSearchPanel: false,
      conferenceShortNames: {},
      searchFilters: {
        id: '',
        year_operator: '',
        challenge_year: '',
        challenge_year2: '',
        challenge_name: '',
        challenge_status: '',
        challenge_owner_id: '',
        challenge_is_lighthouse_challenge: '',
        submission_time_operator: '',
        submission_time_date1: '',
        submission_time_date2: '',
      },
      activeSearchFilters: null,
    }
  },
  mounted() {
    if (this.$route.params.id && !this.dataSelected) {
      this.$router.push({ name: 'Challenges' })
    }
  },
  async created() {
    await Promise.all([this.getAndSetChallengeAll(), this.getAndSetConferenceShortNames()])
    // await this.getAndSetUserAll()
  },
  methods: {
    StringToPrettyDate,
    useAuthStore,
    async getAndSetConferenceShortNames() {
      const payload = {
        output_filters: ['id', 'short_name'],
      }
      await apiPost('/admin/conference/all?limit=1000&offset=0', payload)
        .then((resp) => {
          const conferenceShortNames = {}
          ;(resp?.content || []).forEach((conference) => {
            conferenceShortNames[conference.id] = conference.short_name || `#${conference.id}`
          })
          this.conferenceShortNames = conferenceShortNames
        })
        .catch(() => {
          this.conferenceShortNames = {}
        })
    },
    getConferenceShortName(conferenceId) {
      if (!conferenceId) return '-'
      return this.conferenceShortNames[conferenceId] || `#${conferenceId}`
    },
    async getAndSetChallengeAll() {
      const offset = (this.currentPage - 1) * this.itemsPerPage
      const apiEndpoint = `/admin/challenge/all?limit=${this.itemsPerPage}&offset=${offset}`
      const output_filters = [
        'id',
        'challenge_name',
        'challenge_author_names',
        'challenge_author_emails',
        'challenge_year',
        'challenge_acronym',
        'challenge_conference_id',
        'challenge_owner_id',
        'challenge_status',
        'challenge_created_time',
        'challenge_modified_time',
        'challenge_submission_time',
        'challenge_file',
      ]
      let payload = {
        output_filters,
        search_filters: this.activeSearchFilters,
      }
      await apiPost(apiEndpoint, payload)
        .then((resp) => {
          this.challengesList = resp['content']
          this.totalItems = resp['total_records']
          this.LoadingCircleState = false
        })
        .catch((e) => {
          this.LoadingCircleState = false
          if (e.message.includes('No Challenge found') || e.message.includes('not found')) {
            this.challengesList = []
            this.totalItems = 0
            useToastAlertStore().showAlert('No challenges found matching criteria', 'info', 3000)
          } else {
            useToastAlertStore().showAlert(e.message, 'danger', 6000)
          }
        })
    },
    buildSearchFilters() {
      const filters = {}

      // Challenge ID - exact match
      if (this.searchFilters.id) {
        filters.id = this.searchFilters.id
      }

      // Challenge Year - with operators
      if (this.searchFilters.year_operator && this.searchFilters.challenge_year) {
        if (this.searchFilters.year_operator === 'eq') {
          filters.challenge_year = this.searchFilters.challenge_year
        } else if (this.searchFilters.year_operator === 'lt') {
          filters.challenge_year__lt = this.searchFilters.challenge_year
        } else if (this.searchFilters.year_operator === 'gt') {
          filters.challenge_year__gt = this.searchFilters.challenge_year
        } else if (
          this.searchFilters.year_operator === 'between' &&
          this.searchFilters.challenge_year2
        ) {
          filters.challenge_year__between = [
            this.searchFilters.challenge_year,
            this.searchFilters.challenge_year2,
          ]
        }
      }

      // Challenge Name - contains search
      if (this.searchFilters.challenge_name) {
        filters.challenge_name__ilike = `%${this.searchFilters.challenge_name}%`
      }

      // Challenge Status - exact match
      if (this.searchFilters.challenge_status) {
        filters.challenge_status = this.searchFilters.challenge_status
      }

      // Challenge Owner ID - exact match
      if (this.searchFilters.challenge_owner_id) {
        filters.challenge_owner_id = this.searchFilters.challenge_owner_id
      }

      // Is Lighthouse Challenge - boolean
      if (this.searchFilters.challenge_is_lighthouse_challenge !== '') {
        filters.challenge_is_lighthouse_challenge =
          this.searchFilters.challenge_is_lighthouse_challenge === 'true'
      }

      // Submission Time - with operators
      if (this.searchFilters.submission_time_operator && this.searchFilters.submission_time_date1) {
        const date1 = new Date(this.searchFilters.submission_time_date1).toISOString()

        if (this.searchFilters.submission_time_operator === 'lt') {
          filters.challenge_submission_time__lt = date1
        } else if (this.searchFilters.submission_time_operator === 'gt') {
          filters.challenge_submission_time__gt = date1
        } else if (
          this.searchFilters.submission_time_operator === 'between' &&
          this.searchFilters.submission_time_date2
        ) {
          const date2 = new Date(this.searchFilters.submission_time_date2).toISOString()
          filters.challenge_submission_time__between = [date1, date2]
        }
      }

      return Object.keys(filters).length > 0 ? filters : null
    },
    applySearch() {
      this.activeSearchFilters = this.buildSearchFilters()
      this.currentPage = 1 // Reset to first page when applying search
      this.getAndSetChallengeAll()

      if (this.activeSearchFilters) {
        useToastAlertStore().showAlert('Search filters applied', 'success', 3000)
      } else {
        useToastAlertStore().showAlert('No filters to apply', 'info', 3000)
      }
    },
    clearSearch() {
      // Reset all search filter fields
      this.searchFilters = {
        id: '',
        year_operator: '',
        challenge_year: '',
        challenge_year2: '',
        challenge_name: '',
        challenge_status: '',
        challenge_owner_id: '',
        challenge_is_lighthouse_challenge: '',
        submission_time_operator: '',
        submission_time_date1: '',
        submission_time_date2: '',
      }
      this.activeSearchFilters = null
      this.currentPage = 1
      this.getAndSetChallengeAll()
      useToastAlertStore().showAlert('Search filters cleared', 'success', 3000)
    },
    // async getAndSetUserAll() {
    //   await apiPost('/admin/user/all/?limit=10&offset=0').then((resp) => {
    //     this.creatorList = resp["content"]
    //     this.getCreatorText()
    //   })
    // },
    selectData(item, idx) {
      this.data = {
        data: item,
        index: idx,
      }
      this.status = this.setStatusText()
      // this.creator = this.dataSelected?.challenge_author_names[0] !== null ? this.dataSelected.challenge_author_names[0] : "No author name";
      // this.creator = this.dataSelected?.challenge_author_names !== null ? this.dataSelected.challenge_author_names : "No author name";
      this.$router.push({ name: 'Challenges Overview', params: { id: item.id } })
    },
    unselectData() {
      this.data = {}
      this.searchString = ''
      this.failMessageCreator = null
    },
    async downloadChallenge(id) {
      if (Number.isInteger(id)) {
        this.LoadingCircleStateDownload = true
        await apiGetDownload(`/admin/challenge/${id}/download`, {
          responseType: 'blob',
        })
          .then((response) => {
            const contentType = response.headers['content-type']
            const blob = new Blob([response.data], { type: 'application/pdf' })
            const url = window.URL.createObjectURL(blob)
            const link = document.createElement('a')

            link.href = url
            const filenameSection =
              response.headers['x-content-filename'] || 'Challenge_proposal.pdf'
            let decodedFilename = decodeURIComponent(filenameSection)
            link.setAttribute('download', decodedFilename)
            document.body.appendChild(link)
            link.click()
            link.remove()
            window.URL.revokeObjectURL(url)
            this.LoadingCircleStateDownload = false
          })
          .catch((e) => {
            this.LoadingCircleStateDownload = false
            useToastAlertStore().showAlert(e, 'danger', 6000)
          })
      }
    },
    async registerChallenge() {
      // await apiGet(`challenge/${challengeId}/download`)
      //   .then(() => {
      //     useToastAlertStore().showAlert('The challenge was registered', 'success')
      //   })
      //   .catch((resp) => {
      //     useToastAlertStore().showAlert(resp, 'danger', 6000)
      //   })
    },

    async setAllowModification() {
      let is_allowed_for_further_editing = false
      if (this.allowModification === this.allowModificationList[0]) {
        is_allowed_for_further_editing = true
      }
      // let challenge_locked = this.setLocked(challenge_status)
      let data = {
        is_allowed_for_further_editing: is_allowed_for_further_editing,
      }
      await apiPut(`admin/challenge/${this.dataSelected?.id}/update`, data)
        .then(() => {
          useToastAlertStore().showAlert('Challenge updated', 'success')
        })
        .catch((e) => {
          useToastAlertStore().showAlert(e, 'danger', 6000)
        })
    },
    async setStatus() {
      let challenge_status = this.setStatusCamelCase()
      // let challenge_locked = this.setLocked(challenge_status)
      let newStatus = {
        challenge_status: challenge_status,
      }
      await apiPut(`admin/challenge/${this.dataSelected?.id}/status`, newStatus)
        .then(() => {
          useToastAlertStore().showAlert('The status was changed', 'success')
        })
        .catch((e) => {
          useToastAlertStore().showAlert(e, 'danger', 6000)
        })
    },
    setStatusCamelCase() {
      switch (this.status) {
        case 'Draft submitted':
          return 'DraftSubmitted'
        case 'Draft updated':
          return 'DraftUpdated'
        case 'Revision updated':
          return 'RevisionUpdated'
        case 'Revision submitted':
          return 'RevisionSubmitted'
        case 'Registered but submitted':
          return 'RevisionSubmitted'
        case 'Major revision required':
          return 'MajorRevisionRequired'
        case 'Minor revision required':
          return 'MinorRevisionRequired'
        case 'Submitted new parameters and waiting for feedback':
          return 'SubmittedNewParametersAndWaitingForFeedback'
        case 'Revision of submitted new parameters':
          return 'RevisionOfSubmittedNewParameters'
        case 'Accept as lighthouse challenge':
          return 'AcceptAsLighthouseChallenge'
        case 'Accept as standard challenge':
          return 'AcceptAsStandardChallenge'
        case 'Preliminary accept as lighthouse challenge (subject to minor revision)':
          return 'PrelimAcceptAsLighthouseChallenge'
        case 'Preliminary accept as standard challenge (subject to minor revision)':
          return 'PrelimAcceptAsStandardChallenge'
        case 'Accepted modified':
          return 'AcceptedModified'
        case 'Revision updated for preliminary accept':
          return 'RevisionUpdatedPrelimAccept'
        case 'Revision submitted for preliminary accept':
          return 'RevisionSubmittedPrelimAccept'
        case 'Accepted modified draft':
          return 'AcceptedModifiedDraft'
        case 'Accepted modified updated':
          return 'AcceptedModifiedUpdated'
        case 'Accepted modified submitted':
          return 'AcceptedModifiedSubmitted'
        case 'Clean/Unmark proposal':
          return 'CleanProposal'
        default:
          return this.status
      }
    },
    setStatusPretty(status) {
      switch (status) {
        case 'Draft':
          return 'Draft ⚪'
        case 'DraftSubmitted':
          return 'Draft submitted 🟢'
        case 'DraftUpdated':
          return 'Draft updated 🟡'
        case 'RevisionSubmitted':
          return 'Revision submitted 🟢'
        case 'MajorRevisionRequired':
          return 'Major revision required ‼️'
        case 'MinorRevisionRequired':
          return 'Minor revision required ❗'
        case 'SubmittedNewParametersAndWaitingForFeedback':
          return 'Submitted new parameters and waiting for feedback 🟢'
        case 'RevisionOfSubmittedNewParameters':
          return 'Revision of submitted new parameters'
        case 'Accept':
          return 'Accept ✔️'
        case 'Reject':
          return 'Reject ❌'
        case 'AcceptAsLighthouseChallenge':
          return 'Accept as lighthouse challenge ✔️'
        case 'AcceptAsStandardChallenge':
          return 'Accept as standard challenge ✔️'
        case 'PrelimAcceptAsLighthouseChallenge':
          return 'Preliminary accept as lighthouse challenge (subject to minor revision)'
        case 'PrelimAcceptAsStandardChallenge':
          return 'Preliminary accept as standard challenge (subject to minor revision)'
        case 'CleanProposal':
          return 'Clean/Unmark proposal 🧹'
        default:
          return status
      }
    },
    // setLocked(challenge_status) {
    //   const validStatuses = ['DraftSubmitted', 'RevisionSubmitted', 'Accept', 'Reject', 'Deleted'];
    //   return validStatuses.includes(challenge_status);
    // },
    setStatusText() {
      switch (this.dataSelected?.challenge_status) {
        case 'DraftSubmitted':
          return 'Draft submitted'
        case 'DraftUpdated':
          return 'Draft updated'
        case 'RevisionSubmitted':
          return 'Revision submitted'
        case 'MajorRevisionRequired':
          return 'Major revision required'
        case 'MinorRevisionRequired':
          return 'Minor revision required'
        case 'SubmittedNewParametersAndWaitingForFeedback':
          return 'Submitted new parameters and waiting for feedback'
        case 'RevisionOfSubmittedNewParameters':
          return 'Revision of submitted new parameters'
        case 'AcceptAsLighthouseChallenge':
          return 'Accept as lighthouse challenge'
        case 'AcceptAsStandardChallenge':
          return 'Accept as standard challenge'
        case 'PrelimAcceptAsLighthouseChallenge':
          return 'Preliminary accept as lighthouse challenge (subject to minor revision)'
        case 'PrelimAcceptAsStandardChallenge':
          return 'Preliminary accept as standard challenge (subject to minor revision)'
        case 'CleanProposal':
          return 'Clean/Unmark proposal'
        default:
          return this.dataSelected?.challenge_status
      }
    },
    async setCreator() {
      this.failMessageCreator = null
      // this.dataSelected.challenge_author_names = [this.creator]
      await apiPut(`admin/challenge/${this.dataSelected?.id}/update`, this.dataSelected)
        .then((resp) => {
          if (resp?.name && resp?.name === 'AxiosError') {
            this.failMessageCreator = resp?.response?.data.detail
          } else {
            useToastAlertStore().showAlert('Another user has been assigned', 'success')
          }
        })
        .catch((e) => {
          useToastAlertStore().showAlert(e, 'danger', 6000)
        })
    },
    // getCreatorText() {
    //   this.creatorList.forEach((creator) => {
    //     this.creatorListText.push(creator.first_name + ' ' + creator.last_name)
    //   })
    // },
    async deleteChallenge() {
      const ok = await this.$refs.confirmDialogue.show({
        title: 'Prune challenge proposal',
        message: 'Are you sure you want to prune this challenge? It cannot be undone.',
        okButton: 'Prune forever',
        okButtonTheme: 'btn-danger',
      })
      if (ok) {
        await apiDelete(
          `admin/challenge/${this.dataSelected?.id}/prune?active_user_password=${encodeURIComponent(
            this.current_password
          )}`
        )
          .then(() => {
            useToastAlertStore().showAlert('The challenge was finally deleted', 'success')
            setTimeout(1000)
            location.reload()
          })
          .catch((e) => {
            useToastAlertStore().showAlert(e, 'danger', 6000)
          })
      } else {
      }
    },
    changePage(page) {
      if (page >= 1 && page <= Math.ceil(this.totalItems / this.itemsPerPage)) {
        this.currentPage = page
      }
    },
    changeItemsPerPage(option) {
      this.itemsPerPage = option
      this.currentPage = 1 // Reset to the first page when items per page changes
      this.getAndSetChallengeAll()
    },
    sortTable(column) {
      // Toggle sort direction if the same column is clicked again
      if (this.sortColumn === column) {
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc'
      } else {
        // Reset sort direction if a new column is clicked
        this.sortDirection = 'asc'
      }

      this.sortColumn = column
      let idx = this.tableHeader.indexOf(column)

      // Perform sorting based on the selected column and direction
      this.list.sort((a, b) => {
        const valueA =
          column === 'Conference'
            ? this.getSortableValue(this.getConferenceShortName(a.challenge_conference_id))
            : this.getSortableValue(a[this.tableHeaderColumnNames[idx]])
        const valueB =
          column === 'Conference'
            ? this.getSortableValue(this.getConferenceShortName(b.challenge_conference_id))
            : this.getSortableValue(b[this.tableHeaderColumnNames[idx]])

        if (valueA < valueB) {
          return this.sortDirection === 'asc' ? -1 : 1
        }
        if (valueA > valueB) {
          return this.sortDirection === 'asc' ? 1 : -1
        }
        return 0
      })
    },
    getSortableValue(value) {
      // Convert values to a common type for proper sorting
      if (typeof value === 'string') {
        return value.toLowerCase()
      } else if (value instanceof Date) {
        return value.getTime()
      } else {
        return value
      }
    },
    selectAllRows() {
      // Toggle the selection of all rows
      if (this.selectAll) {
        this.selectedRows = this.challengesList.map((item) => item.id)
      } else {
        this.selectedRows = []
      }
    },
    async bulkDownloadChallenges() {
      if (this.selectedRows.length === 0) {
        useToastAlertStore().showAlert('No challenges selected', 'warning', 3000)
        return
      }

      const ok = await this.$refs.confirmDialogue.show({
        title: 'Download Selected Challenges',
        message: `Are you sure you want to download ${this.selectedRows.length} challenge(s)?`,
        okButton: 'Download',
        okButtonTheme: 'btn-primary',
      })

      if (!ok) return

      try {
        this.LoadingCircleStateDownload = true
        await api
          .post('/admin/challenge/bulk-download', this.selectedRows, {
            responseType: 'blob',
          })
          .then((response) => {
            const blob = new Blob([response.data], { type: 'application/zip' })
            const url = window.URL.createObjectURL(blob)
            const link = document.createElement('a')
            link.href = url

            const filenameSection = response.headers['x-content-filename'] || 'challenges.zip'
            let decodedFilename = decodeURIComponent(filenameSection)
            link.setAttribute('download', decodedFilename)
            document.body.appendChild(link)
            link.click()
            link.remove()
            window.URL.revokeObjectURL(url)

            useToastAlertStore().showAlert(
              `${this.selectedRows.length} challenge(s) downloaded successfully`,
              'success'
            )
            this.selectedRows = []
            this.selectAll = false
          })
          .catch((e) => {
            useToastAlertStore().showAlert(e, 'danger', 6000)
          })
      } finally {
        this.LoadingCircleStateDownload = false
      }
    },
    async bulkChangeStatus() {
      if (this.selectedRows.length === 0) {
        useToastAlertStore().showAlert('No challenges selected', 'warning', 3000)
        return
      }

      // If panel is not shown, show it and return
      if (!this.showBulkStatusPanel) {
        this.showBulkStatusPanel = true
        this.showBulkAllowModPanel = false
        this.showBulkPrunePanel = false
        return
      }

      // If panel is shown but no status selected, show toast
      if (!this.bulkStatusSelected) {
        useToastAlertStore().showAlert('Please select a status from the dropdown', 'info', 3000)
        return
      }

      // Execute the bulk status change directly
      try {
        await api
          .put('/admin/challenge/bulk-status', {
            ids: this.selectedRows,
            challenge_status_object: {
              challenge_status: this.bulkStatusSelected,
            },
          })
          .then((response) => {
            useToastAlertStore().showAlert(
              response.data.detail || `Status changed for ${this.selectedRows.length} challenge(s)`,
              'success'
            )
            this.selectedRows = []
            this.selectAll = false
            this.bulkStatusSelected = ''
            this.showBulkStatusPanel = false
            this.getAndSetChallengeAll()
          })
          .catch((e) => {
            useToastAlertStore().showAlert(e?.response?.data?.detail || e.message, 'danger', 6000)
          })
      } catch (e) {
        useToastAlertStore().showAlert(e, 'danger', 6000)
      }
    },
    async bulkAllowModifications() {
      if (this.selectedRows.length === 0) {
        useToastAlertStore().showAlert('No challenges selected', 'warning', 3000)
        return
      }

      // If panel is not shown, show it and return
      if (!this.showBulkAllowModPanel) {
        this.showBulkStatusPanel = false
        this.showBulkAllowModPanel = true
        this.showBulkPrunePanel = false
        return
      }

      // If panel is shown but no option selected, show toast
      if (this.bulkAllowModificationSelected === '') {
        useToastAlertStore().showAlert('Please select an option from the dropdown', 'info', 3000)
        return
      }

      const is_allowed_for_further_editing =
        this.bulkAllowModificationSelected === this.allowModificationList[0]

      // Execute the bulk permission change directly
      try {
        const updates = this.selectedRows.map((id) => ({
          id: id,
          is_allowed_for_further_editing: is_allowed_for_further_editing,
        }))

        await api
          .put('/admin/challenge/bulk-update', updates)
          .then((response) => {
            useToastAlertStore().showAlert(
              response.data.detail ||
                `Modification settings updated for ${this.selectedRows.length} challenge(s)`,
              'success'
            )
            this.selectedRows = []
            this.selectAll = false
            this.bulkAllowModificationSelected = ''
            this.showBulkAllowModPanel = false
            this.getAndSetChallengeAll()
          })
          .catch((e) => {
            useToastAlertStore().showAlert(e?.response?.data?.detail || e.message, 'danger', 6000)
          })
      } catch (e) {
        useToastAlertStore().showAlert(e, 'danger', 6000)
      }
    },
    async bulkPruneChallenges() {
      if (this.selectedRows.length === 0) {
        useToastAlertStore().showAlert('No challenges selected', 'warning', 3000)
        return
      }

      // If panel is not shown, show it and return
      if (!this.showBulkPrunePanel) {
        this.showBulkStatusPanel = false
        this.showBulkAllowModPanel = false
        this.showBulkPrunePanel = true
        return
      }

      // If panel is shown but no password entered, show toast
      if (!this.bulkCurrentPassword) {
        useToastAlertStore().showAlert('Please enter your password to confirm', 'warning', 3000)
        return
      }

      // Execute the bulk prune directly
      try {
        await api
          .delete(
            `/admin/challenge/bulk-prune?active_user_password=${encodeURIComponent(
              this.bulkCurrentPassword
            )}`,
            {
              data: this.selectedRows,
            }
          )
          .then((response) => {
            useToastAlertStore().showAlert(
              response.data.detail ||
                `${this.selectedRows.length} challenge(s) pruned successfully`,
              'success'
            )
            this.selectedRows = []
            this.selectAll = false
            this.bulkCurrentPassword = ''
            this.showBulkPrunePanel = false
            this.getAndSetChallengeAll()
          })
          .catch((e) => {
            useToastAlertStore().showAlert(e?.response?.data?.detail || e.message, 'danger', 6000)
          })
      } catch (e) {
        useToastAlertStore().showAlert(e, 'danger', 6000)
      }
    },
  },
  watch: {
    $route(val) {
      if (val.name === 'Challenges') {
        this.data = {}
        this.searchString = ''
      }
    },
    currentPage: 'getAndSetChallengeAll',
  },
}
</script>

<style scoped>
input[type='checkbox'] {
  transform: scale(1.4);
}

/* Search Panel Styles */
.cursor-pointer {
  cursor: pointer;
}

.cursor-pointer:hover {
  background-color: #f8f9fa;
}

.search-field-group {
  border: 1px solid #dee2e6;
  border-radius: 0.375rem;
  padding: 0.55rem;
  margin: 0.25rem;
  background-color: #f8f9fa;
}

.admin-list-shell {
  width: fit-content;
  max-width: 100%;
}

/* Bulk Operation Modal Styles */
.modal.show {
  display: block;
  animation: fadeIn 0.15s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-backdrop.show {
  opacity: 0.5;
}

.modal-header.bg-warning,
.modal-header.bg-info,
.modal-header.bg-danger {
  border-bottom: none;
}

.modal-header .btn-close-white {
  filter: brightness(0) invert(1);
}

.admin-list-table {
  table-layout: fixed;
}

.admin-list-table th,
.admin-list-table td {
  vertical-align: middle;
}

.table-col-id,
.table-col-owner {
  width: 80px;
  min-width: 80px;
}

.table-col-year {
  width: 90px;
  min-width: 90px;
}

.table-col-name {
  width: 320px;
  min-width: 320px;
}

.table-col-conference {
  width: 140px;
  min-width: 140px;
}

.table-col-status {
  width: 260px;
  min-width: 260px;
}

.table-col-modified {
  width: 150px;
  min-width: 150px;
}

.cell-truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
