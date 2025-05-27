<template>
  <div>
    <h1>네이버 로그인 처리 중...</h1>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

onMounted(async () => {
  const { code, state } = route.query

  if (code && state) {
    try {
      const result = await authStore.socialLogin({
        accessToken: code,
        provider: 'naver',
        state: state
      })

      if (result.success) {
        alert('네이버 계정으로 성공적으로 로그인되었습니다.')
        router.push('/')
      } else {
        alert(result.message || '네이버 로그인에 실패했습니다. 서버 응답을 확인해주세요.')
        router.push('/login')
      }
    } catch (error) {
      console.error('네이버 로그인 콜백 처리 중 오류 발생:', error)
      alert('네이버 로그인 처리 중 오류가 발생했습니다. 콘솔을 확인해주세요.')
      router.push('/login')
    }
  } else {
    alert('잘못된 접근입니다. 네이버 로그인 코드가 없습니다.')
    router.push('/login')
  }
})
</script>
