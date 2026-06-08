<template>
  <div class="container">
    <h1 class="page-title">📔 日记</h1>

    <div v-if="loading" style="padding:10px 0;">
      <div v-for="i in 4" :key="i" class="skeleton" style="height:100px;margin-bottom:16px;"></div>
    </div>

    <div v-else-if="!diaries.length" class="empty-state">
      <div class="empty-state-icon">📖</div>
      <p class="empty-state-text">还没有日记，记录生活的点滴吧</p>
    </div>

    <div v-else class="timeline" ref="timelineRef">
      <div class="timeline-entry reveal-stagger" v-for="diary in diaries" :key="diary.id">
        <div class="timeline-dot">{{ diary.mood || '📝' }}</div>
        <div class="timeline-card">
          <div class="timeline-date">{{ formatDate(diary.created_at) }}</div>
          <div class="timeline-title">{{ diary.title }}</div>
          <div class="timeline-content">{{ diary.content }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { getDiaries } from '../api'

const diaries = ref([])
const loading = ref(true)
const timelineRef = ref(null)

function formatDate(d) {
  return new Date(d).toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric', weekday: 'short' })
}

onMounted(async () => {
  try { const res = await getDiaries(); diaries.value = res.data } catch {}
  loading.value = false

  await nextTick()
  if (timelineRef.value) {
    new IntersectionObserver((entries) => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible') } })
    }, { threshold: 0.1 }).observe(timelineRef.value)
  }
})
</script>

<style scoped>
.timeline {
  position: relative;
  padding-left: 40px;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 15px;
  top: 8px;
  bottom: 8px;
  width: 2px;
  background: var(--border-strong);
  border-radius: 1px;
}

.timeline-entry {
  position: relative;
  margin-bottom: 20px;
}

.timeline-dot {
  position: absolute;
  left: -40px;
  top: 14px;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  background: var(--surface-elevated);
  border: 2px solid var(--border-strong);
  border-radius: 50%;
  z-index: 1;
}

.timeline-card {
  position: relative;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius);
  box-shadow: var(--glass-shadow);
  padding: 20px 22px;
  overflow: hidden;
  transition: transform 0.35s var(--ease-out-expo), box-shadow 0.35s var(--ease-out-expo);
}

.timeline-card::before {
  content: '';
  position: absolute;
  inset: 0;
  z-index: -1;
  border-radius: inherit;
  background: linear-gradient(180deg, var(--glass-highlight) 0%, transparent 40%);
  pointer-events: none;
}

.timeline-card:hover {
  transform: translateX(4px);
  box-shadow: var(--glass-shadow-hover);
}

.timeline-date {
  font-size: 12.5px;
  color: var(--primary);
  font-weight: 500;
  margin-bottom: 6px;
}

.timeline-title {
  font-size: 17px;
  font-weight: 650;
  color: var(--text);
  margin-bottom: 8px;
  line-height: 1.3;
}

.timeline-content {
  font-size: 14.5px;
  color: var(--text-secondary);
  line-height: 1.75;
  white-space: pre-wrap;
}

/* Responsive */
@media (max-width: 768px) {
  .timeline {
    padding-left: 34px;
  }

  .timeline::before {
    left: 12px;
  }

  .timeline-dot {
    left: -34px;
    width: 28px;
    height: 28px;
    font-size: 17px;
  }

  .timeline-card {
    padding: 16px 18px;
  }

  .timeline-title {
    font-size: 15px;
  }

  .timeline-content {
    font-size: 13.5px;
  }
}

@media (max-width: 480px) {
  .timeline {
    padding-left: 30px;
  }

  .timeline::before {
    left: 10px;
  }

  .timeline-dot {
    left: -30px;
    width: 24px;
    height: 24px;
    font-size: 15px;
    top: 10px;
  }

  .timeline-entry {
    margin-bottom: 14px;
  }

  .timeline-card {
    padding: 14px 14px;
  }

  .timeline-date {
    font-size: 11.5px;
  }

  .timeline-title {
    font-size: 14px;
  }

  .timeline-content {
    font-size: 13px;
    line-height: 1.65;
  }
}
</style>
