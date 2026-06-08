<template>
  <div class="home-page">
    <div class="home-layout">
      <!-- Left Sidebar -->
      <aside class="home-sidebar">
        <!-- Personal Info Card -->
        <div class="sidebar-card fade-in">
          <img
            v-if="userStore.user?.avatar"
            :src="userStore.user.avatar"
            class="sidebar-avatar"
            alt="avatar"
          />
          <div
            v-else
            class="sidebar-avatar"
            style="background:var(--surface);display:flex;align-items:center;justify-content:center;font-size:28px;"
          >&#9998;</div>
          <div class="sidebar-name">{{ userStore.user?.nickname || '博主' }}</div>
          <div class="sidebar-bio">记录思考、技术与生活。</div>
          <div class="sidebar-divider"></div>
          <div class="sidebar-stat">
            <span class="sidebar-stat-num">{{ stats.posts }}</span>
            <span class="sidebar-stat-label">文章</span>
          </div>
          <div class="sidebar-stat">
            <span class="sidebar-stat-num">{{ stats.messages }}</span>
            <span class="sidebar-stat-label">留言</span>
          </div>
          <div class="sidebar-stat">
            <span class="sidebar-stat-num">{{ stats.totalWords.toLocaleString() }}</span>
            <span class="sidebar-stat-label">总字数</span>
          </div>
        </div>

        <!-- Tags -->
        <div class="sidebar-card fade-in" style="animation-delay:0.08s">
          <div class="sidebar-card-title">分类标签</div>
          <div class="tag-cloud">
            <span v-if="!tags.length" style="font-size:13px;color:var(--text-muted)">暂无标签</span>
            <span v-for="tag in tags" :key="tag.name" class="tag-pill" @click="goTag(tag.name)">
              {{ tag.name }} ({{ tag.count }})
            </span>
          </div>
        </div>

        <!-- Recent Messages -->
        <div class="sidebar-card fade-in" style="animation-delay:0.12s">
          <div class="sidebar-card-title">💬 最近留言</div>
          <div v-if="!recentMessages.length" style="font-size:12px;color:var(--text-muted);text-align:center;padding:8px 0">暂无留言</div>
          <div v-else class="recent-msgs">
            <div v-for="msg in recentMessages" :key="msg.id" class="recent-msg-item">
              <div class="recent-msg-top">
                <span class="recent-msg-name">{{ msg.name }}</span>
                <span class="recent-msg-date">{{ formatShortDate(msg.created_at) }}</span>
              </div>
              <div class="recent-msg-content">{{ msg.content.slice(0, 40) }}{{ msg.content.length > 40 ? '...' : '' }}</div>
            </div>
          </div>
        </div>
      </aside>

      <!-- Main Content -->
      <main class="home-main">
        <h2 class="page-title">最新文章</h2>

        <div v-if="loading" style="padding:10px 0;">
          <div v-for="i in 3" :key="i" class="skeleton" style="height:110px;margin-bottom:16px;"></div>
        </div>

        <div v-else-if="!posts.length" class="empty-state">
          <div class="empty-state-icon">&#128221;</div>
          <p class="empty-state-text">还没有文章，博主正在努力创作中...</p>
        </div>

        <div v-else class="reveal-stagger" ref="postListRef">
          <div class="post-card" v-for="post in posts" :key="post.id">
            <div class="post-card-tags" v-if="extractTags(post.title).length">
              <span class="tag-pill tag-pill-sm" v-for="t in extractTags(post.title)" :key="t">{{ t }}</span>
            </div>
            <div class="title">
              <router-link :to="`/posts/${post.id}`">{{ post.title }}</router-link>
            </div>
            <div class="summary">{{ post.summary || stripHtml(post.content).slice(0, 150) }}</div>
            <div class="meta">
              <span>{{ formatDate(post.created_at) }}</span>
              <span>&middot;</span>
              <span>{{ wordCountVal(post) }} 字</span>
            </div>
          </div>
        </div>
      </main>

      <!-- Right Sidebar -->
      <aside class="home-rightbar">
        <!-- Mini Calendar -->
        <div class="sidebar-card fade-in" style="animation-delay:0.04s">
          <div class="sidebar-card-title">📅 {{ calendarTitle }}</div>
          <div class="mini-calendar">
            <div class="cal-weekdays">
              <span v-for="d in weekDays" :key="d">{{ d }}</span>
            </div>
            <div class="cal-grid">
              <span
                v-for="(day, i) in calendarDays"
                :key="i"
                class="cal-day"
                :class="{
                  'cal-today': day === today && day > 0,
                  'cal-other': day === 0
                }"
              >{{ day || '' }}</span>
            </div>
          </div>
        </div>

        <!-- Site Stats -->
        <div class="sidebar-card fade-in" style="animation-delay:0.08s">
          <div class="sidebar-card-title">📊 站点统计</div>
          <div class="site-stats-list">
            <div class="site-stat-item">
              <span class="site-stat-icon">📝</span>
              <span class="site-stat-label">文章总数</span>
              <span class="site-stat-val">{{ stats.posts }}</span>
            </div>
            <div class="site-stat-item">
              <span class="site-stat-icon">💬</span>
              <span class="site-stat-label">留言总数</span>
              <span class="site-stat-val">{{ stats.messages }}</span>
            </div>
            <div class="site-stat-item">
              <span class="site-stat-icon">📖</span>
              <span class="site-stat-label">总字数</span>
              <span class="site-stat-val">{{ stats.totalWords.toLocaleString() }}</span>
            </div>
            <div class="site-stat-item">
              <span class="site-stat-icon">⏱️</span>
              <span class="site-stat-label">运行天数</span>
              <span class="site-stat-val">{{ runDays }}</span>
            </div>
            <div class="site-stat-item">
              <span class="site-stat-icon">🏷️</span>
              <span class="site-stat-label">分类标签</span>
              <span class="site-stat-val">{{ tags.length }}</span>
            </div>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { getPosts, getMessages } from '../api'
import { useUserStore } from '../stores/user'

const userStore = useUserStore()
const router = useRouter()
const posts = ref([])
const loading = ref(true)
const postListRef = ref(null)

const stats = ref({ posts: 0, messages: 0, totalWords: 0 })
const tags = ref([])
const recentMessages = ref([])

const SITE_START = new Date('2026-06-04')
const runDays = computed(() => Math.floor((Date.now() - SITE_START.getTime()) / (1000 * 60 * 60 * 24)))

function formatDate(d) {
  return new Date(d).toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
}

function formatShortDate(d) {
  return new Date(d).toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' })
}

function stripHtml(html) {
  if (!html) return ''
  return html.replace(/<[^>]*>/g, '').trim()
}

function wordCountVal(post) {
  // Use content (stripped of HTML) as primary word count source
  const text = stripHtml(post.content)
  if (text) return text.length
  // Fall back to summary
  return (post.summary || '').replace(/<[^>]*>/g, '').length
}

function extractTags(title) {
  const matches = []
  const hashTags = title.match(/#(\S+)/g)
  if (hashTags) matches.push(...hashTags.map(t => t.replace('#', '')))
  const bracketTags = title.match(/【(.+?)】/g)
  if (bracketTags) matches.push(...bracketTags.map(t => t.replace(/【|】/g, '')))
  return [...new Set(matches)].slice(0, 3)
}

function buildTags(postsList) {
  const tagMap = {}
  postsList.forEach(p => {
    const tgs = extractTags(p.title)
    tgs.forEach(t => {
      tagMap[t] = (tagMap[t] || 0) + 1
    })
  })
  return Object.entries(tagMap)
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 12)
}

function goTag(tag) {
  router.push({ path: '/posts', query: { search: tag } })
}

// ---- Mini Calendar ----
const weekDays = ['日', '一', '二', '三', '四', '五', '六']
const now = new Date()
const today = now.getDate()
const calYear = ref(now.getFullYear())
const calMonth = ref(now.getMonth()) // 0-indexed

const calendarTitle = computed(() => {
  return `${calYear.value}年${calMonth.value + 1}月`
})

const calendarDays = computed(() => {
  const year = calYear.value
  const month = calMonth.value
  const firstDay = new Date(year, month, 1).getDay() // 0=Sun
  const daysInMonth = new Date(year, month + 1, 0).getDate()

  const days = []
  for (let i = 0; i < firstDay; i++) days.push(0)
  for (let d = 1; d <= daysInMonth; d++) days.push(d)
  return days
})

onMounted(async () => {
  try {
    const [postsRes, msgsRes] = await Promise.all([getPosts(), getMessages()])
    posts.value = postsRes.data
    const totalWords = postsRes.data.reduce((sum, p) => {
      const text = stripHtml(p.content)
      return sum + (text ? text.length : (p.summary || '').replace(/<[^>]*>/g, '').length)
    }, 0)
    stats.value = {
      posts: postsRes.data.length,
      messages: msgsRes.data.length,
      totalWords,
    }
    tags.value = buildTags(postsRes.data)
    recentMessages.value = msgsRes.data.slice(0, 5)
  } catch {}
  loading.value = false

  await nextTick()
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible')
          observer.unobserve(entry.target)
        }
      })
    },
    { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
  )
  document.querySelectorAll('.reveal-stagger').forEach((el) => observer.observe(el))
})
</script>

<style scoped>
/* Mini Calendar */
.mini-calendar {
  font-size: 13px;
}

.cal-weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  text-align: center;
  margin-bottom: 6px;
  color: var(--text-muted);
  font-weight: 500;
  font-size: 12px;
}

.cal-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
  text-align: center;
}

.cal-day {
  padding: 6px 0;
  border-radius: 8px;
  color: var(--text-secondary);
  font-size: 13px;
  transition: background 0.15s;
}

.cal-day.cal-other {
  pointer-events: none;
}

.cal-day.cal-today {
  background: var(--primary);
  color: #fff;
  font-weight: 600;
  border-radius: 50%;
}

/* Recent Messages */
.recent-msgs {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.recent-msg-item {
  padding: 8px 6px;
  border-radius: 8px;
  transition: background 0.15s;
}

.recent-msg-item:hover {
  background: var(--surface-hover);
}

.recent-msg-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 3px;
}

.recent-msg-name {
  font-size: 12px;
  font-weight: 600;
  color: var(--primary);
}

.recent-msg-date {
  font-size: 10.5px;
  color: var(--text-muted);
}

.recent-msg-content {
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.5;
}

/* Site Stats List */
.site-stats-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.site-stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 7px 6px;
  border-radius: 8px;
  transition: background 0.15s;
}

.site-stat-item:hover {
  background: var(--surface-hover);
}

.site-stat-icon {
  font-size: 15px;
  flex-shrink: 0;
}

.site-stat-label {
  flex: 1;
  font-size: 13px;
  color: var(--text-secondary);
}

.site-stat-val {
  font-size: 13px;
  font-weight: 650;
  color: var(--primary);
}
</style>
