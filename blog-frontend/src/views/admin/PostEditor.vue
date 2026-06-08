<template>
  <div>
    <h2 style="font-size:20px;margin-bottom:20px">{{ isEdit ? '编辑文章' : '写文章' }}</h2>
    <el-input v-model="form.title" placeholder="文章标题" style="margin-bottom:16px" />
    <div style="margin-bottom:16px">
      <el-input v-model="form.summary" placeholder="摘要（可选）" />
    </div>
    <div style="border:1px solid #d9d9d9;border-radius:4px;margin-bottom:16px" ref="editorRef"></div>
    <el-button type="primary" @click="handleSave" :loading="saving">保存</el-button>
    <el-button @click="$router.back()">取消</el-button>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { createPost, updatePost, getPost } from '../../api'
import { ElMessage } from 'element-plus'
import { createEditor, createToolbar } from '@wangeditor/editor'
import '@wangeditor/editor/dist/css/style.css'

const route = useRoute()
const router = useRouter()
const isEdit = !!route.params.id
const editorRef = ref(null)
const saving = ref(false)
const form = reactive({ title: '', content: '', summary: '' })

let editor = null
let toolbar = null

onMounted(async () => {
  const editorContainer = document.createElement('div')
  editorContainer.style.minHeight = '400px'
  editorRef.value.appendChild(editorContainer)

  const toolbarContainer = document.createElement('div')
  editorRef.value.prepend(toolbarContainer)

  // Configure editor with image upload
  editor = createEditor({
    selector: editorContainer,
    config: {
      placeholder: '开始写作...',
      MENU_CONF: {
        uploadImage: {
          server: '/api/upload',
          fieldName: 'file',
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token') || ''}`
          },
          // Insert image as absolute path
          customInsert(res, insertFn) {
            const url = res.url || (res.data && res.data.url)
            if (url) insertFn(url)
          },
        }
      }
    },
    mode: 'default'
  })

  toolbar = createToolbar({ editor, selector: toolbarContainer, mode: 'default' })

  if (isEdit) {
    const res = await getPost(route.params.id)
    form.title = res.data.title
    form.summary = res.data.summary
    form.content = res.data.content
    editor.setHtml(res.data.content)
  }
})

onBeforeUnmount(() => {
  if (editor) editor.destroy()
  if (toolbar) toolbar.destroy()
})

async function handleSave() {
  if (!form.title.trim()) { ElMessage.warning('请输入标题'); return }
  const data = { title: form.title, content: editor.getHtml(), summary: form.summary }
  saving.value = true
  try {
    if (isEdit) {
      await updatePost(route.params.id, data)
      ElMessage.success('已更新')
    } else {
      await createPost(data)
      ElMessage.success('已发布')
    }
    router.push('/admin')
  } catch { ElMessage.error('保存失败') }
  saving.value = false
}
</script>
