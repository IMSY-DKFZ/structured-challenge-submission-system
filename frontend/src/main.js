import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style/custom.scss'
import * as bootstrap from 'bootstrap';
// import '../node_modules/bootstrap/dist/css/bootstrap.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
// import '../node_modules/bootstrap/dist/js/bootstrap.bundle'
import piniaPluginPersistedState from 'pinia-plugin-persistedstate'

import router from './router'
import App from './App.vue'

window.bootstrap = bootstrap;

const pinia = createPinia()
pinia.use(piniaPluginPersistedState)
const app = createApp(App)
app.config.unwrapInjectedRef = true

app.use(router)
app.use(pinia)
app.mount('#app')
