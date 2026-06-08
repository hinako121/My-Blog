<template>
  <div>
    <h2 style="font-size:20px;margin-bottom:20px">个人设置</h2>

    <el-card style="max-width:500px;margin-bottom:20px">
      <template #header><span>个人信息</span></template>
      <el-form :model="form" label-width="80px">
        <el-form-item label="头像">
          <div style="display:flex;align-items:center;gap:12px">
            <el-avatar :size="60" :src="avatarUrl" />
            <input type="file" accept="image/*" ref="fileInput" style="display:none" @change="handleUpload" />
            <el-button @click="$refs.fileInput.click()" :loading="uploading">更换头像</el-button>
          </div>
        </el-form-item>
        <el-form-item label="用户名">
          <el-input :model-value="userStore.user?.username" disabled />
        </el-form-item>
        <el-form-item label="昵称">
          <el-input v-model="form.nickname" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSave" :loading="saving">保存</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- Site Settings: Background Image -->
    <el-card style="max-width:500px">
      <template #header><span>网站设置</span></template>
      <el-form label-width="100px">
        <el-form-item label="背景图片">
          <div style="display:flex;flex-direction:column;gap:12px;width:100%">
            <div v-if="bgPreview" style="width:100%;height:120px;border-radius:8px;background-size:cover;background-position:center;border:1px solid var(--border)" :style="{ backgroundImage: `url(${bgPreview})` }"></div>
            <input type="file" accept="image/*" ref="bgInput" style="display:none" @change="handleBgUpload" />
            <div style="display:flex;gap:8px">
              <el-button @click="$refs.bgInput.click()" :loading="bgUploading">{{ bgPreview ? '更换背景' : '上传背景' }}</el-button>
              <el-button v-if="bgPreview" type="danger" plain @click="handleRemoveBg">移除背景</el-button>
            </div>
          </div>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSaveBg" :loading="bgSaving">保存背景设置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted } from 'vue'
import { updateUser, uploadAvatar, getSettings, updateSettings, uploadBgImage } from '../../api'
import { useUserStore } from '../../stores/user'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const form = reactive({ nickname: userStore.user?.nickname || '' })
const saving = ref(false)
const uploading = ref(false)
const fileInput = ref(null)
const avatarUrl = computed(() => userStore.user?.avatar ? userStore.user.avatar : '')

// Background image
const bgInput = ref(null)
const bgUploading = ref(false)
const bgSaving = ref(false)
const bgPreview = ref('')
const bgFile = ref(null)
const currentBg = ref('')

onMounted(async () => {
  try {
    const res = await getSettings()
    if (res.data.background_image) {
      currentBg.value = res.data.background_image
      bgPreview.value = res.data.background_image
    }
  } catch {}
})

async function handleUpload() {
  const file = fileInput.value.files[0]
  if (!file) return
  uploading.value = true
  const fd = new FormData()
  fd.append('file', file)
  try {
    const res = await uploadAvatar(fd)
    userStore.setUser(res.data)
    ElMessage.success('头像已更新')
  } catch { ElMessage.error('上传失败') }
  uploading.value = false
}

async function handleSave() {
  saving.value = true
  try {
    const res = await updateUser({ nickname: form.nickname })
    userStore.setUser(res.data)
    ElMessage.success('已保存')
  } catch { ElMessage.error('保存失败') }
  saving.value = false
}

function handleBgUpload() {
  const file = bgInput.value.files[0]
  if (!file) return
  bgFile.value = file
  bgPreview.value = URL.createObjectURL(file)
}

async function handleSaveBg() {
  if (!bgFile.value) {
    ElMessage.info('请先选择要上传的图片')
    return
  }
  bgSaving.value = true
  const fd = new FormData()
  fd.append('file', bgFile.value)
  try {
    const uploadRes = await uploadBgImage(fd)
    const url = uploadRes.data.url
    await updateSettings({ background_image: url })
    currentBg.value = url
    document.body.style.setProperty('--bg-image', `url(${url})`)
    ElMessage.success('背景已更新')
  } catch {
    ElMessage.error('保存失败')
  }
  bgSaving.value = false
}

async function handleRemoveBg() {
  bgSaving.value = true
  try {
    await updateSettings({ background_image: '' })
    bgPreview.value = ''
    currentBg.value = ''
    bgFile.value = null
    document.body.style.setProperty('--bg-image', 'none')
    ElMessage.success('背景已移除')
  } catch {
    ElMessage.error('操作失败')
  }
  bgSaving.value = false
}
</script>
