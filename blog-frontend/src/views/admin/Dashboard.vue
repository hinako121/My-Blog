<template>
  <div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">
      <h2 style="font-size:20px">文章管理</h2>
      <el-button type="primary" @click="$router.push('/admin/editor')">写文章</el-button>
    </div>
    <el-table :data="posts" style="width:100%" v-loading="loading">
      <el-table-column prop="title" label="标题" min-width="200" />
      <el-table-column prop="created_at" label="发布时间" width="180">
        <template #default="scope">{{ formatDate(scope.row.created_at) }}</template>
      </el-table-column>
      <el-table-column label="操作" width="160">
        <template #default="scope">
          <el-button size="small" @click="$router.push(`/admin/editor/${scope.row.id}`)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getPosts, deletePost } from '../../api'
import { ElMessage, ElMessageBox } from 'element-plus'

const posts = ref([])
const loading = ref(true)
function formatDate(d) { return new Date(d).toLocaleDateString('zh-CN') }

onMounted(async () => {
  const res = await getPosts()
  posts.value = res.data
  loading.value = false
})

async function handleDelete(row) {
  await ElMessageBox.confirm(`确定删除「${row.title}」？`, '提示', { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' })
  await deletePost(row.id)
  posts.value = posts.value.filter(p => p.id !== row.id)
  ElMessage.success('已删除')
}
</script>
