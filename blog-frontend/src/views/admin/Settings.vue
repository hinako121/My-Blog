<template>
  <div>
    <h2 style="font-size:20px;margin-bottom:20px">个人设置</h2>
    <el-card style="max-width:500px">
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
  </div>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'
import { updateUser, uploadAvatar } from '../../api'
import { useUserStore } from '../../stores/user'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const form = reactive({ nickname: userStore.user?.nickname || '' })
const saving = ref(false)
const uploading = ref(false)
const fileInput = ref(null)
const avatarUrl = computed(() => userStore.user?.avatar ? userStore.user.avatar : '')

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
</script>
