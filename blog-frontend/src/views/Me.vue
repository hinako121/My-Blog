<template>
  <div class="container">
    <div v-if="!loaded" style="padding: 40px 0; text-align: center;">
      <div class="skeleton" style="width: 100px; height: 100px; border-radius: 50%; margin: 0 auto 16px;"></div>
      <div class="skeleton" style="width: 160px; height: 24px; margin: 0 auto 12px;"></div>
      <div class="skeleton" style="width: 240px; height: 60px; margin: 0 auto;"></div>
    </div>

    <div v-else class="profile-card fade-in">
      <img
        :src="userStore.user?.avatar || '/img/default-avatar.svg'"
        class="profile-avatar"
        alt="avatar"
      />
      <div class="profile-name">{{ userStore.user?.nickname || '博主' }}</div>
      <div class="profile-bio">
        <p>热爱技术，热爱生活。</p>
        <p>这个博客记录了我的思考、学习和分享。</p>
        <p style="margin-top:14px;font-size:13px;color:var(--text-muted)">
          共 {{ postCount }} 篇文章
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
const loaded = ref(false)

onMounted(async () => {
  try {
    const [userPromise, postsRes] = await Promise.all([
      userStore.fetchUser(),
      getPosts()
    ])
    postCount.value = postsRes.data.length
  } catch {}
  loaded.value = true
})
</script>
