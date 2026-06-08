<template>
  <div class="container">
    <h1 class="page-title">📷 相册</h1>

    <div v-if="loading" style="padding:10px 0;">
      <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px">
        <div v-for="i in 6" :key="i" class="skeleton" style="height:200px;"></div>
      </div>
    </div>

    <div v-else-if="!photos.length" class="empty-state">
      <div class="empty-state-icon">📸</div>
      <p class="empty-state-text">还没有照片，敬请期待...</p>
    </div>

    <div v-else class="photo-grid reveal-stagger" ref="gridRef">
      <div
        v-for="photo in photos"
        :key="photo.id"
        class="photo-card"
        @click="openLightbox(photo)"
      >
        <div class="photo-thumb">
          <img :src="photo.url" :alt="photo.title || '照片'" loading="lazy" />
        </div>
        <div class="photo-info">
          <div class="photo-title">{{ photo.title || '未命名' }}</div>
          <div class="photo-date">{{ formatDate(photo.created_at) }}</div>
        </div>
      </div>
    </div>

    <!-- Lightbox -->
    <Teleport to="body">
      <div
        v-if="lightboxVisible"
        class="lightbox-overlay"
        @click.self="closeLightbox"
      >
        <div class="lightbox-content">
          <button class="lightbox-close" @click="closeLightbox">&times;</button>
          <img :src="currentPhoto?.url" :alt="currentPhoto?.title || '照片'" />
          <div class="lightbox-caption">
            <div class="lightbox-title">{{ currentPhoto?.title || '未命名' }}</div>
            <div class="lightbox-desc" v-if="currentPhoto?.description">{{ currentPhoto.description }}</div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch, onUnmounted } from 'vue'
import { getPhotos } from '../api'

const photos = ref([])
const loading = ref(true)
const gridRef = ref(null)
const lightboxVisible = ref(false)
const currentPhoto = ref(null)

function formatDate(d) {
  return new Date(d).toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
}

function openLightbox(photo) {
  currentPhoto.value = photo
  lightboxVisible.value = true
}

function closeLightbox() {
  lightboxVisible.value = false
  currentPhoto.value = null
}

watch(lightboxVisible, (v) => {
  document.body.style.overflow = v ? 'hidden' : ''
})

function onKeydown(e) {
  if (e.key === 'Escape' && lightboxVisible.value) closeLightbox()
}

onMounted(async () => {
  document.addEventListener('keydown', onKeydown)
  try { const res = await getPhotos(); photos.value = res.data } catch {}
  loading.value = false

  await nextTick()
  if (gridRef.value) {
    new IntersectionObserver((entries) => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible') } })
    }, { threshold: 0.1 }).observe(gridRef.value)
  }
})

onUnmounted(() => {
  document.removeEventListener('keydown', onKeydown)
})
</script>

<style scoped>
.photo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px;
}

.photo-card {
  position: relative;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius);
  box-shadow: var(--glass-shadow);
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.35s var(--ease-out-expo), box-shadow 0.35s var(--ease-out-expo);
}

.photo-card::before {
  content: '';
  position: absolute;
  inset: 0;
  z-index: -1;
  border-radius: inherit;
  background: linear-gradient(180deg, var(--glass-highlight) 0%, transparent 40%);
  pointer-events: none;
}

.photo-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--glass-shadow-hover);
}

.photo-thumb {
  aspect-ratio: 4 / 3;
  overflow: hidden;
}

.photo-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s var(--ease-out-expo);
}

.photo-card:hover .photo-thumb img {
  transform: scale(1.05);
}

.photo-info {
  padding: 14px 16px;
}

.photo-title {
  font-size: 14.5px;
  font-weight: 600;
  color: var(--text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.photo-date {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 4px;
}

/* Lightbox */
.lightbox-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  animation: lbFadeIn 0.25s ease;
}

@keyframes lbFadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.lightbox-content {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
}

.lightbox-content img {
  max-width: 90vw;
  max-height: 80vh;
  border-radius: var(--radius-sm);
  box-shadow: 0 8px 48px rgba(0,0,0,0.4);
  object-fit: contain;
}

.lightbox-close {
  position: absolute;
  top: -40px;
  right: 0;
  background: none;
  border: none;
  color: #fff;
  font-size: 32px;
  cursor: pointer;
  line-height: 1;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.lightbox-close:hover { opacity: 1; }

.lightbox-caption {
  margin-top: 14px;
  text-align: center;
  color: #fff;
}

.lightbox-title {
  font-size: 17px;
  font-weight: 600;
}

.lightbox-desc {
  font-size: 13.5px;
  opacity: 0.7;
  margin-top: 4px;
}

/* Responsive */
@media (max-width: 768px) {
  .photo-grid {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 12px;
  }

  .photo-info {
    padding: 10px 12px;
  }

  .photo-title {
    font-size: 13px;
  }

  .lightbox-close {
    top: -36px;
    font-size: 28px;
  }

  .lightbox-title {
    font-size: 15px;
  }
}

@media (max-width: 480px) {
  .photo-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
  }

  .photo-info {
    padding: 8px 10px;
  }

  .photo-title {
    font-size: 12px;
  }

  .photo-date {
    font-size: 11px;
  }

  .lightbox-content img {
    max-width: 95vw;
    max-height: 70vh;
  }

  .lightbox-close {
    top: -32px;
    right: -4px;
    font-size: 26px;
  }
}
</style>
