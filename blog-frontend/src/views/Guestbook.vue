<template>
  <div class="container">
    <h1 class="page-title">留言板</h1>

    <!-- Form -->
    <div class="guestbook-form">
      <div style="margin-bottom:14px">
        <input
          v-model="form.name"
          placeholder="你的名字（可选）"
          style="width:220px;padding:10px 14px;border:1px solid var(--border);border-radius:10px;background:var(--surface);color:var(--text);font-family:inherit;font-size:14px;outline:none;transition:border-color 0.2s,box-shadow 0.2s"
          @focus="onFocus($event)"
          @blur="onBlur($event)"
        />
      </div>
      <textarea
        v-model="form.content"
        placeholder="写下你想说的话..."
        @focus="onFocus($event)"
        @blur="onBlur($event)"
      />
      <div style="display:flex;justify-content:space-between;align-items:center;margin-top:14px">
        <span style="font-size:12px;color:var(--text-muted)">{{ form.content.length }} 字</span>
        <button
          class="btn btn-primary"
          :disabled="!form.content.trim() || submitting"
          @click="submitMessage"
          :style="{ opacity: !form.content.trim() || submitting ? 0.5 : 1 }"
        >
          {{ submitting ? '提交中...' : '发布留言' }}
        </button>
      </div>
    </div>

    <!-- Messages -->
    <div v-if="loading" style="padding: 20px 0;">
      <div v-for="i in 3" :key="i" class="skeleton" style="height: 70px; margin-bottom: 12px;"></div>
    </div>

    <div v-else-if="!messages.length" class="empty-state">
      <div class="empty-state-icon">&#128172;</div>
      <p class="empty-state-text">还没有留言，来留下第一条吧</p>
    </div>

    <div v-else class="reveal-stagger" ref="msgListRef">
      <div class="guestbook-item" v-for="msg in messages" :key="msg.id">
        <div class="msg-header">
          <span class="msg-name">{{ msg.name }}</span>
          <span class="msg-date">{{ formatDate(msg.created_at) }}</span>
        </div>
        <div class="msg-content">{{ msg.content }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { getMessages, createMessage } from '../api'
import { ElMessage } from 'element-plus'

const messages = ref([])
const loading = ref(true)
const submitting = ref(false)
const msgListRef = ref(null)
const form = reactive({ name: '', content: '' })

function formatDate(d) {
  return new Date(d).toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

function onFocus(e) {
  e.target.style.borderColor = 'var(--primary)'
  e.target.style.boxShadow = '0 0 0 3px var(--primary-glow)'
}

function onBlur(e) {
  e.target.style.borderColor = 'var(--border)'
  e.target.style.boxShadow = 'none'
}

onMounted(async () => {
  try {
    const res = await getMessages()
    messages.value = res.data
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
    { threshold: 0.1 }
  )
  if (msgListRef.value) observer.observe(msgListRef.value)
})

async function submitMessage() {
  if (!form.content.trim()) return
  submitting.value = true
  try {
    const res = await createMessage({ name: form.name.trim() || '匿名', content: form.content.trim() })
    messages.value.unshift(res.data)
    form.content = ''
    ElMessage.success('留言发布成功')
  } catch {
    ElMessage.error('发布失败，请重试')
  }
  submitting.value = false
}
</script>
