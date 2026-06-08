<template>
  <div class="login-page">
    <div class="login-card">
      <h2 class="login-title">后台登录</h2>
      <el-form ref="formRef" :model="form" :rules="rules" @submit.prevent="handleLogin">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" show-password placeholder="密码" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="loading" style="width:100%">登录</el-button>
        </el-form-item>
      </el-form>
      <div v-if="error" class="login-error">{{ error }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '../../api'
import { useUserStore } from '../../stores/user'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref(null)
const loading = ref(false)
const error = ref('')
const form = reactive({ username: '', password: '' })
const rules = { username: [{ required: true, message: '请输入用户名' }], password: [{ required: true, message: '请输入密码' }] }

async function handleLogin() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  loading.value = true; error.value = ''
  try {
    const res = await login(form)
    localStorage.setItem('token', res.data.access_token)
    await userStore.fetchUser()
    router.push('/admin')
  } catch {
    error.value = '用户名或密码错误'
  }
  loading.value = false
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e8ecf8 0%, #f0e6f6 30%, #fce4ec 60%, #e8f0f8 100%);
}
.login-page::before {
  content: '';
  position: fixed;
  inset: 0;
  background: url('/img/bg.svg') center / cover no-repeat;
  opacity: 0.5;
  z-index: 0;
}
.login-card {
  position: relative;
  z-index: 1;
  width: 380px;
  padding: 32px 28px;
  background: rgba(255, 255, 255, 0.45);
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.35);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06);
}
.login-title {
  text-align: center;
  margin-bottom: 24px;
  font-size: 20px;
  color: #1a1a2e;
}
.login-error {
  color: #f56c6c;
  text-align: center;
  font-size: 13px;
  margin-top: 8px;
}
</style>
