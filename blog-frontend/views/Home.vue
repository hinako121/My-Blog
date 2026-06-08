<template>
  <div class="container">
    <h1 class="page-title">📝 最新文章</h1>
    <div v-if="loading" style="text-align:center;padding:60px;color:var(--text-muted)">加载中...</div>
    <div v-else-if="!posts.length" style="text-align:center;padding:60px;color:var(--text-muted)">暂无文章</div>
    <div v-else class="post-card" v-for="post in posts" :key="post.id">
      <div class="title"><router-link :to="`/posts/${post.id}`">{{ post.title }}</router-link></div>
      <div class="summary">{{ post.summary || '暂无摘要' }}</div>
      <div class="meta">
        <span>📅 {{ formatDate(post.created_at) }}</span>
        <span>📖 {{ wordCount(post) }} 字</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getPosts } from '../api'
const posts = ref([])
const loading = ref(true)
function formatDate(d) { return new Date(d).toLocaleDateString('zh-CN') }
function wordCount(post) {
  return (post.summary || '').replace(/<[^>]*>/g, '').length
}
onMounted(async () => {
  const res = await getPosts()
  posts.value = res.data
  loading.value = false
})
</script>
