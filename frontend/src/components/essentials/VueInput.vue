<template>
  <div>
    <!--    Text-Inputs  -->
    <div v-if="!isCheckbox && !isCheckboxPlus && !isSelectPlus && !isSelectWithOther && !isSelectMultipleWithOther"
      class="mt-3">
      <div class="mb-1">
        <span v-if="label" v-html="label" class="form-label label"></span>
        <!-- <span v-if="required" class="text-danger"><b>*</b></span> -->
      </div>
      <div>
        <div class="input-group" v-if="type === 'select'">
          <span class="input-group-text" v-if="icon !== ''">
            <i class="bi" :class="`bi-${icon}`"></i>
          </span>
          <select :errormessage="message" @input="$emit('update:modelValue', $event.target.value)" :value="modelValue"
            class="form-select" :class="{ 'border-danger': modelValue == null }">
            <option v-for="(item, idx) in options" :key="idx">
              {{ item }}
            </option>
          </select>
        </div>
        <div v-else class="input-group">
          <span class="input-group-text" v-if="icon !== ''">
            <i class="bi" :class="`bi-${icon}`"></i>
          </span>
          <component :is="inputComponentTyp" :errormessage="message" :disabled="disabled" :label="label"
            :type="textInputType" class="form-control" :minlength="textMinLength" :maxlength="textMaxLength"
            :class="{ 'border-danger': showError || (required && (!modelValue || !modelValue.length)) }"
            :value="modelValue" :placeholder="placeholder" @input="$emit('update:modelValue', $event.target.value)"
            :required="required" :allowSpecialCharacters="allowSpecialCharacters" />
          <button v-if="passwordInput" @click="toggleShow" class="btn btn-outline-secondary" type="button">
            <i class="bi" :class="{ 'bi-eye-slash': showPassword, 'bi-eye': !showPassword }"></i>
          </button>
        </div>
      </div>

      <!-- <div v-if="forgetPassword" class="text-end">
        <router-link :to="{ name: 'Reset password request' }">Reset password</router-link>
      </div> -->
      <div v-if="showError" class="text-start input-invalid mb-3">
        <div v-if="typeof message === 'string'">
          {{ message }}
        </div>
        <ul v-else-if="Array.isArray(message)">
          <li v-for="(item, index) in message" :key="index">{{ item }}</li>
        </ul>
      </div>
    </div>
    <div v-if="isPasswordRepeat" class="mb-3">
      <div id="passwordHelpBlock" class="form-text pb-2">
        <small>Your password must be 8-20 characters long. It must include upper and lower case letters, numbers, and
          special
          characters such as !,#.</small>
      </div>
      <label class="form-label">Confirm password</label>
      <div class="input-group">
        <span class="input-group-text" v-if="icon !== ''">
          <i class="bi" :class="`bi-${icon}`"></i>
        </span>
        <!-- <input :errormessage="passwordDontMatch" :label="'Confirm password'" onpaste="return false;"
          ondrop="return false;" autocomplete="off" :type="textInputType" class="form-control"
          :class="{ 'border-danger': passwordDontMatch }" v-model="passwordRepeat" :required="modelValue !== ''" /> -->

        <input :errormessage="passwordDontMatch" :label="'Confirm password'" autocomplete="off" :type="textInputType"
          class="form-control" :class="{ 'border-danger': passwordsDontMatch || hasValidationErrors }"
          v-model="passwordRepeat" :required="modelValue !== ''" /><button v-if="passwordInput" @click="toggleShow"
          class="btn btn-outline-secondary" type="button">
          <i class="bi" :class="{ 'bi-eye-slash': showPassword, 'bi-eye': !showPassword }"></i>
        </button>
      </div>
      <!-- <div v-if="hasValidationErrors" class="text-danger mt-2">
        <div v-if="typeof message === 'string' && message">
          {{ message }}
        </div>
        <ul v-else-if="Array.isArray(message) && message.length" class="mb-0 ps-3">
          <li v-for="(error, index) in message" :key="index">{{ error }}</li>
        </ul>
      </div> -->
      <div v-if="passwordsDontMatch" class="text-danger mt-2">
        <small>{{ passwordDontMatch }}</small>
      </div>
    </div>
    <div class="form-check d-flex align-items-center gap-2 mt-4" style="flex-grow: 1; flex-shrink: 1" v-if="isCheckbox">
      <input :checked="modelValue" :errormessage="message" type="checkbox" class="form-check-input"
        :class="{ 'border-danger': showError || (required && (required && (!modelValue))) }"
        @input="$emit('update:modelValue', $event.target.checked)" :required="required" :id="label + 'id'" />
      <label style="flex-shrink: 100" class="form-check-label"
        :class="{ 'text-danger': showError || (required && (required && (!modelValue))) }" v-html="label"
        :for="label + 'id'">

      </label>
      <!-- <span v-if="required" class="text-danger"><b>*</b></span> -->
    </div>
    <!-- Add radio group here -->
    <div class="gap-2" v-if="isCheckboxPlus">
      <div v-for="(item, idx) in options" :key="idx" class="p-1 gap-2 pe-3 align-items-center"
        style="display: inline-flex">
        <input :checked="setCheckboxPlusVModal(item)" :errormessage="message" type="checkbox" class="form-check-input"
          :class="{ 'border-danger': showError }" @input="buildCheckboxPlusVModal({ key: 'checkbox', value: item })"
          :required="required" :id="item + uniqueId + 'option'" />
        <label class="form-check-label" :for="item + uniqueId + 'option'">
          {{ item }}
        </label>
      </div>
      <input v-model="inputPlus" :errormessage="message" :disabled="disabled" :label="label" type="text"
        class="form-control" :minlength="textMinLength" :maxlength="textMaxLength" placeholder="Please specify"
        :class="{ 'border-danger': showError || (required && (!modelValue || !modelValue.length)) }"
        :required="required" :allowSpecialCharacters="allowSpecialCharacters" />
      <div v-if="showError" class="text-start input-invalid mb-3">
        {{ message }}
      </div>
    </div>

    <div class="gap-2" v-if="isSelectWithOther">

      <span class="input-group-text" v-if="icon !== ''">
        <i class="bi" :class="`bi-${icon}`"></i>
      </span>
      <select v-model="selectedOption" class="form-select mb-2" :class="{ 'border-danger': selectedOption == null }">
        <option v-for="(item, idx) in options" :key="idx">
          {{ item }}
        </option>
        <option value="Other">Other</option>
      </select>

      <!-- Conditionally show input field when "Other" is selected -->
      <input v-if="selectedOption === 'Other'" type="text" class="form-control" v-model="customInput"
        placeholder="Enter custom value" />
    </div>
    <div class="gap-2" v-if="isSelectMultipleWithOther">
      <span class="input-group-text" v-if="icon !== ''">
        <i class="bi" :class="`bi-${icon}`"></i>
      </span>
      <i class="ms-1 small">(You can select multiple values and/or add a custom input)</i>
      <multiselect v-model="selectedOptions" :multiple="true" :taggable="true" :close-on-select="true"
        :spellcheck="true" :allow-empty="true" :options="options"
        tag-placeholder="Press ENTER to add this as custom input"
        placeholder="Select option(s) or start typing to add a custom input..."
        :class="{ 'border-danger': hasSelectedOptionsError }" @tag="addCustomInput">

      </multiselect>
      <div class="text-danger mt-1 ms-1 small" v-if="hasSelectedOptionsError">
        Please select at least one option.
      </div>

      <!-- <input v-if="showCustomInput" type="text" class="form-control mt-2" v-model="customInput"
        placeholder="Enter custom value" /> -->
    </div>
  </div>
</template>

<script>
import Multiselect from 'vue-multiselect'

export default {
  name: 'VueInput',
  components: { Multiselect },
  props: {
    uniqueId: {
      typ: String,
    },
    questionKey: {
      typ: String,
    },
    disabled: {
      typ: Boolean,
      default: false,
    },
    modelValue: {
      typ: [String, Date, Array],
    },
    hasError: {
      typ: Boolean,
      default: false,
    },
    label: {
      typ: String,
    },
    text: {
      typ: String,
    },
    options: {
      typ: Array,
      default: () => [],
    },
    values: {
      typ: Array,
      default: () => [],
    },
    icon: {
      typ: String,
      default: '',
    },
    placeholder: {
      typ: String,
      default: '',
    },
    type: {
      typ: String,
      default: 'text',
      validator(value) {
        return [
          '',
          'date',
          'textarea',
          'select',
          'selectPlus',
          'selectWithOther',
          'selectMultipleWithOther',
          'text',
          'password',
          'email',
          'password-repeat',
          'text-field',
          'checkbox',
          'checkboxPlus',
        ].includes(value)
      },
    },
    textMinLength: {
      typ: Number,
    },
    textMaxLength: {
      typ: Number,
    },
    required: {
      typ: Boolean,
    },
    allowSpecialCharacters: {
      typ: Boolean,
      default: true,
    },
    showForgetPassword: {
      typ: Boolean,
      default: true,
    },
  },
  emits: ['update:modelValue', 'errorState'],
  data() {
    return {
      message: '',
      passwordRepeat: '',
      showPassword: false,
      inputPlus: '',
      selectedOption: this.modelValue || null,
      selectedOptions: [],
      customInput: '',
    }
  },
  computed: {
    inputComponentTyp() {
      return this.type === 'textarea' ? 'textarea' : 'input'
    },
    hasValidationErrors() {
      return Array.isArray(this.message) ? this.message.length > 0 : Boolean(this.message);
    },
    showError() {
      return this.hasValidationErrors || this.hasError || this.passwordsDontMatch
    },
    forgetPassword() {
      return this.type === 'password' && this.showForgetPassword
    },
    isCheckbox() {
      return this.type === 'checkbox'
    },
    isCheckboxPlus() {
      return this.type === 'checkboxPlus'
    },
    isSelectPlus() {
      return this.type === 'selectPlus'
    },
    isSelectWithOther() {
      return this.type === 'selectWithOther'
    },
    isSelectMultipleWithOther() {
      return this.type === 'selectMultipleWithOther'
    },
    isPasswordRepeat() {
      return this.type === 'password-repeat'
    },
    passwordsDontMatch() {
      return this.isPasswordRepeat &&
        this.modelValue &&
        this.passwordRepeat &&
        this.modelValue !== this.passwordRepeat;
    },

    passwordDontMatch() {
      return this.passwordsDontMatch ? 'Passwords do not match.' : '';
    },
    passwordInput() {
      return ['password', 'password-repeat'].includes(this.type)
    },
    textInputType() {
      return this.type === 'date'
        ? 'date'
        : this.type === 'text'
          ? 'text'
          : this.type === 'email'
            ? 'email'
            : this.showPassword === true
              ? 'text'
              : 'password'
    },

    hasSelectedOptionsError() {
      return !this.selectedOptions || this.selectedOptions.length === 0;
    },
    showCustomInput() {
      return this.selectedOptions && this.selectedOptions.some(option => option.label === 'Other');
    },
    formattedOptions() {
      return [...this.options, 'Other'];
    }
  },
  watch: {
    hasError(n) {
      if (!n) {
        this.resetInputState()
      }
    },
    passwordRepeat(newValue) {
      if (this.isPasswordRepeat && this.modelValue) {
        this.validatePassword(this.modelValue);
      }

    },
    modelValue: {
      handler: function (value) {
        if (value) {
          this.checkForFormValidation(value)
        } else {
          this.resetInputState()
        }
        if (this.type === 'password-repeat') {
          this.validatePassword(value);
        }
        this.$emit('errorState', {
          questionKey: this.questionKey,
          value: this.message !== '',
          uniqueId: this.uniqueId,
        })
      },
      deep: true,
    },
    inputPlus(v) {
      this.buildCheckboxPlusVModal({ key: 'other', value: v })
    },
    selectedOption(newValue) {
      if (newValue !== 'Other') {
        this.customInput = '';
        this.$emit('update:modelValue', newValue);
      } else {
        this.$emit('update:modelValue', this.customInput);
      }
    },
    customInput(newValue) {
      if (this.selectedOption === 'Other') {
        this.$emit('update:modelValue', newValue);
      }
    },
    selectedOptions: {

      handler(newValue) {
        this.$emit('update:modelValue', this.convertSelectedOptionsToString(newValue));

      },
      deep: true
    },

  },
  async mounted() {
    if (this.hasError) {
      this.checkForFormValidation(await this.modelValue)
    }
    if (this.modelValue !== null && this.isCheckboxPlus) {
      this.setInputPlus()
    }
    // Check if the modelValue exists in options, or set it as 'Other'
    if (this.modelValue && this.options.includes(this.modelValue)) {
      this.selectedOption = this.modelValue; // Preselect the saved option
    } else if (this.modelValue) {
      this.selectedOption = 'Other'; // Preselect "Other" if value not in options
      this.customInput = this.modelValue; // Set the custom input to saved value
    }
    if (this.isSelectMultipleWithOther && typeof this.modelValue === 'string') {
      this.selectedOptions = this.convertStringToSelectedOptions(this.modelValue);
    }
  },
  methods: {
    resetInputState() {
      this.message = ''
      this.passwordRepeat = ''
      this.showPassword = false
    },
    checkForFormValidation(value) {
      if (this.type === 'select' && this.required) {
        this.validateSelect(value)
      } else if (this.type === 'email') {
        this.validateEmail(value)
      } else if (this.type === 'password-repeat') {
        this.validatePassword(value)
      } else if (this.type === 'checkbox' && this.required) {
        this.validateCheckbox(value)
      } else if (this.type === 'checkboxPlus' && this.required) {
        this.validateCheckboxPlus(value)
      } else if (this.textMinLength || this.textMaxLength) {
        this.validateLength(value)
      } else if (this.required) {
        this.validateInput(value)
      }
      const regex = /[^A-z0-9\\_\-\\.\\<\\>\\?\\@\\*\\%\\$€\\&\\/\\§\\!\\:\\;\\,\\+\\=\\(\\)\\}\\{\\"\\'\#\'\\Ä-ü\s\–]/;
      if ((this.type !== 'email' && this.type !== 'password-repeat' && this.type !== 'password') && !this.allowSpecialCharacters && regex.test(JSON.stringify(value))

      ) {
        const matches = value.match(regex);
        const foundCharacters = matches.map(match => match.trim());
        this.message = `The following characters are not alowed: ${foundCharacters.join(', ')}`
      } else {
        this.message = ''
      }
    },
    toggleShow() {
      this.showPassword = !this.showPassword
    },
    validateSelect(value) {
      if (value !== '') {
        this.message = ''
      } else {
        this.message = 'Select an option'
      }
    },
    validateEmail(value) {
      if (/^(.+)@(.+)*(\.\w{2,3})+$/.test(value)) {
        this.message = ''
      } else {
        this.message = 'Invalid Email Address'
      }
    },
    validateLength(value) {
      if (value.length < this.textMinLength) {
        this.message = `Input must be at least ${this.textMinLength} characters`
      } else if (value.length > this.textMaxLength) {
        this.message = `Input can't be longer then ${this.textMaxLength} characters`
      } else {
        this.message = ''
      }
    },
    validateInput(value) {
      if (value.trim !== '') {
        this.message = ''
      } else {
        this.message = 'Input is required'
      }
    },
    // validatePassword(value) {
    //   let regex = /^(?=.*[0-9])(?=.*[!@.#$%^&*])(?=.*[A-Z])[a-zA-Z0-9!@#,$%.^&*]{8,}$/
    //   if (regex.test(value)) {
    //     this.message = ''
    //   } else if (value.length < this.textMinLength) {
    //     this.message = `Input must be at least ${this.textMinLength} characters`
    //   } else if (value.length > this.textMaxLength) {
    //     this.message = `Input can't be longer then ${this.textMaxLength} characters`
    //   } else {
    //     this.message =
    //       'Password must contain at least one lower case letter, one upper case letter and contain at least one special character.'
    //   }
    // },
    validatePasswordMatch(value) {
      if (this.modelValue && value && this.modelValue !== value) {
        this.message = 'Passwords do not match.';
      } else {
        // Only clear the message if it was a password match error
        if (this.message === 'Passwords do not match.') {
          this.message = '';
        }
      }
    },
    validatePassword(value) {
      let hasUpperCase = /[A-Z]/.test(value);
      let hasLowerCase = /[a-z]/.test(value);
      let hasDigit = /\d/.test(value);
      // let hasSpecialChar = /[!@.#$%^&*]/.test(value);
      let hasSpecialChar = /[!@.#$%^&*(),\[\]=§{}?><\/\\~+;:_-]/.test(value);


      let errorMessages = [];

      if (!hasUpperCase) {
        errorMessages.push('Password must contain at least one upper case letter.');
      }

      if (!hasLowerCase) {
        errorMessages.push('Password must contain at least one lower case letter.');
      }

      if (!hasDigit) {
        errorMessages.push('Password must contain at least one digit.');
      }

      if (!hasSpecialChar) {
        errorMessages.push('Password must contain at least one special character.');
      }

      if (value.length < this.textMinLength) {
        errorMessages.push(`Password must be at least ${this.textMinLength} characters long.`);
      }

      if (value.length > this.textMaxLength) {
        errorMessages.push(`Input can't be longer than ${this.textMaxLength} characters.`);
      }

      if (errorMessages.length > 0) {
        // this.message = `<ul><li>${errorMessages.join('</li><li>')}</li></ul>`;
        this.message = errorMessages
      } else {
        this.message = '';
      }
    },

    validateCheckbox(value) {
      if (value) {
        this.message = ''
      } else {
        this.message = 'Checkbox is required'
      }
    },
    validateCheckboxPlus(value) {
      if (value.length > 0) {
        this.message = ''
      } else {
        this.message = 'Please select at least one option'
      }
    },
    setCheckboxPlusVModal(obj) {
      return this.modelValue?.includes(obj)
    },
    buildCheckboxPlusVModal(obj) {
      let testList = this.modelValue ? this.modelValue : []
      if (obj.key === 'checkbox') {
        // for checkbox's
        if (!testList.includes(obj.value)) {
          testList.push(obj.value)
        } else {
          const item = testList.indexOf(obj.value)
          testList = testList.filter((x, idx) => idx !== item)
        }
      } else {
        // for custom input value
        const idx = testList.map((x) => x.key).indexOf('other')
        if (obj.value === '') {
          testList.splice(idx, 1)
        } else {
          if (idx !== -1) {
            testList[idx] = obj
          } else {
            testList.push(obj)
          }
        }
      }
      this.$emit('update:modelValue', testList)
    },
    setInputPlus() {
      this.modelValue.forEach((x) => {
        if (x.key === 'other') {
          this.inputPlus = x.value
        }
      })
    },
    convertSelectedOptionsToString(options) {
      if (Array.isArray(options)) {
        return options.join(',');
      }
      return options;
    },

    convertStringToSelectedOptions(string) {
      if (typeof string === 'string' && string !== undefined) {
        if (string === '') {
          return []
        } else {
          return string.split(',').map(option => (option));
        }
      }
      return string;
    },
    addCustomInput(input) {
      this.options.push(input)
      this.selectedOptions.push(input)
      // this.selectedOptions = this.selectedOptions.concat(',', input)
    }
  },
}
</script>

<style>
/* @import 'vue-multiselect/dist/vue-multiselect.css'; */
@import url('https://unpkg.com/vue-multiselect/dist/vue-multiselect.min.css');

.multiselect__tags {
  font-size: 17px;
}

.multiselect__tag-icon::after {
  content: "x";
  color: #266d4d;
  font-size: 17px;
}

.multiselect__select {
  z-index: 1;
}

.multiselect__select::before {
  position: relative;
  right: 0;
  top: 40%;
  margin-top: 0;
  border: none;
  content: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3e%3cpath fill='none' stroke='%23343a40' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m2 5 6 6 6-6'/%3e%3c/svg%3e");
}

.multiselect--active .multiselect__select {
  transform: translate(0%, 5%);
}
</style>
