<template>
  <div class="container">
    <div class="profile-card">
      <img
        :src="userStore.user?.avatar || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'"
        class="profile-avatar"
        alt="avatar"
      />
      <div class="profile-name">{{ userStore.user?.nickname || '博主' }}</div>
      <div class="profile-bio">
        <p>热爱技术，热爱生活。</p>
        <p>这个博客记录了我的思考、学习和分享。</p>
        <p style="margin-top:12px;font-size:13px;color:var(--text-muted)">
          📍 共 {{ postCount }} 篇文章
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '../stores/user'
import { getPosts } from '../api'

const userStore = useUserStore()
const postCount = ref(0)

onMounted(async () => {
  try {
    const res = await getPosts()
    postCount.value = res.data.length
  } catch {}
})
</script>
