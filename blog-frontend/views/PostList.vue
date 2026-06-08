<template>
  <div class="container">
    <h1 class="page-title">
      <template v-if="searchQuery">🔍 搜索: "{{ searchQuery }}"</template>
      <template v-else>📚 所有文章</template>
    </h1>

    <div v-if="loading" style="text-align:center;padding:60px;color:var(--text-muted)">加载中...</div>
    <div v-else-if="!filteredPosts.length" style="text-align:center;padding:60px;color:var(--text-muted)">
      {{ searchQuery ? '没有找到匹配的文章' : '暂无文章' }}
    </div>
    <div v-else class="post-card" v-for="post in filteredPosts" :key="post.id">
      <div class="title">
        <router-link :to="`/posts/${post.id}`" v-html="highlight(post.title)"></router-link>
      </div>
      <div class="summary" v-html="highlight(post.summary || '暂无摘要')"></div>
      <div class="meta">
        <span>📅 {{ formatDate(post.created_at) }}</span>
        <span>📖 {{ postCount(post) }} 字</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getPosts } from '../api'

const route = useRoute()
const posts = ref([])
const loading = ref(true)

const searchQuery = computed(() => route.query.search || '')

const filteredPosts = computed(() => {
  if (!searchQuery.value) return posts.value
  const q = searchQuery.value.toLowerCase()
  return posts.value.filter(p =>
    p.title.toLowerCase().includes(q) ||
    (p.summary && p.summary.toLowerCase().includes(q))
  )
})

function formatDate(d) { return new Date(d).toLocaleDateString('zh-CN') }

function postCount(post) {
  const text = (post.summary || '').replace(/<[^>]*>/g, '')
  return text.length
}

function highlight(text) {
  if (!searchQuery.value || !text) return text
  const q = searchQuery.value
  const idx = text.toLowerCase().indexOf(q.toLowerCase())
  if (idx === -1) return text
  return text.slice(0, idx) + '<span class="search-highlight">' + text.slice(idx, idx + q.length) + '</span>' + text.slice(idx + q.length)
}

onMounted(async () => {
  const res = await getPosts()
  posts.value = res.data
  loading.value = false
})
</script>
