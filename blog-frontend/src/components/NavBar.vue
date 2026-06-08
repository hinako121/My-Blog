<template>
  <nav class="navbar" :class="{ scrolled: isScrolled }" ref="navRef">
    <div class="inner">
      <router-link to="/" class="logo">My Blog</router-link>

      <!-- Desktop nav links (centered) -->
      <div class="nav-links-desktop">
        <router-link to="/posts" class="nav-link">文章</router-link>
        <router-link to="/about" class="nav-link">关于我</router-link>
        <router-link to="/guestbook" class="nav-link">留言板</router-link>
      </div>

      <!-- Theme toggle -->
      <button class="theme-toggle" @click="cycleTheme" :title="themeLabel">
        <svg v-if="resolvedTheme === 'light'" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="5"/>
          <line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/>
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
          <line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/>
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
        </svg>
        <svg v-else width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
        </svg>
      </button>

      <!-- Hamburger menu button (mobile) -->
      <button class="hamburger-btn" @click="toggleMobileMenu" :aria-label="mobileMenuOpen ? '关闭菜单' : '打开菜单'">
        <span :class="{ open: mobileMenuOpen }"></span>
        <span :class="{ open: mobileMenuOpen }"></span>
        <span :class="{ open: mobileMenuOpen }"></span>
      </button>

      <!-- Avatar with dropdown -->
      <div v-if="userStore.user" class="avatar-wrapper" ref="dropdownRef">
        <button class="avatar-btn" @click="toggleDropdown">
          <img
            :src="userStore.user.avatar || '/img/default-avatar.svg'"
            class="nav-avatar"
            alt="用户菜单"
          />
        </button>

        <div v-if="showDropdown" class="avatar-dropdown">
          <div class="dropdown-user">
            <img
              :src="userStore.user.avatar || '/img/default-avatar.svg'"
              class="dropdown-avatar"
              alt=""
            />
            <span class="dropdown-nickname">{{ userStore.user.nickname || '用户' }}</span>
          </div>

          <div class="dropdown-items">
            <router-link to="/me" class="dropdown-item" @click="showDropdown = false">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
              </svg>
              个人中心
            </router-link>

            <router-link to="/album" class="dropdown-item" @click="showDropdown = false">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                <circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21,15 16,10 5,21"/>
              </svg>
              相册
            </router-link>

            <router-link to="/diary" class="dropdown-item" @click="showDropdown = false">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14,2 14,8 20,8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>
              </svg>
              日记
            </router-link>

            <router-link to="/tools" class="dropdown-item" @click="showDropdown = false">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
              </svg>
              工具分享
            </router-link>

            <div class="dropdown-divider"></div>

            <button class="dropdown-item" @click="cycleTheme">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="5"/>
                <line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/>
                <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
                <line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/>
                <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
              </svg>
              {{ themeLabel }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Mobile menu overlay -->
    <transition name="mobile-slide">
      <div v-if="mobileMenuOpen" class="mobile-menu" @click.self="mobileMenuOpen = false">
        <div class="mobile-menu-inner">
          <router-link to="/" class="mobile-nav-link" @click="mobileMenuOpen = false">首页</router-link>
          <router-link to="/posts" class="mobile-nav-link" @click="mobileMenuOpen = false">文章</router-link>
          <router-link to="/album" class="mobile-nav-link" @click="mobileMenuOpen = false">相册</router-link>
          <router-link to="/diary" class="mobile-nav-link" @click="mobileMenuOpen = false">日记</router-link>
          <router-link to="/tools" class="mobile-nav-link" @click="mobileMenuOpen = false">工具</router-link>
          <router-link to="/about" class="mobile-nav-link" @click="mobileMenuOpen = false">关于我</router-link>
          <router-link to="/guestbook" class="mobile-nav-link" @click="mobileMenuOpen = false">留言板</router-link>
          <router-link to="/me" class="mobile-nav-link" @click="mobileMenuOpen = false">个人中心</router-link>
        </div>
      </div>
    </transition>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

const userStore = useUserStore()
const router = useRouter()
const isScrolled = ref(false)
const showDropdown = ref(false)
const dropdownRef = ref(null)
const mobileMenuOpen = ref(false)

// ---- Theme ----
const themeMode = ref(localStorage.getItem('theme-mode') || 'system')

const resolvedTheme = computed(() => {
  if (themeMode.value === 'dark') return 'dark'
  if (themeMode.value === 'light') return 'light'
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
})

const themeLabel = computed(() => {
  if (themeMode.value === 'light') return '浅色模式'
  if (themeMode.value === 'dark') return '深色模式'
  return '跟随系统'
})

function applyTheme() {
  const resolved = resolvedTheme.value
  document.documentElement.setAttribute('data-theme', resolved)
  const meta = document.querySelector('meta[name="theme-color"]')
  if (meta) meta.content = resolved === 'dark' ? '#0f0f1a' : '#6366f1'
}

function cycleTheme() {
  if (themeMode.value === 'light') {
    themeMode.value = 'dark'
  } else if (themeMode.value === 'dark') {
    themeMode.value = 'system'
  } else {
    themeMode.value = 'light'
  }
  localStorage.setItem('theme-mode', themeMode.value)
  applyTheme()
}

function onSystemThemeChange() {
  if (themeMode.value === 'system') applyTheme()
}

// ---- Dropdown ----
function toggleDropdown() {
  showDropdown.value = !showDropdown.value
}

function onClickOutside(e) {
  if (dropdownRef.value && !dropdownRef.value.contains(e.target)) {
    showDropdown.value = false
  }
}

// ---- Mobile Menu ----
function toggleMobileMenu() {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

// Lock body scroll when mobile menu is open
import { watch } from 'vue'
watch(mobileMenuOpen, (v) => {
  document.body.style.overflow = v ? 'hidden' : ''
})

// ---- Scroll ----
function onScroll() {
  isScrolled.value = window.scrollY > 20
}

onMounted(() => {
  applyTheme()
  window.addEventListener('scroll', onScroll, { passive: true })
  document.addEventListener('click', onClickOutside)
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', onSystemThemeChange)
})

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
  document.removeEventListener('click', onClickOutside)
  window.matchMedia('(prefers-color-scheme: dark)').removeEventListener('change', onSystemThemeChange)
  document.body.style.overflow = ''
})
</script>

<style scoped>
/* ======== Desktop nav links ======== */
.nav-links-desktop {
  display: flex;
  align-items: center;
  gap: 4px;
  margin: 0 auto;
}

/* ======== Hamburger button ======== */
.hamburger-btn {
  display: none;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 5px;
  width: 36px;
  height: 36px;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--surface);
  cursor: pointer;
  padding: 7px 6px;
  margin-left: 8px;
  transition: background var(--transition-fast), border-color var(--transition-fast);
  flex-shrink: 0;
}

.hamburger-btn:hover {
  background: var(--surface-hover);
  border-color: var(--border-strong);
}

.hamburger-btn span {
  display: block;
  width: 20px;
  height: 2px;
  background: var(--text);
  border-radius: 2px;
  transition: transform 0.25s ease, opacity 0.25s ease;
}

.hamburger-btn span.open:nth-child(1) {
  transform: translateY(7px) rotate(45deg);
}

.hamburger-btn span.open:nth-child(2) {
  opacity: 0;
}

.hamburger-btn span.open:nth-child(3) {
  transform: translateY(-7px) rotate(-45deg);
}

/* ======== Mobile menu ======== */
.mobile-menu {
  position: fixed;
  inset: 0;
  top: 58px;
  z-index: 99;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.mobile-menu-inner {
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border-bottom: 1px solid var(--glass-border);
  padding: 12px 20px 20px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.mobile-nav-link {
  display: block;
  padding: 14px 16px;
  font-size: 16px;
  font-weight: 500;
  color: var(--text);
  border-radius: var(--radius-sm);
  text-decoration: none;
  transition: background var(--transition-fast), color var(--transition-fast);
}

.mobile-nav-link:hover,
.mobile-nav-link.router-link-active {
  background: var(--surface-hover);
  color: var(--primary);
}

/* Slide transition */
.mobile-slide-enter-active,
.mobile-slide-leave-active {
  transition: opacity 0.25s ease;
}
.mobile-slide-enter-active .mobile-menu-inner,
.mobile-slide-leave-active .mobile-menu-inner {
  transition: transform 0.25s var(--ease-out-expo);
}
.mobile-slide-enter-from,
.mobile-slide-leave-to {
  opacity: 0;
}
.mobile-slide-enter-from .mobile-menu-inner {
  transform: translateY(-20px);
}
.mobile-slide-leave-to .mobile-menu-inner {
  transform: translateY(-20px);
}

/* ======== Responsive ======== */
@media (max-width: 768px) {
  .nav-links-desktop {
    display: none;
  }

  .hamburger-btn {
    display: flex;
  }
}

@media (min-width: 769px) {
  .mobile-menu {
    display: none;
  }
}
</style>
