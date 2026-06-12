const js = require('@eslint/js')
const vue = require('eslint-plugin-vue')
// eslint-plugin-prettier is not a flat config plugin yet, so we use it as a legacy plugin if needed,
// but here we just use it for the rule and plugin definition manually as per plan.
const prettier = require('eslint-plugin-prettier')
const globals = require('globals')

module.exports = [
  js.configs.recommended,
  ...vue.configs['flat/essential'],
  {
    plugins: {
      prettier,
    },
    rules: {
      'prettier/prettier': 'error',
      'no-unused-vars': 'off',
      'no-empty': 'off',
      'no-prototype-builtins': 'off',
      'no-useless-escape': 'off',
      'vue/multi-word-component-names': 'off',
      'vue/no-async-in-computed-properties': 'off',
      'vue/no-mutating-props': 'off',
      'vue/no-reserved-component-names': 'off',
      'vue/no-unused-components': 'off',
      'vue/no-unused-vars': 'off',
      'vue/no-useless-template-attributes': 'off',
      'vue/valid-template-root': 'off',
    },
    languageOptions: {
      ecmaVersion: 'latest',
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
  },
  {
    ignores: ['dist/', 'node_modules/', 'public/'],
  },
]
