<template>
  <div class="container">
    <h1 class="page-title" v-if="!searchQuery">所有文章</h1>
    <h1 class="page-title" v-else>搜索: &ldquo;{{ searchQuery }}&rdquo;</h1>

    <div v-if="loading" style="padding: 20px 0;">
      <div v-for="i in 3" :key="i" class="skeleton" style="height: 100px; margin-bottom: 16px;"></div>
    </div>

    <div v-else-if="!filteredPosts.length" class="empty-state">
      <div class="empty-state-icon">{{ searchQuery ? '&#128269;' : '&#128221;' }}</div>
      <p class="empty-state-text">
        {{ searchQuery ? '没有找到匹配的文章，试试其他关键词吧' : '暂无文章' }}
      </p>
    </div>

    <div v-else class="reveal-stagger" ref="listRef">
      <div class="post-card" v-for="post in filteredPosts" :key="post.id">
        <div class="title">
          <router-link :to="`/posts/${post.id}`" v-html="highlight(post.title)"></router-link>
        </div>
        <div class="summary" v-html="highlight(post.summary || '暂无摘要')"></div>
        <div class="meta">
          <span>{{ formatDate(post.created_at) }}</span>
          <span>&middot;</span>
          <span>{{ postCount(post) }} 字</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { getPosts } from '../api'

const route = useRoute()
const posts = ref([])
const loading = ref(true)
const listRef = ref(null)

const searchQuery = computed(() => route.query.search || '')

const filteredPosts = computed(() => {
  if (!searchQuery.value) return posts.value
  const q = searchQuery.value.toLowerCase()
  return posts.value.filter(p =>
    p.title.toLowerCase().includes(q) ||
    (p.summary && p.summary.toLowerCase().includes(q))
  )
})

function formatDate(d) {
  return new Date(d).toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
}

function stripHtml(html) {
  if (!html) return ''
  return html.replace(/<[^>]*>/g, '').trim()
}

function postCount(post) {
  const text = stripHtml(post.content)
  if (text) return text.length
  return stripHtml(post.summary || '').length
}

function highlight(text) {
  if (!searchQuery.value || !text) return text
  const q = searchQuery.value
  const idx = text.toLowerCase().indexOf(q.toLowerCase())
  if (idx === -1) return text
  return text.slice(0, idx) + '<span class="search-highlight">' + text.slice(idx, idx + q.length) + '</span>' + text.slice(idx + q.length)
}

onMounted(async () => {
  try {
    const res = await getPosts()
    posts.value = res.data
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
