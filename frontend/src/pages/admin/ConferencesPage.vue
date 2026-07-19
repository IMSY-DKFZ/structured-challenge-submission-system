<template>
  <div>
    <div
      class="d-flex justify-content-between"
      :class="[dataSelected || showCreatePanel ? 'flex-column' : '']">
      <div class="pb-3">
        <collapse-section name="info">
          <VueTextSection>
            <template #text>
              <p>
                In this view, administrators can manage conferences used by the submission system.
                You can search, create, update, and delete conferences, and you can apply limited
                bulk operations to selected rows.
              </p>
              <p>
                Conference metadata controls proposal availability and the dates shown across the
                system. Be careful when changing proposal windows or deleting conferences, because
                those changes affect organizer flows directly.
              </p>
            </template>
          </VueTextSection>
        </collapse-section>
      </div>
      <div
        v-if="dataSelected || showCreatePanel"
        class="pb-3">
        <button
          type="button"
          class="btn btn-secondary"
          @click="closePanels">
          <i class="be bi-arrow-left pe-1" />
          Go Back
        </button>
      </div>
    </div>

    <div v-if="dataSelected">
      <VueTextSection>
        <div class="row">
          <div class="row col-12 mb-3 p-3">
            <div class="col-12 col-md-6 mb-3">
              <h6 class="mb-0">Conference Name</h6>
              <div class="mb-3 opacity-75">{{ dataSelected?.name }}</div>
            </div>
            <div class="col-12 col-md-3 mb-3">
              <h6 class="mb-0">Short Name</h6>
              <div class="mb-3 opacity-75">{{ dataSelected?.short_name }}</div>
            </div>
            <div class="col-12 col-md-3 mb-3">
              <h6 class="mb-0">Year</h6>
              <div class="mb-3 opacity-75">{{ dataSelected?.year }}</div>
            </div>
            <div class="col-12 col-md-4 mb-3">
              <h6 class="mb-0">ID</h6>
              <div class="mb-3 opacity-75">{{ dataSelected?.id }}</div>
            </div>
            <div class="col-12 col-md-4 mb-3">
              <h6 class="mb-0">Owner ID</h6>
              <div class="mb-3 opacity-75">{{ dataSelected?.owner_id }}</div>
            </div>
            <div class="col-12 col-md-4 mb-3">
              <h6 class="mb-0">Open For Submissions</h6>
              <div class="mb-3 opacity-75">
                <span
                  :class="
                    dataSelected?.is_open_for_submissions
                      ? 'badge text-bg-success'
                      : 'badge text-bg-secondary'
                  ">
                  {{ dataSelected?.is_open_for_submissions ? 'Open' : 'Closed' }}
                </span>
              </div>
            </div>
            <div class="col-12 col-md-4 mb-3">
              <h6 class="mb-0">Lighthouse</h6>
              <div class="mb-3 opacity-75">
                <span
                  :class="
                    dataSelected?.is_lighthouse_challenge
                      ? 'badge text-bg-warning'
                      : 'badge text-bg-light border'
                  ">
                  {{ dataSelected?.is_lighthouse_challenge ? 'Yes' : 'No' }}
                </span>
              </div>
            </div>
            <div class="col-12 col-md-4 mb-3">
              <h6 class="mb-0">Created Time</h6>
              <div class="mb-3 opacity-75 small">
                {{ StringToPrettyDate(dataSelected?.created_time) }}
              </div>
            </div>
            <div class="col-12 col-md-4 mb-3">
              <h6 class="mb-0">Modified Time</h6>
              <div class="mb-3 opacity-75 small">
                {{ StringToPrettyDate(dataSelected?.modified_time) }}
              </div>
            </div>
          </div>

          <div class="col-12 col-lg-8">
            <hr />
            <VueTextSection title-size="h4">
              <template #title>Edit Conference</template>
              <div class="row">
                <div class="col-12 col-md-8">
                  <label class="form-label">Conference Name</label>
                  <input
                    v-model="editForm.name"
                    type="text"
                    class="form-control"
                    placeholder="MICCAI 2027 Challenges" />
                </div>
                <div class="col-12 col-md-4">
                  <label class="form-label">Short Name</label>
                  <input
                    v-model="editForm.short_name"
                    type="text"
                    class="form-control"
                    placeholder="MICCAI" />
                </div>
                <div class="col-12 col-md-4 mt-3">
                  <label class="form-label">Year</label>
                  <input
                    v-model="editForm.year"
                    type="number"
                    class="form-control"
                    placeholder="2027" />
                </div>
                <div class="col-12 col-md-4 mt-3">
                  <label class="form-label">Venue</label>
                  <input
                    v-model="editForm.venue"
                    type="text"
                    class="form-control"
                    placeholder="Conference venue" />
                </div>
                <div class="col-12 col-md-4 mt-3">
                  <label class="form-label">City</label>
                  <input
                    v-model="editForm.city"
                    type="text"
                    class="form-control"
                    placeholder="City" />
                </div>
                <div class="col-12 col-md-6 mt-3">
                  <label class="form-label">Country</label>
                  <input
                    v-model="editForm.country"
                    type="text"
                    class="form-control"
                    placeholder="Country" />
                </div>
                <div class="col-12 col-md-3 mt-3">
                  <div class="form-check mt-4 pt-2">
                    <input
                      id="editOpenForSubmissions"
                      v-model="editForm.is_open_for_submissions"
                      class="form-check-input"
                      type="checkbox" />
                    <label
                      class="form-check-label"
                      for="editOpenForSubmissions">
                      Open for submissions
                    </label>
                  </div>
                </div>
                <div class="col-12 col-md-3 mt-3">
                  <div class="form-check mt-4 pt-2">
                    <input
                      id="editLighthouse"
                      v-model="editForm.is_lighthouse_challenge"
                      class="form-check-input"
                      type="checkbox" />
                    <label
                      class="form-check-label"
                      for="editLighthouse">
                      Lighthouse challenge
                    </label>
                  </div>
                </div>
                <div class="col-12 col-md-6 mt-3">
                  <label class="form-label">Proposal Start Date and Time</label>
                  <input
                    v-model="editForm.proposal_start_date"
                    type="datetime-local"
                    step="1"
                    class="form-control" />
                </div>
                <div class="col-12 col-md-6 mt-3">
                  <label class="form-label">Proposal End Date and Time</label>
                  <input
                    v-model="editForm.proposal_end_date"
                    type="datetime-local"
                    step="1"
                    class="form-control" />
                </div>
                <div class="col-12 col-md-6 mt-3">
                  <label class="form-label">Conference Start Date and Time</label>
                  <input
                    v-model="editForm.start_date"
                    type="datetime-local"
                    step="1"
                    class="form-control" />
                </div>
                <div class="col-12 col-md-6 mt-3">
                  <label class="form-label">Conference End Date and Time</label>
                  <input
                    v-model="editForm.end_date"
                    type="datetime-local"
                    step="1"
                    class="form-control" />
                </div>
                <div class="col-12 mt-3">
                  <label class="form-label">Information</label>
                  <textarea
                    v-model="editForm.information"
                    class="form-control"
                    rows="4"
                    placeholder="Additional conference details"></textarea>
                </div>
                <div class="col-12 mt-3">
                  <label class="form-label">Message Before Generate Proposal</label>
                  <textarea
                    v-model="editForm.message_before_generate_proposal"
                    class="form-control"
                    rows="4"
                    placeholder="Optional message shown to organizers"></textarea>
                </div>
                <div class="col-12 col-md-6 mt-3">
                  <label class="form-label">Chairperson Emails</label>
                  <textarea
                    v-model="editForm.chairperson_emails_text"
                    class="form-control"
                    rows="5"
                    placeholder="One email per line"></textarea>
                  <div class="form-text">One email per line.</div>
                </div>
                <div class="col-12 col-md-6 mt-3">
                  <label class="form-label">Chairperson Names</label>
                  <textarea
                    v-model="editForm.chairperson_names_text"
                    class="form-control"
                    rows="5"
                    placeholder="One name per line"></textarea>
                  <div class="form-text">Optional. One name per line.</div>
                </div>
              </div>
              <button
                type="button"
                class="btn btn-primary mt-4"
                :disabled="updatePending"
                @click="updateConference">
                {{ updatePending ? 'Saving...' : 'Save Conference' }}
              </button>
            </VueTextSection>

            <hr />
            <VueTextSection
              v-if="useAuthStore().adminOnly"
              title-size="h4">
              <VueTextSection :highlight="true">
                <template #title>Delete Conference</template>
                <div class="mb opacity-75">
                  Please enter your current password if you want to delete this conference.
                </div>
                <template #text>This action can not be undone.</template>
                <VueInput
                  label="Current password"
                  type="password"
                  v-model="current_password"></VueInput>
                <button
                  type="button"
                  :disabled="!current_password || deletePending"
                  class="btn btn-danger mt-3"
                  @click="deleteConference(dataSelected.id)">
                  <i class="be bi-trash2-fill" />
                  {{ deletePending ? 'Deleting...' : 'Delete conference' }}
                </button>
              </VueTextSection>
            </VueTextSection>

            <hr />
            <div
              class="alert alert-info"
              role="alert">
              For more admin operations please visit:<br />
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

    <div v-else-if="showCreatePanel">
      <VueTextSection>
        <template #title>Create Conference</template>
        <div class="row">
          <div class="col-12 col-md-8 mt-3">
            <label class="form-label">Conference Name</label>
            <input
              v-model="createForm.name"
              type="text"
              class="form-control"
              placeholder="MICCAI 2027 Challenges" />
          </div>
          <div class="col-12 col-md-4 mt-3">
            <label class="form-label">Short Name</label>
            <input
              v-model="createForm.short_name"
              type="text"
              class="form-control"
              placeholder="MICCAI" />
          </div>
          <div class="col-12 col-md-4 mt-3">
            <label class="form-label">Year</label>
            <input
              v-model="createForm.year"
              type="number"
              class="form-control" />
          </div>
          <div class="col-12 col-md-4 mt-3">
            <label class="form-label">Venue</label>
            <input
              v-model="createForm.venue"
              type="text"
              class="form-control"
              placeholder="Conference venue" />
          </div>
          <div class="col-12 col-md-4 mt-3">
            <label class="form-label">City</label>
            <input
              v-model="createForm.city"
              type="text"
              class="form-control"
              placeholder="City" />
          </div>
          <div class="col-12 col-md-6 mt-3">
            <label class="form-label">Country</label>
            <input
              v-model="createForm.country"
              type="text"
              class="form-control"
              placeholder="Country" />
          </div>
          <div class="col-12 col-md-3 mt-3">
            <div class="form-check mt-4 pt-2">
              <input
                id="createOpenForSubmissions"
                v-model="createForm.is_open_for_submissions"
                class="form-check-input"
                type="checkbox" />
              <label
                class="form-check-label"
                for="createOpenForSubmissions">
                Open for submissions
              </label>
            </div>
          </div>
          <div class="col-12 col-md-3 mt-3">
            <div class="form-check mt-4 pt-2">
              <input
                id="createLighthouse"
                v-model="createForm.is_lighthouse_challenge"
                class="form-check-input"
                type="checkbox" />
              <label
                class="form-check-label"
                for="createLighthouse">
                Lighthouse challenge
              </label>
            </div>
          </div>
          <div class="col-12 col-md-6 mt-3">
            <label class="form-label">Proposal Start Date and Time</label>
            <input
              v-model="createForm.proposal_start_date"
              type="datetime-local"
              step="1"
              class="form-control" />
          </div>
          <div class="col-12 col-md-6 mt-3">
            <label class="form-label">Proposal End Date and Time</label>
            <input
              v-model="createForm.proposal_end_date"
              type="datetime-local"
              step="1"
              class="form-control" />
          </div>
          <div class="col-12 col-md-6 mt-3">
            <label class="form-label">Conference Start Date and Time</label>
            <input
              v-model="createForm.start_date"
              type="datetime-local"
              step="1"
              class="form-control" />
          </div>
          <div class="col-12 col-md-6 mt-3">
            <label class="form-label">Conference End Date and Time</label>
            <input
              v-model="createForm.end_date"
              type="datetime-local"
              step="1"
              class="form-control" />
          </div>
          <div class="col-12 mt-3">
            <label class="form-label">Information</label>
            <textarea
              v-model="createForm.information"
              class="form-control"
              rows="4"
              placeholder="Additional conference details"></textarea>
          </div>
          <div class="col-12 mt-3">
            <label class="form-label">Message Before Generate Proposal</label>
            <textarea
              v-model="createForm.message_before_generate_proposal"
              class="form-control"
              rows="4"
              placeholder="Optional message shown to organizers"></textarea>
          </div>
          <div class="col-12 col-md-6 mt-3">
            <label class="form-label">Chairperson Emails</label>
            <textarea
              v-model="createForm.chairperson_emails_text"
              class="form-control"
              rows="5"
              placeholder="One email per line"></textarea>
            <div class="form-text">Required. One email per line.</div>
          </div>
          <div class="col-12 col-md-6 mt-3">
            <label class="form-label">Chairperson Names</label>
            <textarea
              v-model="createForm.chairperson_names_text"
              class="form-control"
              rows="5"
              placeholder="One name per line"></textarea>
            <div class="form-text">Optional. One name per line.</div>
          </div>
        </div>
        <button
          type="button"
          class="btn btn-primary mt-4"
          :disabled="createPending"
          @click="createConference">
          {{ createPending ? 'Creating...' : 'Create Conference' }}
        </button>
      </VueTextSection>
    </div>

    <div v-else>
      <div class="admin-list-shell">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <div>
            <h4 class="mb-0">Conference Management</h4>
            <small class="text-muted"
              >Manage conference windows, locations, and chairpersons.</small
            >
          </div>
          <button
            type="button"
            class="btn btn-primary"
            :disabled="LoadingCircleState"
            @click="openCreatePanel">
            <i class="bi bi-plus-circle me-2"></i>Create Conference
          </button>
        </div>

        <div class="card mb-3">
          <div
            class="card-header bg-body-tertiary cursor-pointer"
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
            <div
              class="d-flex gap-2 mb-2 p-2 bg-body-tertiary border border-secondary-subtle rounded">
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">ID</label>
                <input
                  v-model="searchFilters.id"
                  type="number"
                  class="form-control form-control-sm"
                  placeholder="ID" />
              </div>
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">Name</label>
                <input
                  v-model="searchFilters.name"
                  type="text"
                  class="form-control form-control-sm"
                  placeholder="Conference name contains..." />
              </div>
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">Short Name</label>
                <input
                  v-model="searchFilters.short_name"
                  type="text"
                  class="form-control form-control-sm"
                  placeholder="MICCAI" />
              </div>
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">Owner ID</label>
                <input
                  v-model="searchFilters.owner_id"
                  type="number"
                  class="form-control form-control-sm"
                  placeholder="Owner ID" />
              </div>
            </div>

            <div
              class="d-flex gap-2 mb-2 p-2 bg-body-tertiary border border-secondary-subtle rounded">
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">Year</label>
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
                  v-model="searchFilters.year"
                  type="number"
                  class="form-control form-control-sm"
                  :disabled="!searchFilters.year_operator" />
              </div>
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">To Year</label>
                <input
                  v-model="searchFilters.year2"
                  type="number"
                  class="form-control form-control-sm"
                  :disabled="searchFilters.year_operator !== 'between'" />
              </div>
            </div>

            <div
              class="d-flex gap-2 mb-2 p-2 bg-body-tertiary border border-secondary-subtle rounded">
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">City</label>
                <input
                  v-model="searchFilters.city"
                  type="text"
                  class="form-control form-control-sm"
                  placeholder="City contains..." />
              </div>
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">Country</label>
                <input
                  v-model="searchFilters.country"
                  type="text"
                  class="form-control form-control-sm"
                  placeholder="Country contains..." />
              </div>
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">Open For Submissions</label>
                <select
                  v-model="searchFilters.is_open_for_submissions"
                  class="form-select form-select-sm">
                  <option value="">All</option>
                  <option value="true">Open</option>
                  <option value="false">Closed</option>
                </select>
              </div>
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">Lighthouse</label>
                <select
                  v-model="searchFilters.is_lighthouse_challenge"
                  class="form-select form-select-sm">
                  <option value="">All</option>
                  <option value="true">Yes</option>
                  <option value="false">No</option>
                </select>
              </div>
            </div>

            <div
              class="d-flex gap-2 mb-2 p-2 bg-body-tertiary border border-secondary-subtle rounded">
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">Proposal Start</label>
                <select
                  v-model="searchFilters.proposal_start_operator"
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
                  v-model="searchFilters.proposal_start_date1"
                  type="date"
                  class="form-control form-control-sm"
                  :disabled="!searchFilters.proposal_start_operator" />
              </div>
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">To Date</label>
                <input
                  v-model="searchFilters.proposal_start_date2"
                  type="date"
                  class="form-control form-control-sm"
                  :disabled="searchFilters.proposal_start_operator !== 'between'" />
              </div>
            </div>

            <div
              class="d-flex gap-2 mb-2 p-2 bg-body-tertiary border border-secondary-subtle rounded">
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">Proposal End</label>
                <select
                  v-model="searchFilters.proposal_end_operator"
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
                  v-model="searchFilters.proposal_end_date1"
                  type="date"
                  class="form-control form-control-sm"
                  :disabled="!searchFilters.proposal_end_operator" />
              </div>
              <div class="w-100">
                <label class="form-label small fw-bold text-nowrap">To Date</label>
                <input
                  v-model="searchFilters.proposal_end_date2"
                  type="date"
                  class="form-control form-control-sm"
                  :disabled="searchFilters.proposal_end_operator !== 'between'" />
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
            :placeholder="'Filter current page by ID, year, name, short name, city, country'"></VueInput>
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
                @click="openBulkUpdateModal"
                :class="{ disabled: selectedRows.length === 0 }"
                href="#"
                ><i class="bi bi-pencil-square me-2"></i>Bulk Update Selected ({{
                  selectedRows.length
                }})</a
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
                @click.prevent="changePage(currentPage - 1)"
                aria-label="Previous"
                href="#">
                <span aria-hidden="true">&laquo;</span>
              </a>
            </li>
            <li
              class="page-item"
              v-for="page in visiblePages"
              :key="page"
              :class="{ active: currentPage === page }">
              <a
                class="page-link"
                @click.prevent="changePage(page)"
                :aria-current="currentPage === page ? 'page' : undefined"
                href="#"
                >{{ page }}</a
              >
            </li>
            <li
              class="page-item"
              :class="{
                disabled: currentPage === totalPages || totalPages === 0,
              }">
              <a
                class="page-link"
                @click.prevent="changePage(currentPage + 1)"
                aria-label="Next"
                href="#">
                <span aria-hidden="true">&raquo;</span>
              </a>
            </li>
          </ul>
        </div>

        <div class="table-responsive">
          <table class="table table-striped table-hover">
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
                  :key="item"
                  @click="sortTable(item)">
                  <a
                    href="#"
                    @click.prevent
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
                :key="item.id"
                style="cursor: pointer"
                @click="selectData(item)">
                <td @click.stop>
                  <input
                    type="checkbox"
                    v-model="selectedRows"
                    :value="item.id" />
                </td>
                <th scope="row">{{ item.id }}</th>
                <td>{{ item.year }}</td>
                <td>{{ item.name }}</td>
                <td>{{ item.city }}</td>
                <td>{{ item.country }}</td>
                <td>{{ dateRangeLabel(item.proposal_start_date, item.proposal_end_date) }}</td>
                <td>
                  <span
                    :class="
                      item.is_open_for_submissions
                        ? 'badge text-bg-success'
                        : 'badge text-bg-secondary'
                    ">
                    {{ item.is_open_for_submissions ? 'Open' : 'Closed' }}
                  </span>
                </td>
                <td>
                  <span
                    :class="
                      item.is_lighthouse_challenge
                        ? 'badge text-bg-warning'
                        : 'badge text-bg-light border'
                    ">
                    {{ item.is_lighthouse_challenge ? 'Yes' : 'No' }}
                  </span>
                </td>
                <td>
                  <small>{{ StringToPrettyDate(item.modified_time) }}</small>
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
                @click.prevent="changePage(currentPage - 1)"
                aria-label="Previous"
                href="#">
                <span aria-hidden="true">&laquo;</span>
              </a>
            </li>
            <li
              class="page-item"
              v-for="page in visiblePages"
              :key="page"
              :class="{ active: currentPage === page }">
              <a
                class="page-link"
                @click.prevent="changePage(page)"
                :aria-current="currentPage === page ? 'page' : undefined"
                href="#"
                >{{ page }}</a
              >
            </li>
            <li
              class="page-item"
              :class="{
                disabled: currentPage === totalPages || totalPages === 0,
              }">
              <a
                class="page-link"
                @click.prevent="changePage(currentPage + 1)"
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

    <div
      class="modal fade"
      :class="{ show: showBulkUpdatePanel, 'd-block': showBulkUpdatePanel }"
      tabindex="-1"
      @click.self="closeBulkUpdateModal"
      @keydown.esc="closeBulkUpdateModal">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-info text-white">
            <h5 class="modal-title">
              <i class="bi bi-pencil-square me-2"></i>Bulk Update Conferences
            </h5>
            <button
              type="button"
              class="btn-close btn-close-white"
              aria-label="Close"
              @click="closeBulkUpdateModal"></button>
          </div>
          <div class="modal-body">
            <p class="mb-3">
              <strong>{{ selectedRows.length }}</strong> conference(s) selected
            </p>
            <div class="mb-3">
              <label class="form-label fw-bold">Open For Submissions</label>
              <select
                v-model="bulkUpdate.open_for_submissions"
                class="form-select">
                <option value="">No change</option>
                <option value="true">Set Open</option>
                <option value="false">Set Closed</option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold">Lighthouse</label>
              <select
                v-model="bulkUpdate.is_lighthouse_challenge"
                class="form-select">
                <option value="">No change</option>
                <option value="true">Mark as lighthouse</option>
                <option value="false">Unmark lighthouse</option>
              </select>
            </div>
            <div class="alert alert-info small mb-0">
              Only the selected bulk fields will be updated.
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              @click="closeBulkUpdateModal">
              Cancel
            </button>
            <button
              type="button"
              class="btn btn-info"
              :disabled="bulkUpdatePending"
              @click="bulkUpdateConferences">
              <i class="bi bi-check-circle me-2"></i
              >{{ bulkUpdatePending ? 'Applying...' : 'Apply' }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <div
      v-if="showBulkUpdatePanel"
      class="modal-backdrop fade show"></div>

    <div
      class="modal fade"
      :class="{ show: showBulkDeletePanel, 'd-block': showBulkDeletePanel }"
      tabindex="-1"
      @click.self="closeBulkDeleteModal"
      @keydown.esc="closeBulkDeleteModal">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-danger text-white">
            <h5 class="modal-title">
              <i class="bi bi-trash2-fill me-2"></i>Delete Multiple Conferences
            </h5>
            <button
              type="button"
              class="btn-close btn-close-white"
              aria-label="Close"
              @click="closeBulkDeleteModal"></button>
          </div>
          <div class="modal-body">
            <p class="mb-3">
              <strong>{{ selectedRows.length }}</strong> conference(s) selected
            </p>
            <div class="alert alert-danger mb-3">
              <strong>Warning:</strong> This will permanently delete the selected conferences.
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold">Enter Your Password to Confirm</label>
              <input
                v-model="bulkCurrentPassword"
                type="password"
                class="form-control"
                placeholder="Enter your current password"
                @keyup.enter="bulkDeleteConferences" />
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              @click="closeBulkDeleteModal">
              Cancel
            </button>
            <button
              type="button"
              class="btn btn-danger"
              :disabled="!bulkCurrentPassword || bulkDeletePending"
              @click="bulkDeleteConferences">
              <i class="bi bi-exclamation-triangle me-2"></i
              >{{ bulkDeletePending ? 'Deleting...' : 'Delete Forever' }}
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
import ConfirmDialogue from '@/components/ConfirmDialogue.vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'
import { apiDelete, apiGet, apiPost, apiPut } from '@/api/api'
import LoadingCircle from '@/components/LoadingCircle.vue'
import { useToastAlertStore } from '@/stores/toastAlert'
import StringToPrettyDate from '../../helper/format'

const createEmptyConferenceForm = () => ({
  name: '',
  short_name: '',
  year: '',
  information: '',
  venue: '',
  city: '',
  country: '',
  proposal_start_date: '',
  proposal_end_date: '',
  start_date: '',
  end_date: '',
  is_lighthouse_challenge: false,
  is_open_for_submissions: true,
  chairperson_emails_text: '',
  chairperson_names_text: '',
  message_before_generate_proposal: '',
})

export default {
  name: 'ConferencesPage',
  components: {
    LoadingCircle,
    ConfirmDialogue,
    VueInput,
    CollapseSection,
    VueTextSection,
  },
  data() {
    return {
      LoadingCircleState: true,
      data: {},
      showCreatePanel: false,
      current_password: '',
      searchString: '',
      tableHeader: [
        'ID',
        'Year',
        'Name',
        'City',
        'Country',
        'Proposal Period',
        'Open',
        'Lighthouse',
        'Last Modified',
      ],
      tableHeaderColumnNames: [
        'id',
        'year',
        'name',
        'city',
        'country',
        'proposal_start_date',
        'is_open_for_submissions',
        'is_lighthouse_challenge',
        'modified_time',
      ],
      conferencesList: [],
      currentPage: 1,
      itemsPerPage: 100,
      itemsPerPageOptions: [20, 50, 100, 200],
      totalItems: 0,
      totalPages: 0,
      listLoaded: false,
      listRequestId: 0,
      detailRequestId: 0,
      showSearchPanel: false,
      searchFilters: {
        id: '',
        name: '',
        short_name: '',
        owner_id: '',
        year_operator: '',
        year: '',
        year2: '',
        city: '',
        country: '',
        is_open_for_submissions: '',
        is_lighthouse_challenge: '',
        proposal_start_operator: '',
        proposal_start_date1: '',
        proposal_start_date2: '',
        proposal_end_operator: '',
        proposal_end_date1: '',
        proposal_end_date2: '',
      },
      activeSearchFilters: null,
      sortColumn: 'ID',
      sortDirection: 'asc',
      selectedRows: [],
      selectAll: false,
      createForm: createEmptyConferenceForm(),
      editForm: createEmptyConferenceForm(),
      showBulkUpdatePanel: false,
      showBulkDeletePanel: false,
      bulkUpdate: {
        open_for_submissions: '',
        is_lighthouse_challenge: '',
      },
      bulkCurrentPassword: '',
      createPending: false,
      updatePending: false,
      deletePending: false,
      bulkUpdatePending: false,
      bulkDeletePending: false,
    }
  },
  async created() {
    if (this.$route.params.id) {
      await this.getConferenceById(Number(this.$route.params.id))
    } else {
      await this.getAndSetConferenceAll()
    }
  },
  methods: {
    useAuthStore,
    StringToPrettyDate,
    dateRangeLabel(start, end) {
      const startLabel = start ? this.dateLabelValue(start) : '-'
      const endLabel = end ? this.dateLabelValue(end) : '-'
      return `${startLabel} to ${endLabel}`
    },
    dateLabelValue(value) {
      if (!value) return ''
      const rawValue = String(value)
      if (/^\d{4}-\d{2}-\d{2}T/.test(rawValue) && !/(Z|[+-]\d{2}:\d{2})$/.test(rawValue)) {
        return rawValue.slice(0, 10)
      }
      const date = new Date(value)
      if (Number.isNaN(date.getTime())) return ''
      const pad = (part) => String(part).padStart(2, '0')
      return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`
    },
    datetimeInputValue(value) {
      if (!value) return ''
      const rawValue = String(value)
      if (
        /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}/.test(rawValue) &&
        !/(Z|[+-]\d{2}:\d{2})$/.test(rawValue)
      ) {
        return rawValue.slice(0, 19)
      }
      const date = new Date(value)
      if (Number.isNaN(date.getTime())) return ''
      const pad = (part) => String(part).padStart(2, '0')
      return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(
        date.getHours()
      )}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`
    },
    datetimePayloadValue(value) {
      if (!value) return null
      return value.length === 16 ? `${value}:00` : value
    },
    normalizeLines(value) {
      if (!value) return []
      return value
        .split(/\r?\n|,/)
        .map((item) => item.trim())
        .filter((item) => item !== '')
    },
    arrayToLines(value) {
      if (!Array.isArray(value)) return ''
      return value.join('\n')
    },
    buildConferencePayload(form) {
      return {
        name: form.name?.trim(),
        short_name: form.short_name?.trim(),
        year: Number(form.year),
        information: form.information?.trim() || null,
        venue: form.venue?.trim() || null,
        city: form.city?.trim() || null,
        country: form.country?.trim() || null,
        proposal_start_date: this.datetimePayloadValue(form.proposal_start_date),
        proposal_end_date: this.datetimePayloadValue(form.proposal_end_date),
        start_date: this.datetimePayloadValue(form.start_date),
        end_date: this.datetimePayloadValue(form.end_date),
        is_lighthouse_challenge: Boolean(form.is_lighthouse_challenge),
        is_open_for_submissions: Boolean(form.is_open_for_submissions),
        chairperson_emails: this.normalizeLines(form.chairperson_emails_text),
        chairperson_names: this.normalizeLines(form.chairperson_names_text),
        message_before_generate_proposal: form.message_before_generate_proposal?.trim() || null,
      }
    },
    validateConferenceForm(form) {
      const requiredFields = [
        ['Conference name', form.name],
        ['Short name', form.short_name],
        ['Year', form.year],
        ['Proposal start date', form.proposal_start_date],
        ['Proposal end date', form.proposal_end_date],
        ['Conference start date', form.start_date],
        ['Conference end date', form.end_date],
      ]

      for (const [label, value] of requiredFields) {
        if (
          value === null ||
          value === undefined ||
          value === '' ||
          (typeof value === 'string' && value.trim() === '')
        ) {
          useToastAlertStore().showAlert(`${label} is required`, 'warning', 4000)
          return false
        }
      }

      if (!/^\d{4}$/.test(String(form.year))) {
        useToastAlertStore().showAlert('Year must be a four-digit number', 'warning', 4000)
        return false
      }

      const chairpersonEmails = this.normalizeLines(form.chairperson_emails_text)
      if (chairpersonEmails.length === 0) {
        useToastAlertStore().showAlert(
          'At least one chairperson email is required',
          'warning',
          4000
        )
        return false
      }
      const invalidEmail = chairpersonEmails.find(
        (email) => !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
      )
      if (invalidEmail) {
        useToastAlertStore().showAlert(
          `Invalid chairperson email: ${invalidEmail}`,
          'warning',
          4000
        )
        return false
      }

      const proposalStart = new Date(form.proposal_start_date)
      const proposalEnd = new Date(form.proposal_end_date)
      const conferenceStart = new Date(form.start_date)
      const conferenceEnd = new Date(form.end_date)

      if (proposalStart > proposalEnd) {
        useToastAlertStore().showAlert(
          'Proposal start date must be before proposal end date',
          'warning',
          4000
        )
        return false
      }
      if (conferenceStart > conferenceEnd) {
        useToastAlertStore().showAlert(
          'Conference start date must be before conference end date',
          'warning',
          4000
        )
        return false
      }

      return true
    },
    populateEditForm(item) {
      this.editForm = {
        name: item?.name || '',
        short_name: item?.short_name || '',
        year: item?.year || '',
        information: item?.information || '',
        venue: item?.venue || '',
        city: item?.city || '',
        country: item?.country || '',
        proposal_start_date: this.datetimeInputValue(item?.proposal_start_date),
        proposal_end_date: this.datetimeInputValue(item?.proposal_end_date),
        start_date: this.datetimeInputValue(item?.start_date),
        end_date: this.datetimeInputValue(item?.end_date),
        is_lighthouse_challenge: Boolean(item?.is_lighthouse_challenge),
        is_open_for_submissions: Boolean(item?.is_open_for_submissions),
        chairperson_emails_text: this.arrayToLines(item?.chairperson_emails),
        chairperson_names_text: this.arrayToLines(item?.chairperson_names),
        message_before_generate_proposal: item?.message_before_generate_proposal || '',
      }
    },
    async closePanels() {
      this.data = {}
      this.showCreatePanel = false
      this.current_password = ''
      if (this.$route.name !== 'Admin Conferences') {
        await this.$router.push({ name: 'Admin Conferences' })
      }
    },
    openCreatePanel() {
      this.showCreatePanel = true
      this.data = {}
      this.createForm = createEmptyConferenceForm()
    },
    clearSelection() {
      this.selectedRows = []
      this.selectAll = false
    },
    async getAndSetConferenceAll() {
      const requestId = ++this.listRequestId
      this.LoadingCircleState = true
      const offset = (this.currentPage - 1) * this.itemsPerPage
      const sortBy = this.tableHeaderColumnNames[this.tableHeader.indexOf(this.sortColumn)] || 'id'
      const sortDesc = this.sortDirection === 'desc'
      const apiEndpoint =
        `/admin/conference/all?limit=${this.itemsPerPage}&offset=${offset}` +
        `&sort_by=${sortBy}&sort_desc=${sortDesc}`

      const payload = {
        output_filters: [
          'id',
          'name',
          'short_name',
          'year',
          'information',
          'venue',
          'city',
          'country',
          'proposal_start_date',
          'proposal_end_date',
          'start_date',
          'end_date',
          'is_lighthouse_challenge',
          'is_open_for_submissions',
          'chairperson_emails',
          'chairperson_names',
          'message_before_generate_proposal',
          'owner_id',
          'created_time',
          'modified_time',
        ],
        search_filters: this.activeSearchFilters || null,
      }

      try {
        const resp = await apiPost(apiEndpoint, payload)
        if (requestId !== this.listRequestId) return
        this.conferencesList = resp?.content || []
        this.totalItems = resp?.total_records || 0
        this.totalPages = resp?.total_pages || 0
        this.listLoaded = true
        if (this.totalPages > 0 && this.currentPage > this.totalPages) {
          this.currentPage = this.totalPages
          await this.getAndSetConferenceAll()
        }
      } catch (e) {
        if (requestId !== this.listRequestId) return
        if (e.message.includes('No Conference found') || e.message.includes('not found')) {
          this.conferencesList = []
          this.totalItems = 0
          this.totalPages = 0
          this.listLoaded = true
          useToastAlertStore().showAlert('No conferences found matching criteria', 'info', 3000)
        } else {
          useToastAlertStore().showAlert(e.message, 'danger', 6000)
        }
      } finally {
        if (requestId === this.listRequestId) this.LoadingCircleState = false
      }
    },
    async getConferenceById(id) {
      if (!Number.isInteger(id) || id < 1) {
        useToastAlertStore().showAlert('Invalid conference ID', 'danger', 6000)
        await this.$router.replace({ name: 'Admin Conferences' })
        return
      }
      const requestId = ++this.detailRequestId
      this.LoadingCircleState = true
      try {
        const resp = await apiGet(`/admin/conference/${id}`)
        if (requestId !== this.detailRequestId) return
        if (!resp) throw new Error('Conference not found')
        this.data = {
          data: resp,
          index: 0,
        }
        this.populateEditForm(resp)
        this.showCreatePanel = false
      } catch (e) {
        if (requestId !== this.detailRequestId) return
        useToastAlertStore().showAlert(e.message || e, 'danger', 6000)
        await this.$router.replace({ name: 'Admin Conferences' })
      } finally {
        if (requestId === this.detailRequestId) this.LoadingCircleState = false
      }
    },
    selectData(item) {
      this.data = {
        data: item,
        index: 0,
      }
      this.populateEditForm(item)
      this.showCreatePanel = false
      this.current_password = ''
      this.$router.push({ name: 'Admin Conference Overview', params: { id: item.id } })
    },
    buildDateFilter(operator, firstDate, secondDate, fieldName, filters) {
      if (!operator || !firstDate) return true
      const startOfFirstDay = new Date(`${firstDate}T00:00:00.000`)
      const endOfFirstDay = new Date(`${firstDate}T23:59:59.999`)
      if (Number.isNaN(startOfFirstDay.getTime())) return false
      if (operator === 'lt') {
        filters[`${fieldName}__lt`] = startOfFirstDay.toISOString()
      } else if (operator === 'gt') {
        filters[`${fieldName}__gt`] = endOfFirstDay.toISOString()
      } else if (operator === 'between') {
        if (!secondDate) {
          useToastAlertStore().showAlert('A To Date is required for date ranges', 'warning', 4000)
          return false
        }
        const endOfSecondDay = new Date(`${secondDate}T23:59:59.999`)
        if (Number.isNaN(endOfSecondDay.getTime()) || startOfFirstDay > endOfSecondDay) {
          useToastAlertStore().showAlert(
            'The From Date must not be after the To Date',
            'warning',
            4000
          )
          return false
        }
        filters[`${fieldName}__between`] = [
          startOfFirstDay.toISOString(),
          endOfSecondDay.toISOString(),
        ]
      }
      return true
    },
    buildSearchFilters() {
      const filters = {}
      if (this.searchFilters.id) filters.id = Number(this.searchFilters.id)
      const name = this.searchFilters.name.trim()
      const shortName = this.searchFilters.short_name.trim()
      const city = this.searchFilters.city.trim()
      const country = this.searchFilters.country.trim()
      if (name) filters.name__ilike = name
      if (shortName) {
        filters.short_name__ilike = shortName
      }
      if (this.searchFilters.owner_id) filters.owner_id = Number(this.searchFilters.owner_id)
      if (city) filters.city__ilike = city
      if (country) {
        filters.country__ilike = country
      }
      if (this.searchFilters.year_operator && this.searchFilters.year) {
        const firstYear = Number(this.searchFilters.year)
        if (this.searchFilters.year_operator === 'eq') {
          filters.year = firstYear
        } else if (this.searchFilters.year_operator === 'lt') {
          filters.year__lt = firstYear
        } else if (this.searchFilters.year_operator === 'gt') {
          filters.year__gt = firstYear
        } else if (this.searchFilters.year_operator === 'between') {
          const secondYear = Number(this.searchFilters.year2)
          if (!this.searchFilters.year2 || firstYear > secondYear) {
            useToastAlertStore().showAlert(
              'A valid To Year greater than or equal to From Year is required',
              'warning',
              4000
            )
            return undefined
          }
          filters.year__between = [firstYear, secondYear]
        }
      }
      if (this.searchFilters.is_open_for_submissions !== '') {
        filters.is_open_for_submissions = this.searchFilters.is_open_for_submissions === 'true'
      }
      if (this.searchFilters.is_lighthouse_challenge !== '') {
        filters.is_lighthouse_challenge = this.searchFilters.is_lighthouse_challenge === 'true'
      }
      const proposalStartValid = this.buildDateFilter(
        this.searchFilters.proposal_start_operator,
        this.searchFilters.proposal_start_date1,
        this.searchFilters.proposal_start_date2,
        'proposal_start_date',
        filters
      )
      const proposalEndValid = this.buildDateFilter(
        this.searchFilters.proposal_end_operator,
        this.searchFilters.proposal_end_date1,
        this.searchFilters.proposal_end_date2,
        'proposal_end_date',
        filters
      )
      if (!proposalStartValid || !proposalEndValid) return undefined
      return Object.keys(filters).length > 0 ? filters : null
    },
    async applySearch() {
      const filters = this.buildSearchFilters()
      if (filters === undefined) return
      this.activeSearchFilters = filters
      this.currentPage = 1
      this.clearSelection()
      await this.getAndSetConferenceAll()
      if (this.activeSearchFilters) {
        useToastAlertStore().showAlert('Search filters applied', 'success', 3000)
      } else {
        useToastAlertStore().showAlert('No filters to apply', 'info', 3000)
      }
    },
    async clearSearch() {
      this.searchFilters = {
        id: '',
        name: '',
        short_name: '',
        owner_id: '',
        year_operator: '',
        year: '',
        year2: '',
        city: '',
        country: '',
        is_open_for_submissions: '',
        is_lighthouse_challenge: '',
        proposal_start_operator: '',
        proposal_start_date1: '',
        proposal_start_date2: '',
        proposal_end_operator: '',
        proposal_end_date1: '',
        proposal_end_date2: '',
      }
      this.activeSearchFilters = null
      this.currentPage = 1
      this.clearSelection()
      await this.getAndSetConferenceAll()
      useToastAlertStore().showAlert('Search filters cleared', 'success', 3000)
    },
    async changePage(page) {
      if (page >= 1 && page <= this.totalPages && page !== this.currentPage) {
        this.currentPage = page
        this.clearSelection()
        await this.getAndSetConferenceAll()
      }
    },
    async changeItemsPerPage(option) {
      this.itemsPerPage = option
      this.currentPage = 1
      this.clearSelection()
      await this.getAndSetConferenceAll()
    },
    async sortTable(column) {
      if (this.sortColumn === column) {
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc'
      } else {
        this.sortDirection = 'asc'
      }
      this.sortColumn = column
      this.clearSelection()
      await this.getAndSetConferenceAll()
    },
    selectAllRows() {
      if (this.selectAll) {
        this.selectedRows = this.list.map((item) => item.id)
      } else {
        this.selectedRows = []
      }
    },
    async createConference() {
      if (this.createPending) return
      if (!this.validateConferenceForm(this.createForm)) return
      const payload = this.buildConferencePayload(this.createForm)
      this.createPending = true
      try {
        const resp = await apiPost('/admin/conference/create', payload)
        useToastAlertStore().showAlert('Conference created', 'success')
        this.createForm = createEmptyConferenceForm()
        this.showCreatePanel = false
        this.currentPage = 1
        this.clearSelection()
        await this.getAndSetConferenceAll()
        if (resp?.id) this.selectData(resp)
      } catch (e) {
        useToastAlertStore().showAlert(e.message || e, 'danger', 6000)
      } finally {
        this.createPending = false
      }
    },
    async updateConference() {
      if (this.updatePending) return
      if (!this.dataSelected?.id) return
      if (!this.validateConferenceForm(this.editForm)) return
      const payload = this.buildConferencePayload(this.editForm)
      this.updatePending = true
      try {
        const resp = await apiPut(`/admin/conference/${this.dataSelected.id}/update`, payload)
        useToastAlertStore().showAlert('Conference updated', 'success')
        this.data = {
          data: resp.data,
          index: 0,
        }
        this.populateEditForm(resp.data)
        await this.getAndSetConferenceAll()
      } catch (e) {
        useToastAlertStore().showAlert(e.message || e, 'danger', 6000)
      } finally {
        this.updatePending = false
      }
    },
    async deleteConference(id) {
      if (this.deletePending) return
      const ok = await this.$refs.confirmDialogue.show({
        title: 'Delete conference',
        message: 'Are you sure you want to delete this conference? It cannot be undone.',
        okButton: 'Delete forever',
        okButtonTheme: 'btn-danger',
      })
      if (!ok) {
        this.current_password = ''
        return
      }

      this.deletePending = true
      try {
        await apiDelete(
          `/admin/conference/${id}/delete?active_user_password=${encodeURIComponent(
            this.current_password
          )}`
        )
        useToastAlertStore().showAlert('Conference deleted', 'success')
        this.current_password = ''
        await this.closePanels()
        await this.getAndSetConferenceAll()
      } catch (e) {
        useToastAlertStore().showAlert(e.message || e, 'danger', 6000)
      } finally {
        this.deletePending = false
      }
    },
    openBulkUpdateModal() {
      this.showBulkUpdatePanel = true
      this.bulkUpdate = {
        open_for_submissions: '',
        is_lighthouse_challenge: '',
      }
    },
    closeBulkUpdateModal() {
      if (this.bulkUpdatePending) return
      this.showBulkUpdatePanel = false
    },
    openBulkDeleteModal() {
      this.showBulkDeletePanel = true
      this.bulkCurrentPassword = ''
    },
    closeBulkDeleteModal() {
      if (this.bulkDeletePending) return
      this.showBulkDeletePanel = false
      this.bulkCurrentPassword = ''
    },
    bulkResultSummary(result, operation) {
      const successful = Array.isArray(result?.successful) ? result.successful : []
      const failed = Array.isArray(result?.failed) ? result.failed : []
      const failedIds = failed
        .map((item) => item?.id ?? item?.data?.id)
        .filter((id) => id !== undefined)
      if (failed.length > 0) {
        const failedLabel = failedIds.length > 0 ? ` Failed IDs: ${failedIds.join(', ')}.` : ''
        useToastAlertStore().showAlert(
          `${operation}: ${successful.length} succeeded, ${failed.length} failed.${failedLabel}`,
          successful.length > 0 ? 'warning' : 'danger',
          7000
        )
      } else {
        useToastAlertStore().showAlert(
          `${operation}: ${successful.length} conference(s) succeeded`,
          'success'
        )
      }
      return { successfulCount: successful.length, failedIds }
    },
    async bulkUpdateConferences() {
      if (this.bulkUpdatePending) return
      if (this.selectedRows.length === 0) return
      if (
        this.bulkUpdate.open_for_submissions === '' &&
        this.bulkUpdate.is_lighthouse_challenge === ''
      ) {
        useToastAlertStore().showAlert('Select at least one bulk update action', 'warning', 4000)
        return
      }

      const updates = this.selectedRows.map((id) => {
        const update = { id }
        if (this.bulkUpdate.open_for_submissions !== '') {
          update.is_open_for_submissions = this.bulkUpdate.open_for_submissions === 'true'
        }
        if (this.bulkUpdate.is_lighthouse_challenge !== '') {
          update.is_lighthouse_challenge = this.bulkUpdate.is_lighthouse_challenge === 'true'
        }
        return update
      })

      this.bulkUpdatePending = true
      try {
        const resp = await apiPut('/admin/conference/bulk-update', updates)
        const summary = this.bulkResultSummary(resp.data, 'Bulk update')
        this.selectedRows = summary.failedIds
        this.selectAll = false
        this.showBulkUpdatePanel = summary.failedIds.length > 0
        if (summary.successfulCount > 0) await this.getAndSetConferenceAll()
      } catch (e) {
        useToastAlertStore().showAlert(e.message || e, 'danger', 6000)
      } finally {
        this.bulkUpdatePending = false
      }
    },
    async bulkDeleteConferences() {
      if (this.bulkDeletePending) return
      if (this.selectedRows.length === 0) return
      if (!this.bulkCurrentPassword) {
        useToastAlertStore().showAlert('Password required', 'warning', 4000)
        return
      }

      this.bulkDeletePending = true
      try {
        const result = await apiDelete('/admin/conference/bulk-delete', {
          params: { active_user_password: this.bulkCurrentPassword },
          data: this.selectedRows,
        })
        const summary = this.bulkResultSummary(result, 'Bulk delete')
        this.selectedRows = summary.failedIds
        this.selectAll = false
        this.showBulkDeletePanel = summary.failedIds.length > 0
        this.bulkCurrentPassword = ''
        if (summary.successfulCount > 0) await this.getAndSetConferenceAll()
      } catch (e) {
        useToastAlertStore().showAlert(e.message || e, 'danger', 6000)
      } finally {
        this.bulkDeletePending = false
      }
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
      const needle = this.searchString.toLowerCase().trim()
      return needle === ''
        ? this.conferencesList
        : this.conferencesList.filter(
            (item) =>
              item.id?.toString() === needle ||
              item.year?.toString().includes(needle) ||
              item.name?.toLowerCase().includes(needle) ||
              item.short_name?.toLowerCase().includes(needle) ||
              item.city?.toLowerCase().includes(needle) ||
              item.country?.toLowerCase().includes(needle)
          )
    },
    visiblePages() {
      if (this.totalPages <= 0) return []
      const windowSize = 7
      let start = Math.max(1, this.currentPage - Math.floor(windowSize / 2))
      const end = Math.min(this.totalPages, start + windowSize - 1)
      start = Math.max(1, end - windowSize + 1)
      return Array.from({ length: end - start + 1 }, (_, index) => start + index)
    },
    hasActiveFilters() {
      return this.activeSearchFilters !== null
    },
  },
  watch: {
    searchString() {
      this.clearSelection()
    },
    selectedRows() {
      const visibleIds = this.list.map((item) => item.id)
      this.selectAll =
        visibleIds.length > 0 && visibleIds.every((id) => this.selectedRows.includes(id))
    },
    async $route(val) {
      if (val.name === 'Admin Conferences') {
        this.data = {}
        this.showCreatePanel = false
        if (!this.listLoaded) await this.getAndSetConferenceAll()
      } else if (val.name === 'Admin Conference Overview') {
        const id = Number(val.params.id)
        if (this.dataSelected?.id !== id) await this.getConferenceById(id)
      }
    },
  },
}
</script>

<style scoped>
input[type='checkbox'] {
  transform: scale(1.2);
}

.cursor-pointer {
  cursor: pointer;
}

.cursor-pointer:hover {
  background-color: #f8f9fa;
}

.admin-list-shell {
  width: fit-content;
  max-width: 100%;
}

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

.modal-header.bg-info,
.modal-header.bg-danger {
  border-bottom: none;
}

.modal-header .btn-close-white {
  filter: brightness(0) invert(1);
}
</style>
