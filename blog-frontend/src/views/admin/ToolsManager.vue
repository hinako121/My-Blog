<template>
  <div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">
      <h2 style="font-size:20px">工具管理</h2>
      <el-button type="primary" @click="openCreate">添加工具</el-button>
    </div>

    <el-table :data="tools" style="width:100%" v-loading="loading">
      <el-table-column prop="name" label="名称" min-width="140" />
      <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
      <el-table-column prop="category" label="分类" width="100">
        <template #default="scope">
          <el-tag size="small">{{ scope.row.category }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="url" label="链接" min-width="180" show-overflow-tooltip />
      <el-table-column label="操作" width="160">
        <template #default="scope">
          <el-button size="small" @click="openEdit(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- Dialog -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑工具' : '添加工具'" width="520px" destroy-on-close>
      <el-form :model="form" label-position="top">
        <el-form-item label="名称" required>
          <el-input v-model="form.name" placeholder="工具名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="简短描述" />
        </el-form-item>
        <el-form-item label="链接" required>
          <el-input v-model="form.url" placeholder="https://..." />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="form.category" placeholder="选择分类" style="width:100%" filterable allow-create>
            <el-option v-for="cat in categories" :key="cat" :label="cat" :value="cat" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">{{ isEdit ? '保存' : '添加' }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getTools, createTool, updateTool, deleteTool } from '../../api'
import { ElMessage, ElMessageBox } from 'element-plus'

const tools = ref([])
const loading = ref(true)
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const submitting = ref(false)
const categories = ['效率', '设计', '开发', '学习', '娱乐', '其他']

const form = reactive({ name: '', description: '', url: '', category: '其他' })

function resetForm() {
  form.name = ''; form.description = ''; form.url = ''; form.category = '其他'
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
  form.name = row.name
  form.description = row.description
  form.url = row.url
  form.category = row.category
  dialogVisible.value = true
}

async function handleSubmit() {
  if (!form.name.trim() || !form.url.trim()) {
    ElMessage.warning('请填写名称和链接')
    return
  }
  submitting.value = true
  try {
    if (isEdit.value) {
      const res = await updateTool(editId.value, form)
      const idx = tools.value.findIndex(t => t.id === editId.value)
      if (idx !== -1) tools.value[idx] = res.data
      ElMessage.success('已更新')
    } else {
      const res = await createTool(form)
      tools.value.unshift(res.data)
      ElMessage.success('已添加')
    }
    dialogVisible.value = false
  } catch { ElMessage.error('操作失败') }
  submitting.value = false
}

async function handleDelete(row) {
  await ElMessageBox.confirm(`确定删除「${row.name}」？`, '提示', { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' })
  await deleteTool(row.id)
  tools.value = tools.value.filter(t => t.id !== row.id)
  ElMessage.success('已删除')
}

onMounted(async () => {
  try { const res = await getTools(); tools.value = res.data } catch {}
  loading.value = false
})
</script>
