<template>
  <div class="container">
    <div v-if="loading" style="padding:20px 0;">
      <div class="skeleton" style="height:400px;"></div>
    </div>

    <div v-else-if="!post" class="empty-state">
      <div class="empty-state-icon">&#128533;</div>
      <p class="empty-state-text">文章不存在或已被删除</p>
    </div>

    <template v-else>
      <!-- Single glass card: title + content together -->
      <article class="post-article fade-in">
        <header class="post-article-header">
          <h1>{{ post.title }}</h1>
          <div class="post-meta">
            <span>{{ formatDate(post.created_at) }}</span>
            <span>&middot;</span>
            <span>{{ wordCount }} 字</span>
            <span v-if="post.updated_at !== post.created_at">&middot; 编辑于 {{ formatDate(post.updated_at) }}</span>
          </div>
        </header>
        <div class="post-content" v-html="renderedContent"></div>
      </article>
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

const wordCount = computed(() => {
  if (!post.value) return 0
  const text = post.value.content.replace(/<[^>]*>/g, '').replace(/\s+/g, '')
  return text.length
})

const renderedContent = computed(() => {
  if (!post.value) return ''
  let html = post.value.content
  html = html.replace(/<video([^>]*)>/gi, '<video$1 controls style="max-width:100%;border-radius:10px">')
  html = html.replace(/<img([^>]*)>/gi, '<img$1 loading="lazy" style="max-width:100%;border-radius:10px">')
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
