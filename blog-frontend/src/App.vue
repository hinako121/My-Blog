<template>
  <div v-if="!$route.meta.requiresAuth">
    <NavBar />
    <div class="page">
      <router-view v-slot="{ Component }">
        <transition name="page-fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>
    <footer class="footer">
      <div class="footer-inner">
        <div class="footer-col">
          <span>&copy; 2026 My Blog</span>
          <span class="footer-dot">&middot;</span>
          <span>已运行 <strong>{{ runDays }}</strong> 天</span>
        </div>
        <div class="footer-col">
          <span class="footer-label">技术栈</span>
          <span>Vue 3 + FastAPI + SQLite</span>
        </div>
        <div class="footer-links">
          <router-link to="/">首页</router-link>
          <router-link to="/posts">文章</router-link>
          <router-link to="/about">关于</router-link>
          <router-link to="/guestbook">留言</router-link>
        </div>
      </div>
    </footer>

    <!-- Cursor glow -->
    <div
      class="cursor-glow"
      :style="{ left: cursorX + 'px', top: cursorY + 'px' }"
    ></div>

    <!-- Particle canvas -->
    <canvas ref="canvasRef" class="particle-canvas"></canvas>
  </div>
  <router-view v-else />
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import NavBar from './components/NavBar.vue'
import { useUserStore } from './stores/user'
const userStore = useUserStore()
if (localStorage.getItem('token')) userStore.fetchUser()

const SITE_START = new Date('2026-06-04')
const runDays = computed(() => {
  return Math.floor((Date.now() - SITE_START.getTime()) / (1000 * 60 * 60 * 24))
})

// Cursor position
const cursorX = ref(0)
const cursorY = ref(0)
let mouseX = 0, mouseY = 0

function onMouseMove(e) {
  cursorX.value = e.clientX
  cursorY.value = e.clientY
  mouseX = e.clientX
  mouseY = e.clientY
}

// ---- Particle system ----
const canvasRef = ref(null)
let ctx, canvas, animId
let particles = []
let prevX = 0, prevY = 0

const MAX_PARTICLES = 120
const PARTICLE_LIFE = 60 // frames

function resizeCanvas() {
  if (!canvas) return
  canvas.width = window.innerWidth
  canvas.height = window.innerHeight
}

function spawnParticles(x, y) {
  const dx = x - prevX
  const dy = y - prevY
  const dist = Math.sqrt(dx * dx + dy * dy)
  const count = Math.min(Math.floor(dist / 6), 12)

  for (let i = 0; i < count; i++) {
    const t = i / count
    const px = prevX + dx * t
    const py = prevY + dy * t
    particles.push({
      x: px + (Math.random() - 0.5) * 8,
      y: py + (Math.random() - 0.5) * 8,
      vx: (Math.random() - 0.5) * 1.2,
      vy: (Math.random() - 0.5) * 1.2 - 0.3,
      life: PARTICLE_LIFE,
      maxLife: PARTICLE_LIFE,
      size: Math.random() * 3 + 1.5,
      hue: 240 + Math.random() * 40, // purple-ish range
    })
  }

  // Trim excess
  while (particles.length > MAX_PARTICLES) {
    particles.shift()
  }

  prevX = x
  prevY = y
}

function animate() {
  if (!ctx || !canvas) return
  ctx.clearRect(0, 0, canvas.width, canvas.height)

  for (let i = particles.length - 1; i >= 0; i--) {
    const p = particles[i]
    p.life--
    if (p.life <= 0) {
      particles.splice(i, 1)
      continue
    }

    p.x += p.vx
    p.y += p.vy
    p.vx *= 0.99
    p.vy *= 0.99

    const alpha = p.life / p.maxLife
    const size = p.size * alpha

    ctx.beginPath()
    ctx.arc(p.x, p.y, size, 0, Math.PI * 2)
    ctx.fillStyle = `hsla(${p.hue}, 70%, 65%, ${alpha * 0.7})`
    ctx.fill()
  }

  animId = requestAnimationFrame(animate)
}

onMounted(() => {
  // Canvas setup
  canvas = canvasRef.value
  if (canvas) {
    ctx = canvas.getContext('2d')
    resizeCanvas()
    prevX = mouseX
    prevY = mouseY
    animate()
  }

  window.addEventListener('mousemove', onMouseMove, { passive: true })
  window.addEventListener('resize', resizeCanvas)

  // Spawn particles on a timer for continuous trail
  const spawnTimer = setInterval(() => {
    if (mouseX > 0 || mouseY > 0) {
      spawnParticles(mouseX, mouseY)
    }
  }, 1000 / 60) // 60fps
  window._particleTimer = spawnTimer
})

onUnmounted(() => {
  window.removeEventListener('mousemove', onMouseMove)
  window.removeEventListener('resize', resizeCanvas)
  if (animId) cancelAnimationFrame(animId)
  if (window._particleTimer) clearInterval(window._particleTimer)
})
</script>

<style>
/* Page transition */
.page-fade-enter-active,
.page-fade-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}

.page-fade-enter-from {
  opacity: 0;
  transform: translateY(8px);
}

.page-fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* ======== Cursor Glow ======== */
.cursor-glow {
  position: fixed;
  pointer-events: none;
  z-index: 9998;
  width: 300px;
  height: 300px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.10) 0%, rgba(99, 102, 241, 0.03) 40%, transparent 70%);
  transform: translate(-50%, -50%);
  transition: left 0.5s ease-out, top 0.5s ease-out;
  will-change: left, top;
}

/* ======== Particle Canvas ======== */
.particle-canvas {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 9999;
}

@media (max-width: 768px) {
  .cursor-glow,
  .particle-canvas {
    display: none;
  }
}

@media (prefers-reduced-motion: reduce) {
  .cursor-glow,
  .particle-canvas {
    display: none;
  }
}
</style>
