<template>
  <nav class="glass-nav">
    <div class="inner">
      <!-- Logo / 首页 -->
      <router-link to="/" class="logo">📝 My Blog</router-link>

      <!-- Nav links with dynamic hover effect -->
      <router-link to="/" class="nav-link" :class="{ active: $route.path === '/' }">首页</router-link>
      <router-link to="/me" class="nav-link">我的</router-link>
      <router-link to="/guestbook" class="nav-link">留言</router-link>
      <router-link to="/about" class="nav-link">关于作者</router-link>

      <div class="spacer"></div>

      <!-- Search box -->
      <div class="search-box">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索文章..."
          @keyup.enter="doSearch"
        />
        <span class="search-icon">🔍</span>
      </div>

      <!-- Theme toggle -->
      <button class="theme-toggle" @click="cycleTheme" :title="themeLabel">
        <span v-if="themeStore.resolved === 'light'">☀️</span>
        <span v-else-if="themeStore.resolved === 'dark'">🌙</span>
        <span v-else>💻</span>
      </button>

      <!-- Admin link -->
      <router-link v-if="userStore.user" to="/admin" class="nav-link" title="后台管理">⚙️</router-link>
      <router-link v-else to="/admin/login" class="nav-link" title="登录">🔑</router-link>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { useThemeStore } from '../stores/theme'

const router = useRouter()
const userStore = useUserStore()
const themeStore = useThemeStore()

const searchQuery = ref('')

const themeLabel = ref('切换主题')

function doSearch() {
  const q = searchQuery.value.trim()
  if (!q) return
  router.push({ name: 'PostList', query: { search: q } })
}

function cycleTheme() {
  const order = ['light', 'dark', 'system']
  const idx = order.indexOf(themeStore.mode)
  const next = order[(idx + 1) % order.length]
  themeStore.setMode(next)
  const labels = { light: '☀️ 亮色', dark: '🌙 暗色', system: '💻 跟随系统' }
  themeLabel.value = labels[next]
}
</script>
