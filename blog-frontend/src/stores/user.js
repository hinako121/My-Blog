import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getUser } from '../api'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)

  async function fetchUser() {
    if (!localStorage.getItem('token')) return null
    try {
      const res = await getUser()
      user.value = res.data
      return res.data
    } catch {
      localStorage.removeItem('token')
      user.value = null
      return null
    }
  }

  function setUser(data) {
    user.value = data
  }

  function logout() {
    localStorage.removeItem('token')
    user.value = null
  }

  return { user, fetchUser, setUser, logout }
})
