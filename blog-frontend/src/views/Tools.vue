<template>
  <div class="container">
    <h1 class="page-title">🛠️ 工具分享</h1>

    <div v-if="loading" style="padding:10px 0;">
      <div v-for="i in 4" :key="i" class="skeleton" style="height:120px;margin-bottom:16px;"></div>
    </div>

    <div v-else-if="!tools.length" class="empty-state">
      <div class="empty-state-icon">🧰</div>
      <p class="empty-state-text">还没有工具推荐，敬请期待...</p>
    </div>

    <div v-else class="tools-grid reveal-stagger" ref="gridRef">
      <a
        v-for="tool in tools"
        :key="tool.id"
        :href="tool.url"
        target="_blank"
        rel="noopener noreferrer"
        class="tool-card"
      >
        <span class="tool-category">{{ tool.category }}</span>
        <div class="tool-name">{{ tool.name }}</div>
        <div class="tool-desc">{{ tool.description || '暂无描述' }}</div>
        <div class="tool-link">
          <span>访问链接</span>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
        </div>
      </a>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { getTools } from '../api'

const tools = ref([])
const loading = ref(true)
const gridRef = ref(null)

onMounted(async () => {
  try { const res = await getTools(); tools.value = res.data } catch {}
  loading.value = false

  await nextTick()
  if (gridRef.value) {
    new IntersectionObserver((entries) => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible') } })
    }, { threshold: 0.1 }).observe(gridRef.value)
  }
})
</script>

<style scoped>
.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
}

.tool-card {
  position: relative;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius);
  box-shadow: var(--glass-shadow);
  padding: 24px 22px 20px;
  overflow: hidden;
  cursor: pointer;
  text-decoration: none;
  color: inherit;
  transition: transform 0.35s var(--ease-out-expo), box-shadow 0.35s var(--ease-out-expo);
  display: flex;
  flex-direction: column;
}

.tool-card::before {
  content: '';
  position: absolute;
  inset: 0;
  z-index: -1;
  border-radius: inherit;
  background: linear-gradient(180deg, var(--glass-highlight) 0%, transparent 40%);
  pointer-events: none;
}

.tool-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--glass-shadow-hover);
}

.tool-category {
  display: inline-block;
  padding: 3px 10px;
  font-size: 11.5px;
  font-weight: 500;
  color: var(--primary);
  background: var(--primary-glow);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: var(--radius-full);
  margin-bottom: 10px;
  align-self: flex-start;
}

.tool-name {
  font-size: 17px;
  font-weight: 650;
  color: var(--text);
  margin-bottom: 6px;
  line-height: 1.3;
}

.tool-desc {
  font-size: 13.5px;
  color: var(--text-secondary);
  line-height: 1.6;
  flex: 1;
  margin-bottom: 12px;
}

.tool-link {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12.5px;
  color: var(--primary);
  font-weight: 500;
}

/* Responsive */
@media (max-width: 768px) {
  .tools-grid {
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 12px;
  }

  .tool-card {
    padding: 18px 16px 16px;
  }

  .tool-name {
    font-size: 15px;
  }

  .tool-desc {
    font-size: 13px;
  }
}

@media (max-width: 480px) {
  .tools-grid {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .tool-card {
    padding: 16px 14px;
  }

  .tool-category {
    font-size: 11px;
    padding: 2px 8px;
  }

  .tool-name {
    font-size: 15px;
  }

  .tool-desc {
    font-size: 12.5px;
  }
}
</style>
