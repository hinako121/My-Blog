<template>
  <div class="container">
    <div v-if="loading" style="text-align:center;padding:60px;color:var(--text-muted)">加载中...</div>
    <div v-else-if="!post" style="text-align:center;padding:60px;color:var(--text-muted)">文章不存在</div>
    <template v-else>
      <!-- Post header with meta -->
      <div class="post-header">
        <h1>{{ post.title }}</h1>
        <div class="post-meta">
          <span>📅 {{ formatDate(post.created_at) }}</span>
          <span>📖 {{ wordCount }} 字</span>
          <span v-if="post.updated_at !== post.created_at">🔄 编辑于 {{ formatDate(post.updated_at) }}</span>
        </div>
      </div>

      <!-- Post content -->
      <div class="post-content" v-html="renderedContent"></div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getPost } from '../api'

const route = useRoute()
const post = ref(null)
const loading = ref(true)

function formatDate(d) {
  return new Date(d).toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
}

// Strip HTML tags for word count
const wordCount = computed(() => {
  if (!post.value) return 0
  const text = post.value.content.replace(/<[^>]*>/g, '').replace(/\s+/g, '')
  return text.length
})

// Enhance content: wrap video/img with proper handling
const renderedContent = computed(() => {
  if (!post.value) return ''
  let html = post.value.content
  // Ensure videos have controls and proper styling
  html = html.replace(/<video([^>]*)>/gi, '<video$1 controls style="max-width:100%;border-radius:8px">')
  // Add lazy loading to images
  html = html.replace(/<img([^>]*)>/gi, '<img$1 loading="lazy" style="max-width:100%;border-radius:8px">')
  return html
})

onMounted(async () => {
  try {
    const res = await getPost(route.params.id)
    post.value = res.data
  } catch {
    post.value = null
  }
  loading.value = false
})
</script>
