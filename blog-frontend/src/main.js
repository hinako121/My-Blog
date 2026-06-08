import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import './style.css'

const app = createApp(App)
app.use(ElementPlus)
app.use(router)
app.use(createPinia())
Object.entries(ElementPlusIconsVue).forEach(([k, v]) => app.component(k, v))
app.mount('#app')
