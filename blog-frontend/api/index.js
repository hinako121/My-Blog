import axios from 'axios'

const api = axios.create({ baseURL: '' })

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export function login(data) { return api.post('/api/login', data) }
export function getUser() { return api.get('/api/user') }
export function updateUser(data) { return api.put('/api/user', data) }
export function uploadAvatar(formData) { return api.post('/api/user/avatar', formData) }
export function getPosts() { return api.get('/api/posts') }
export function getPost(id) { return api.get(`/api/posts/${id}`) }
export function createPost(data) { return api.post('/api/posts', data) }
export function updatePost(id, data) { return api.put(`/api/posts/${id}`, data) }
export function deletePost(id) { return api.delete(`/api/posts/${id}`) }

// Media upload
export function uploadMedia(formData) { return api.post('/api/upload', formData) }

// Site settings
export function getSettings() { return api.get('/api/settings') }
export function updateSettings(data) { return api.put('/api/settings', data) }
export function uploadBgImage(formData) { return api.post('/api/upload', formData) }

// Messages
export function getMessages() { return api.get('/api/messages') }
export function createMessage(data) { return api.post('/api/messages', data) }
