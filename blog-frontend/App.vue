<template>
  <div v-if="!$route.meta.requiresAuth">
    <NavBar />
    <div class="page">
      <router-view />
    </div>
    <div class="footer">© 2026 My Blog · Built with ❤️</div>
  </div>
  <router-view v-else />
</template>

<script setup>
import { onMounted } from 'vue'
import NavBar from './components/NavBar.vue'
import { useUserStore } from './stores/user'
import { useThemeStore } from './stores/theme'
import { getSettings } from './api'

const userStore = useUserStore()
const themeStore = useThemeStore()

onMounted(async () => {
  themeStore.applyTheme()
  if (localStorage.getItem('token')) userStore.fetchUser()
  // Load background image from backend
  try {
    const res = await getSettings()
    if (res.data.background_image) {
      document.body.style.setProperty('--bg-image', `url(${res.data.background_image})`)
    }
  } catch {
    // settings not available
  }
})
</script>
