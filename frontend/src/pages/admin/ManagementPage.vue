<template>
  <div class="admin-management-page">
    <div class="pb-3">
      <collapse-section name="info">
        <VueTextSection>
          <template #text>
            <p>
              This view provides administrative tools for database backups and the Redis data store.
              Destructive operations require confirmation and, where required by the API, your
              current password.
            </p>
            <p class="mb-0">
              Redis values may contain application state. Only change or delete them when you know
              which feature owns the key.
            </p>
          </template>
        </VueTextSection>
      </collapse-section>
    </div>

    <div class="row g-4">
      <div class="col-12">
        <section class="card h-100 shadow-sm">
          <div class="card-header bg-body-tertiary">
            <h4 class="mb-0"><i class="bi bi-database me-2"></i>Database backups</h4>
          </div>
          <div class="card-body d-flex flex-column gap-4">
            <div>
              <h5>Create and download backup</h5>
              <p class="text-muted">
                Creates a SQLite backup on the server and downloads a copy to this device.
              </p>
              <label
                class="form-label"
                for="backup-file-name"
                >File name (optional)</label
              >
              <div class="input-group">
                <input
                  id="backup-file-name"
                  v-model.trim="backupFileName"
                  class="form-control"
                  maxlength="200"
                  placeholder="database-backup"
                  @keyup.enter="downloadDatabaseBackup" />
                <button
                  class="btn btn-primary"
                  type="button"
                  :disabled="pending.backup"
                  @click="downloadDatabaseBackup">
                  <span
                    v-if="pending.backup"
                    class="spinner-border spinner-border-sm me-1"
                    aria-hidden="true"></span>
                  <i
                    v-else
                    class="bi bi-download me-1"></i>
                  Create backup
                </button>
              </div>
              <div class="form-text">The .sqlite3 extension is added when omitted.</div>
            </div>

            <hr class="my-0" />

            <div>
              <h5>Delete old backups</h5>
              <p class="text-muted">
                Remove stored backup files from the server. Keeping the latest backup is the safer
                cleanup option.
              </p>
              <label
                class="form-label"
                for="backup-password"
                >Current password</label
              >
              <input
                id="backup-password"
                v-model="backupPassword"
                type="password"
                class="form-control mb-3"
                autocomplete="current-password"
                placeholder="Required for backup deletion" />
              <div class="d-flex flex-wrap gap-2">
                <button
                  class="btn btn-warning"
                  type="button"
                  :disabled="pending.deleteBackups"
                  @click="deleteDatabaseBackups(false)">
                  Keep latest backup
                </button>
                <button
                  class="btn btn-danger"
                  type="button"
                  :disabled="pending.deleteBackups"
                  @click="deleteDatabaseBackups(true)">
                  Delete all backups
                </button>
              </div>
              <div
                v-if="lastDeletedBackups !== null"
                class="alert alert-secondary mt-3 mb-0 py-2">
                Deleted {{ lastDeletedBackups }} backup file(s).
              </div>
            </div>
          </div>
        </section>
      </div>

      <div class="col-12">
        <section class="card h-100 shadow-sm">
          <div class="card-header bg-body-tertiary d-flex flex-wrap align-items-center gap-2">
            <h4 class="mb-0 me-auto"><i class="bi bi-hdd-network me-2"></i>Redis management</h4>
            <span
              v-if="redisHealth"
              class="badge"
              :class="redisHealth === 'healthy' ? 'text-bg-success' : 'text-bg-danger'">
              {{ redisHealth === 'healthy' ? 'Available' : 'Unavailable' }}
            </span>
            <button
              class="btn btn-sm btn-outline-primary"
              type="button"
              :disabled="pending.health"
              @click="checkRedisHealth">
              <span
                v-if="pending.health"
                class="spinner-border spinner-border-sm me-1"
                aria-hidden="true"></span>
              Check health
            </button>
          </div>
          <div class="card-body">
            <form
              class="mb-4"
              @submit.prevent="getRedisValue">
              <h5>Find a key</h5>
              <div class="input-group">
                <input
                  v-model.trim="lookupKey"
                  class="form-control"
                  required
                  placeholder="Redis key" />
                <button
                  class="btn btn-outline-primary"
                  type="submit"
                  :disabled="pending.lookup || !lookupKey">
                  Find
                </button>
              </div>
              <div
                v-if="lookupResult"
                class="border rounded p-3 mt-3 redis-value">
                <div class="fw-semibold text-break">{{ lookupResult.key }}</div>
                <pre class="mb-0 mt-2 text-break">{{ lookupResult.value }}</pre>
              </div>
            </form>

            <form
              class="mb-4"
              @submit.prevent="setRedisValue">
              <h5>Set a key/value pair</h5>
              <div class="mb-2">
                <label
                  class="form-label"
                  for="redis-key"
                  >Key</label
                >
                <input
                  id="redis-key"
                  v-model.trim="redisForm.key"
                  class="form-control"
                  required />
              </div>
              <div class="mb-3">
                <label
                  class="form-label"
                  for="redis-value"
                  >Value</label
                >
                <textarea
                  id="redis-value"
                  v-model="redisForm.value"
                  class="form-control font-monospace"
                  rows="3"
                  required></textarea>
              </div>
              <button
                class="btn btn-primary"
                type="submit"
                :disabled="pending.setValue || !redisForm.key || redisForm.value === ''">
                Save value
              </button>
            </form>

            <div class="border-top pt-4">
              <div class="d-flex flex-wrap align-items-center gap-2 mb-3">
                <h5 class="mb-0 me-auto">All Redis values</h5>
                <button
                  class="btn btn-sm btn-outline-primary"
                  type="button"
                  :disabled="pending.allKeys"
                  @click="getAllRedisValues">
                  <i class="bi bi-arrow-clockwise me-1"></i>Refresh
                </button>
              </div>

              <LoadingCircle :activated="pending.allKeys" />
              <div
                v-if="redisValues.length > 0 && !pending.allKeys"
                class="table-responsive redis-table">
                <table class="table table-sm table-hover align-middle mb-0">
                  <thead class="table-light sticky-top">
                    <tr>
                      <th scope="col">Key</th>
                      <th scope="col">Value</th>
                      <th
                        scope="col"
                        class="text-end">
                        Action
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="item in redisValues"
                      :key="item.key">
                      <td class="text-break fw-semibold">{{ item.key }}</td>
                      <td>
                        <pre class="mb-0 text-break value-cell">{{ item.value }}</pre>
                      </td>
                      <td class="text-end">
                        <button
                          class="btn btn-sm btn-outline-danger"
                          type="button"
                          :disabled="pending.deleteKey === item.key"
                          :aria-label="`Delete Redis key ${item.key}`"
                          @click="deleteRedisKey(item.key)">
                          <i class="bi bi-trash"></i>
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <p
                v-else-if="redisLoaded && !pending.allKeys"
                class="text-muted mb-0">
                Redis contains no keys.
              </p>

              <div class="danger-zone border border-danger rounded p-3 mt-4">
                <h5 class="text-danger">Delete all Redis keys</h5>
                <p class="small mb-2">This cannot be undone and requires your current password.</p>
                <div class="input-group">
                  <input
                    v-model="redisDeletePassword"
                    type="password"
                    class="form-control"
                    autocomplete="current-password"
                    placeholder="Current password" />
                  <button
                    class="btn btn-danger"
                    type="button"
                    :disabled="pending.deleteAllKeys"
                    @click="deleteAllRedisKeys">
                    Delete all keys
                  </button>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>

    <confirm-dialogue ref="confirmDialogue" />
  </div>
</template>

<script>
import api from '@/api/axios'
import { apiDelete, apiGet, apiPost } from '@/api/api'
import CollapseSection from '@/components/CollapseSection.vue'
import ConfirmDialogue from '@/components/ConfirmDialogue.vue'
import LoadingCircle from '@/components/LoadingCircle.vue'
import VueTextSection from '@/components/VueTextSection.vue'
import { useToastAlertStore } from '@/stores/toastAlert'

function errorMessage(error) {
  const detail = error?.response?.data?.detail
  if (typeof detail === 'string') return detail
  return error?.message || 'Request failed'
}

function downloadName(response, requestedName) {
  const disposition = response.headers?.['content-disposition'] || ''
  const encodedMatch = disposition.match(/filename\*=UTF-8''([^;]+)/i)
  const plainMatch = disposition.match(/filename="?([^";]+)"?/i)
  if (encodedMatch) return decodeURIComponent(encodedMatch[1])
  if (plainMatch) return plainMatch[1]
  if (requestedName)
    return requestedName.endsWith('.sqlite3') ? requestedName : `${requestedName}.sqlite3`
  return 'database-backup.sqlite3'
}

export default {
  name: 'ManagementPage',
  components: {
    CollapseSection,
    ConfirmDialogue,
    LoadingCircle,
    VueTextSection,
  },
  data() {
    return {
      backupFileName: '',
      backupPassword: '',
      lastDeletedBackups: null,
      redisHealth: '',
      lookupKey: '',
      lookupResult: null,
      redisForm: { key: '', value: '' },
      redisValues: [],
      redisLoaded: false,
      redisDeletePassword: '',
      pending: {
        backup: false,
        deleteBackups: false,
        health: false,
        lookup: false,
        setValue: false,
        allKeys: false,
        deleteKey: '',
        deleteAllKeys: false,
      },
    }
  },
  async mounted() {
    await Promise.allSettled([this.checkRedisHealth(false), this.getAllRedisValues(false)])
  },
  methods: {
    showError(error) {
      useToastAlertStore().showAlert(errorMessage(error), 'danger', 6000)
    },
    async downloadDatabaseBackup() {
      if (this.pending.backup) return
      this.pending.backup = true
      try {
        const params = this.backupFileName ? { file_name: this.backupFileName } : {}
        const response = await api.post('/admin/database/database_backup_and_download', null, {
          params,
          responseType: 'blob',
        })
        const url = URL.createObjectURL(response.data)
        const link = document.createElement('a')
        link.href = url
        link.download = downloadName(response, this.backupFileName)
        document.body.appendChild(link)
        link.click()
        link.remove()
        URL.revokeObjectURL(url)
        useToastAlertStore().showAlert('Database backup created and downloaded', 'success')
      } catch (error) {
        this.showError(error)
      } finally {
        this.pending.backup = false
      }
    },
    async deleteDatabaseBackups(deleteAll) {
      if (this.pending.deleteBackups) return
      if (!this.backupPassword) {
        useToastAlertStore().showAlert('Current password is required', 'warning', 4000)
        return
      }
      const confirmed = await this.$refs.confirmDialogue.show({
        title: deleteAll ? 'Delete all database backups' : 'Delete old database backups',
        message: deleteAll
          ? 'Delete every database backup stored on the server? This cannot be undone.'
          : 'Delete all database backups except the latest one?',
        okButton: deleteAll ? 'Delete all backups' : 'Delete old backups',
        okButtonTheme: deleteAll ? 'btn-danger' : 'btn-warning',
      })
      if (!confirmed) return

      this.pending.deleteBackups = true
      try {
        const result = await apiDelete('/admin/database/delete_database_backups', {
          params: {
            active_user_password: this.backupPassword,
            delete_all_backups: deleteAll,
          },
        })
        this.lastDeletedBackups = Array.isArray(result?.deleted_files)
          ? result.deleted_files.length
          : 0
        this.backupPassword = ''
        useToastAlertStore().showAlert(result?.message || 'Database backups deleted', 'success')
      } catch (error) {
        this.showError(error)
      } finally {
        this.pending.deleteBackups = false
      }
    },
    async checkRedisHealth(showSuccess = true) {
      if (this.pending.health) return
      this.pending.health = true
      try {
        const result = await apiGet('/admin/redis/health')
        this.redisHealth = 'healthy'
        if (showSuccess) {
          useToastAlertStore().showAlert(result?.message || 'Redis server is available', 'success')
        }
      } catch (error) {
        this.redisHealth = 'unhealthy'
        if (showSuccess) this.showError(error)
      } finally {
        this.pending.health = false
      }
    },
    async getRedisValue() {
      if (!this.lookupKey || this.pending.lookup) return
      this.pending.lookup = true
      this.lookupResult = null
      try {
        this.lookupResult = await apiGet(`/admin/redis/?key=${encodeURIComponent(this.lookupKey)}`)
      } catch (error) {
        this.showError(error)
      } finally {
        this.pending.lookup = false
      }
    },
    async getAllRedisValues(showErrors = true) {
      if (this.pending.allKeys) return
      this.pending.allKeys = true
      try {
        const result = await apiGet('/admin/redis/all_keys')
        this.redisValues = Array.isArray(result) ? result : []
        this.redisLoaded = true
      } catch (error) {
        this.redisValues = []
        this.redisLoaded = true
        if (errorMessage(error).toLowerCase().includes('no data found')) return
        if (showErrors) this.showError(error)
      } finally {
        this.pending.allKeys = false
      }
    },
    async setRedisValue() {
      if (!this.redisForm.key || this.redisForm.value === '' || this.pending.setValue) return
      this.pending.setValue = true
      try {
        const result = await apiPost('/admin/redis/', {
          key: this.redisForm.key,
          value: this.redisForm.value,
        })
        useToastAlertStore().showAlert(result?.message || 'Redis value saved', 'success')
        this.lookupKey = this.redisForm.key
        this.lookupResult = { ...this.redisForm }
        this.redisForm = { key: '', value: '' }
        await this.getAllRedisValues()
      } catch (error) {
        this.showError(error)
      } finally {
        this.pending.setValue = false
      }
    },
    async deleteRedisKey(key) {
      if (this.pending.deleteKey) return
      const confirmed = await this.$refs.confirmDialogue.show({
        title: 'Delete Redis key',
        message: `Delete the Redis key “${key}”? This cannot be undone.`,
        okButton: 'Delete key',
        okButtonTheme: 'btn-danger',
      })
      if (!confirmed) return

      this.pending.deleteKey = key
      try {
        const result = await apiDelete(`/admin/redis/?key=${encodeURIComponent(key)}`)
        useToastAlertStore().showAlert(result?.message || 'Redis key deleted', 'success')
        if (this.lookupResult?.key === key) this.lookupResult = null
        await this.getAllRedisValues()
      } catch (error) {
        this.showError(error)
      } finally {
        this.pending.deleteKey = ''
      }
    },
    async deleteAllRedisKeys() {
      if (this.pending.deleteAllKeys) return
      if (!this.redisDeletePassword) {
        useToastAlertStore().showAlert('Current password is required', 'warning', 4000)
        return
      }
      const confirmed = await this.$refs.confirmDialogue.show({
        title: 'Delete all Redis keys',
        message: 'Delete every key and value from Redis? This cannot be undone.',
        okButton: 'Delete all keys',
        okButtonTheme: 'btn-danger',
      })
      if (!confirmed) return

      this.pending.deleteAllKeys = true
      try {
        const result = await apiDelete('/admin/redis/delete_all_keys', {
          params: { active_user_password: this.redisDeletePassword },
        })
        this.redisDeletePassword = ''
        this.redisValues = []
        this.redisLoaded = true
        this.lookupResult = null
        useToastAlertStore().showAlert(result?.message || 'All Redis keys deleted', 'success')
      } catch (error) {
        this.showError(error)
      } finally {
        this.pending.deleteAllKeys = false
      }
    },
  },
}
</script>

<style scoped>
.admin-management-page .card {
  border-color: #dee2e6;
}

.redis-value pre,
.value-cell {
  white-space: pre-wrap;
  word-break: break-word;
  font-size: 0.85rem;
}

.redis-table {
  max-height: 28rem;
}

.redis-table .value-cell {
  min-width: 12rem;
  max-width: 28rem;
}

.danger-zone {
  background: rgba(var(--bs-danger-rgb), 0.04);
}
</style>
