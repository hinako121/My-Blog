<template>
  <div class="container">
    <h1 class="page-title">💬 留言板</h1>

    <!-- Form -->
    <div class="guestbook-form">
      <div style="margin-bottom:12px">
        <input
          v-model="form.name"
          placeholder="你的名字（可选）"
          style="width:200px;padding:8px 12px;border:1px solid var(--border);border-radius:6px;background:rgba(255,255,255,0.3);color:var(--text);font-family:var(--font-display);font-size:14px;outline:none;transition:border-color 0.2s"
          @focus="$event.target.style.borderColor='var(--primary)'"
          @blur="$event.target.style.borderColor='var(--border)'"
        />
      </div>
      <textarea v-model="form.content" placeholder="写下你想说的话..." />
      <div style="display:flex;justify-content:space-between;align-items:center;margin-top:12px">
        <span style="font-size:12px;color:var(--text-muted)">{{ form.content.length }} 字</span>
        <button
          class="el-button el-button--primary"
          :disabled="!form.content.trim() || submitting"
          @click="submitMessage"
          style="padding:8px 24px;border:none;border-radius:6px;background:var(--primary);color:#fff;font-family:var(--font-display);font-size:14px;cursor:pointer;transition:opacity 0.2s"
          :style="{ opacity: !form.content.trim() || submitting ? 0.5 : 1 }"
        >
          {{ submitting ? '提交中...' : '发布留言' }}
        </button>
      </div>
    </div>

    <!-- Messages -->
    <div v-if="loading" style="text-align:center;padding:40px;color:var(--text-muted)">加载中...</div>
    <div v-else-if="!messages.length" style="text-align:center;padding:40px;color:var(--text-muted)">
      还没有留言，来留下第一条吧 🎉
    </div>
    <div v-else>
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
import { ref, reactive, onMounted } from 'vue'
import { getMessages, createMessage } from '../api'
import { ElMessage } from 'element-plus'

const messages = ref([])
const loading = ref(true)
const submitting = ref(false)
const form = reactive({ name: '', content: '' })

function formatDate(d) {
  return new Date(d).toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

onMounted(async () => {
  try {
    const res = await getMessages()
    messages.value = res.data
  } catch {}
  loading.value = false
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
