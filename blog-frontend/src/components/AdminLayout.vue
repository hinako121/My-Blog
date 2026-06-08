<template>
  <el-container style="min-height:100vh">
    <el-aside width="200px" style="background:#fff;border-right:1px solid #eee">
      <div style="padding:20px;font-size:18px;font-weight:700;border-bottom:1px solid #eee">后台管理</div>
      <el-menu router :default-active="$route.path" style="border:none">
        <el-menu-item index="/admin"><el-icon><List /></el-icon>文章列表</el-menu-item>
        <el-menu-item index="/admin/editor"><el-icon><Edit /></el-icon>写文章</el-menu-item>
        <el-menu-item index="/admin/photos"><el-icon><Picture /></el-icon>相册管理</el-menu-item>
        <el-menu-item index="/admin/diaries"><el-icon><Notebook /></el-icon>日记管理</el-menu-item>
        <el-menu-item index="/admin/tools"><el-icon><Switch /></el-icon>工具管理</el-menu-item>
        <el-menu-item index="/admin/settings"><el-icon><Setting /></el-icon>设置</el-menu-item>
      </el-menu>
      <div style="padding:12px 20px;border-top:1px solid #eee;margin-top:auto;position:absolute;bottom:0;width:200px">
        <el-button text @click="logout">退出登录</el-button>
      </div>
    </el-aside>
    <el-main style="background:#f5f5f5;padding:24px">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { List, Edit, Setting, Picture, Notebook, Switch } from '@element-plus/icons-vue'
const router = useRouter()
const userStore = useUserStore()
function logout() {
  userStore.logout()
  router.push('/admin/login')
}
</script>
