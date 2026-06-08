<template>
  <div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">
      <h2 style="font-size:20px">日记管理</h2>
      <el-button type="primary" @click="openCreate">写日记</el-button>
    </div>

    <el-table :data="diaries" style="width:100%" v-loading="loading">
      <el-table-column prop="created_at" label="日期" width="160">
        <template #default="scope">{{ formatDate(scope.row.created_at) }}</template>
      </el-table-column>
      <el-table-column prop="title" label="标题" min-width="160" />
      <el-table-column prop="mood" label="心情" width="70">
        <template #default="scope">
          <span style="font-size:22px">{{ scope.row.mood || '📝' }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="content" label="内容" min-width="200" show-overflow-tooltip />
      <el-table-column label="操作" width="160">
        <template #default="scope">
          <el-button size="small" @click="openEdit(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- Dialog -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑日记' : '写日记'" width="560px" destroy-on-close>
      <el-form :model="form" label-position="top">
        <el-form-item label="心情">
          <div style="display:flex;gap:8px;flex-wrap:wrap">
            <button
              v-for="emoji in emojis"
              :key="emoji"
              type="button"
              class="emoji-btn"
              :class="{ active: form.mood === emoji }"
              @click="form.mood = emoji"
            >{{ emoji }}</button>
          </div>
        </el-form-item>
        <el-form-item label="标题" required>
          <el-input v-model="form.title" placeholder="日记标题" />
        </el-form-item>
        <el-form-item label="内容" required>
          <el-input v-model="form.content" type="textarea" :rows="6" placeholder="今天发生了什么..." />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">{{ isEdit ? '保存' : '发布' }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getDiaries, createDiary, updateDiary, deleteDiary } from '../../api'
import { ElMessage, ElMessageBox } from 'element-plus'

const diaries = ref([])
const loading = ref(true)
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const submitting = ref(false)
const emojis = ['😊', '😢', '😡', '😴', '🎉', '😍', '😨', '🤔', '🥰', '😎', '🥳', '😤']

const form = reactive({ title: '', content: '', mood: '' })

function formatDate(d) {
  return new Date(d).toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' })
}

function resetForm() {
  form.title = ''; form.content = ''; form.mood = ''
}

function openCreate() {
  resetForm()
  isEdit.value = false
  editId.value = null
  dialogVisible.value = true
}

function openEdit(row) {
  isEdit.value = true
  editId.value = row.id
  form.title = row.title
  form.content = row.content
  form.mood = row.mood
  dialogVisible.value = true
}

async function handleSubmit() {
  if (!form.title.trim() || !form.content.trim()) {
    ElMessage.warning('请填写标题和内容')
    return
  }
  submitting.value = true
  try {
    if (isEdit.value) {
      const res = await updateDiary(editId.value, form)
      const idx = diaries.value.findIndex(d => d.id === editId.value)
      if (idx !== -1) diaries.value[idx] = res.data
      ElMessage.success('已更新')
    } else {
      const res = await createDiary(form)
      diaries.value.unshift(res.data)
      ElMessage.success('已发布')
    }
    dialogVisible.value = false
  } catch { ElMessage.error('操作失败') }
  submitting.value = false
}

async function handleDelete(row) {
  await ElMessageBox.confirm(`确定删除「${row.title}」？`, '提示', { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' })
  await deleteDiary(row.id)
  diaries.value = diaries.value.filter(d => d.id !== row.id)
  ElMessage.success('已删除')
}

onMounted(async () => {
  try { const res = await getDiaries(); diaries.value = res.data } catch {}
  loading.value = false
})
</script>

<style scoped>
.emoji-btn {
  width: 40px;
  height: 40px;
  font-size: 22px;
  border: 2px solid transparent;
  border-radius: 10px;
  background: var(--surface, #f5f5f5);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: border-color 0.2s, transform 0.15s, background 0.2s;
}

.emoji-btn:hover {
  transform: scale(1.12);
}

.emoji-btn.active {
  border-color: var(--primary, #6366f1);
  background: var(--primary-glow, rgba(99,102,241,0.15));
}
</style>
