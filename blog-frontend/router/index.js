import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/posts', name: 'PostList', component: () => import('../views/PostList.vue') },
  { path: '/posts/:id', name: 'PostDetail', component: () => import('../views/PostDetail.vue') },
  { path: '/me', name: 'Me', component: () => import('../views/Me.vue') },
  { path: '/guestbook', name: 'Guestbook', component: () => import('../views/Guestbook.vue') },
  { path: '/about', name: 'About', component: () => import('../views/About.vue') },
  { path: '/admin/login', name: 'Login', component: () => import('../views/admin/Login.vue') },
  {
    path: '/admin',
    component: () => import('../components/AdminLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', name: 'Dashboard', component: () => import('../views/admin/Dashboard.vue') },
      { path: 'editor', name: 'PostEditor', component: () => import('../views/admin/PostEditor.vue') },
      { path: 'editor/:id', name: 'EditPost', component: () => import('../views/admin/PostEditor.vue') },
      { path: 'settings', name: 'Settings', component: () => import('../views/admin/Settings.vue') },
    ]
  }
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !localStorage.getItem('token')) {
    next('/admin/login')
  } else {
    next()
  }
})

export default router
