<template>
  <div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">
      <h2 style="font-size:20px">相册管理</h2>
      <el-button type="primary" @click="openCreate">上传照片</el-button>
    </div>

    <el-table :data="photos" style="width:100%" v-loading="loading">
      <el-table-column label="缩略图" width="100">
        <template #default="scope">
          <img :src="scope.row.url" style="width:60px;height:45px;object-fit:cover;border-radius:6px" />
        </template>
      </el-table-column>
      <el-table-column prop="title" label="标题" min-width="140" />
      <el-table-column prop="description" label="描述" min-width="180" show-overflow-tooltip />
      <el-table-column prop="created_at" label="上传时间" width="160">
        <template #default="scope">{{ formatDate(scope.row.created_at) }}</template>
      </el-table-column>
      <el-table-column label="操作" width="160">
        <template #default="scope">
          <el-button size="small" @click="openEdit(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- Upload Dialog -->
    <el-dialog v-model="uploadVisible" title="上传照片" width="480px" destroy-on-close>
      <el-form :model="uploadForm" label-position="top">
        <el-form-item label="选择图片" required>
          <div style="display:flex;align-items:center;gap:12px">
            <el-upload
              :auto-upload="false"
              :show-file-list="false"
              :on-change="handleFileChange"
              accept="image/*"
            >
              <el-button>选择图片</el-button>
            </el-upload>
            <span v-if="uploadFile" style="font-size:13px;color:var(--text-muted)">{{ uploadFile.name }}</span>
          </div>
          <img v-if="previewUrl" :src="previewUrl" style="width:100%;max-height:200px;object-fit:cover;border-radius:10px;margin-top:12px" />
        </el-form-item>
        <el-form-item label="标题">
          <el-input v-model="uploadForm.title" placeholder="照片标题（可选）" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="uploadForm.description" type="textarea" :rows="2" placeholder="照片描述（可选）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="uploadVisible = false">取消</el-button>
        <el-button type="primary" @click="handleUpload" :loading="submitting" :disabled="!uploadFile">上传</el-button>
      </template>
    </el-dialog>

    <!-- Edit Dialog -->
    <el-dialog v-model="editVisible" title="编辑照片" width="460px" destroy-on-close>
      <el-form :model="editForm" label-position="top">
        <el-form-item label="标题">
          <el-input v-model="editForm.title" placeholder="照片标题" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="editForm.description" type="textarea" :rows="3" placeholder="照片描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editVisible = false">取消</el-button>
        <el-button type="primary" @click="handleEditSubmit" :loading="submitting">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getPhotos, createPhoto, updatePhoto, deletePhoto } from '../../api'
import { ElMessage, ElMessageBox } from 'element-plus'

const photos = ref([])
const loading = ref(true)
const submitting = ref(false)

// Upload
const uploadVisible = ref(false)
const uploadFile = ref(null)
const previewUrl = ref('')
const uploadForm = reactive({ title: '', description: '' })

// Edit
const editVisible = ref(false)
const editId = ref(null)
const editForm = reactive({ title: '', description: '' })

function formatDate(d) {
  return new Date(d).toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' })
}

function handleFileChange(file) {
  uploadFile.value = file.raw
  previewUrl.value = URL.createObjectURL(file.raw)
}

function openCreate() {
  uploadForm.title = ''
  uploadForm.description = ''
  uploadFile.value = null
  previewUrl.value = ''
  uploadVisible.value = true
}

async function handleUpload() {
  if (!uploadFile.value) return
  submitting.value = true
  try {
    const fd = new FormData()
    fd.append('file', uploadFile.value)
    fd.append('title', uploadForm.title)
    fd.append('description', uploadForm.description)
    const res = await createPhoto(fd)
    photos.value.unshift(res.data)
    uploadVisible.value = false
    ElMessage.success('上传成功')
  } catch { ElMessage.error('上传失败') }
  submitting.value = false
}

function openEdit(row) {
  editId.value = row.id
  editForm.title = row.title
  editForm.description = row.description
  editVisible.value = true
}

async function handleEditSubmit() {
  submitting.value = true
  try {
    const res = await updatePhoto(editId.value, editForm)
    const idx = photos.value.findIndex(p => p.id === editId.value)
    if (idx !== -1) photos.value[idx] = res.data
    editVisible.value = false
    ElMessage.success('已更新')
  } catch { ElMessage.error('更新失败') }
  submitting.value = false
}

async function handleDelete(row) {
  await ElMessageBox.confirm(`确定删除「${row.title || '未命名'}」？`, '提示', { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' })
  await deletePhoto(row.id)
  photos.value = photos.value.filter(p => p.id !== row.id)
  ElMessage.success('已删除')
}

onMounted(async () => {
  try { const res = await getPhotos(); photos.value = res.data } catch {}
  loading.value = false
})
</script>
