import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const mode = ref(localStorage.getItem('theme-mode') || 'system')
  const resolved = ref('light')

  function applyTheme() {
    if (mode.value === 'system') {
      resolved.value = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
    } else {
      resolved.value = mode.value
    }
    document.documentElement.setAttribute('data-theme', resolved.value)
  }

  function setMode(m) {
    mode.value = m
    localStorage.setItem('theme-mode', m)
    applyTheme()
  }

  // Watch system changes
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
  mediaQuery.addEventListener('change', () => {
    if (mode.value === 'system') applyTheme()
  })

  // Init
  applyTheme()

  return { mode, resolved, setMode, applyTheme }
})
