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
export function getMessages() { return api.get('/api/messages') }
export function createMessage(data) { return api.post('/api/messages', data) }
export function getSettings() { return api.get('/api/settings') }
export function updateSettings(data) { return api.put('/api/settings', data) }
export function uploadMedia(formData) { return api.post('/api/upload', formData) }

// Photos
export function getPhotos() { return api.get('/api/photos') }
export function createPhoto(formData) { return api.post('/api/photos', formData) }
export function updatePhoto(id, data) { return api.put(`/api/photos/${id}`, data) }
export function deletePhoto(id) { return api.delete(`/api/photos/${id}`) }

// Diaries
export function getDiaries() { return api.get('/api/diaries') }
export function createDiary(data) { return api.post('/api/diaries', data) }
export function updateDiary(id, data) { return api.put(`/api/diaries/${id}`, data) }
export function deleteDiary(id) { return api.delete(`/api/diaries/${id}`) }

// Tools
export function getTools() { return api.get('/api/tools') }
export function createTool(data) { return api.post('/api/tools', data) }
export function updateTool(id, data) { return api.put(`/api/tools/${id}`, data) }
export function deleteTool(id) { return api.delete(`/api/tools/${id}`) }
