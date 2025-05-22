<template>
  <div class="mb-3 d-flex flex-column">
    <form class="d-block order-last" @submit.prevent="submitEvent" :id="formID">
      <slot></slot>
      <div class="alert alert-info opacity-75 lh-sm" v-if="errorMessage">
        {{ errorMessage }}
      </div>
      <button v-if="showActionBtn" type="submit" class="btn btn-primary mt-4" :class="classListBtn">
        {{ actionBtn }}
      </button>
    </form>
    <div v-if="missingInputsList.length > 0" :class="classList">
      <div v-for="(item, index) in missingInputsList" :key="index" class="py-3">
        <div class="alert alert-danger" role="alert">
          {{ item.label }} - {{ item.message }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VueForm',
  data() {
    return {
      missingInputsList: [],
    }
  },
  props: {
    actionBtn: {
      typ: String,
      default: 'Submit',
    },
    name: {
      typ: String,
      required: true,
    },
    actionBtnFullwidth: {
      typ: Boolean,
      default: true,
    },
    errorMessage: {
      typ: String,
    },
    showActionBtn: {
      typ: Boolean,
      default: true,
    },
    showMissingInputTop: {
      typ: Boolean,
      default: false,
    },
  },
  computed: {
    classList() {
      return {
        'order-first': this.showMissingInputTop,
      }
    },
    classListBtn() {
      return {
        'w-100': this.actionBtnFullwidth,
      }
    },
    formID() {
      return `${this.name}_formId`
    },
  },
  emits: ['submitEvent'],
  methods: {
    validateForm() {
      const requiredInputs = [
        ...document.getElementById(this.formID).querySelectorAll('[required]'),
      ]
      const missingInputs = Object.values(requiredInputs).filter((el) => {
        return el.getAttribute('errormessage') !== ''
      })
      this.missingInputsList = missingInputs.map((x) => {
        return {
          ...x,
          label: x.getAttribute('label'),
          message: x.getAttribute('errormessage'),
        }
      })
      return missingInputs.length === 0
    },
    submitEvent() {
      if (this.validateForm()) {
        //if no required inputs are missing, the form will emit a trigger to the parent component
        this.$emit('submitEvent')
      }
    },
  },
}
</script>

<style scoped></style>
