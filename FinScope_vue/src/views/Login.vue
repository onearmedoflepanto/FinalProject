<template>
  <div class="bg-gray-900 min-h-screen flex flex-col items-center text-gray-100 px-6 pt-20 md:pt-24 pb-12"> 
    <main class="container mx-auto w-full max-w-md">
      <div class="bg-gray-800 p-8 rounded-lg shadow-xl border border-gray-700">
        <h1 class="text-3xl font-bold mb-8 text-center text-primary-light">로그인</h1>

        <div class="mb-8 flex flex-col space-y-4">
          <button type="button" @click="handleGoogleLogin"
            class="w-full flex items-center justify-center p-3 border border-gray-600 rounded-lg bg-gray-700 hover:bg-gray-600 text-sm font-medium text-gray-200 transition-colors">
            <svg class="social-btn-svg" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
              fill="#4285F4" />
            <path
              d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
              fill="#34A853" />
            <path
              d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
              fill="#FBBC05" />
            <path
              d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
              fill="#EA4335" />
            <path d="M1 1h22v22H1z" fill="none" />
          </svg>
          Google로 로그인
        </button>
        <button type="button" @click="handleKakaoLogin"
          class="w-full flex items-center justify-center p-3 bg-[#FEE500] text-black rounded-lg hover:bg-yellow-400 text-sm font-medium border border-gray-600 transition-colors">
          <svg class="social-btn-svg" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path
              d="M12 2.248c-5.523 0-10 3.594-10 8.024 0 3.034 2.006 5.666 4.922 6.947.004.113.01.294.01.294l-.34 2.46s.282-.192.502-.36c.22-.17.712-.574 1.006-.81.408.07.823.128 1.244.172.306.03.615.047.928.047 5.523 0 10-3.594 10-8.024S17.523 2.248 12 2.248z"
              fill="#191919"></path>
          </svg>
          카카오로 로그인
        </button>
        <button type="button" @click="handleNaverLogin"
          class="w-full flex items-center justify-center p-3 bg-[#03C75A] text-white rounded-lg hover:bg-green-600 text-sm font-medium border border-gray-600 transition-colors">
          <svg class="social-btn-svg mr-2" width="24" height="24" viewBox="0 0 64 64"
            xmlns="http://www.w3.org/2000/svg">
            <rect width="64" height="64" rx="12" fill="#03C75A" />
            <path d="M20 16h8.7l7.8 11.4h.1V16h7.4v32h-8.2l-8.3-12.1h-.1V48H20V16z" fill="#fff" />
          </svg>
          네이버로 로그인
        </button>
      </div>

      <div class="my-6 text-center">
        <hr class="border-gray-600">
        <span class="inline-block bg-gray-800 px-2 text-xs text-gray-400 relative -top-2.5">또는 이메일로 로그인</span>
      </div>

      <form @submit.prevent="handleLoginSubmit">
        <div class="mb-4">
          <label for="loginUsername" class="block text-sm font-medium text-gray-300 mb-1">이메일</label>
          <input type="text" id="loginUsername" v-model="username"
            class="w-full p-3 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-light text-gray-100 placeholder-gray-400" required>
        </div>
        <div class="mb-6">
          <label for="loginPassword" class="block text-sm font-medium text-gray-300 mb-1">비밀번호</label>
          <input type="password" id="loginPassword" v-model="password"
            class="w-full p-3 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-light text-gray-100 placeholder-gray-400" required>
        </div>
        <button type="submit"
          class="w-full bg-primary hover:bg-primary-dark text-white py-3 rounded-lg font-semibold transition-colors">로그인</button>
      </form>

      <p class="text-sm text-center mt-6 text-gray-400">
        계정이 없으신가요? <router-link to="/signup" class="text-primary-light hover:underline">회원가입</router-link>
      </p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/user'

const username = ref('')
const password = ref('')
const router = useRouter()
const authStore = useAuthStore()

const handleLoginSubmit = async () => {
  if (!username.value || !password.value) {
    alert('아이디와 비밀번호를 모두 입력해주세요.')
    return
  }
  try {
    const result = await authStore.login(username.value, password.value)
    if (result.success) {
      // alert('로그인 성공!')
      router.push('/')
    } else {
      alert(result.message || '로그인에 실패했습니다. 아이디 또는 비밀번호를 확인해주세요.')
    }
  } catch (error) {
    console.error('Login component error:', error)
    alert('로그인 처리 중 오류가 발생했습니다.')
  }
}

const handleGoogleLogin = () => {
  const redirectUri = 'http://localhost:5173/login'
  const clientId = import.meta.env.VITE_GOOGLE_LOGIN_ID
  const scope = 'profile email'
  const responseType = 'token id_token'
  const state = Math.random().toString(36).substring(7)
  const nonce = Math.random().toString(36).substring(7)
  const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?response_type=${responseType}&client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scope}&state=${state}&nonce=${nonce}` // encodeURIComponent 제거
  console.log('Generated Auth URL:', authUrl)
  window.location.href = authUrl
}

const handleKakaoLogin = () => {
  const redirectUri = 'https://kauth.kakao.com/oauth/authorize'
  const clientId = import.meta.env.VITE_KAKAO_LOGIN_SECRET

  const queryParams = new URLSearchParams({
    client_id: clientId,
    redirect_uri: 'http://localhost:5173/login',
    response_type: 'code'
  })

  window.location.href = `${redirectUri}?${queryParams.toString()}`
}

const handleNaverLogin = () => {
  const clientId = import.meta.env.VITE_NAVER_LOGIN_ID
  const redirectUri = encodeURIComponent('http://localhost:5173/login/naver/callback')
  const state = btoa(String(Math.random()))

  const authUrl = `https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=${clientId}&redirect_uri=${redirectUri}&state=${state}`
  window.location.href = authUrl
}

onMounted(async () => {
  const hashParams = new URLSearchParams(window.location.hash.substring(1));
  const queryParams = new URLSearchParams(window.location.search.substring(1));

  const googleIdToken = hashParams.has('id_token') ? hashParams.get('id_token') : null;
  const kakaoCode = queryParams.has('code') ? queryParams.get('code') : null;
  const naverCode = queryParams.has('code') && queryParams.has('state') ? queryParams.get('code') : null; // Naver는 state도 함께옴
  const naverState = queryParams.has('state') ? queryParams.get('state') : null;


  if (kakaoCode && !naverState) { // 카카오 로그인 콜백 (네이버 state가 없을 때만)
    try {
      const result = await authStore.socialLogin({
        accessToken: kakaoCode,
        provider: 'kakao',
      })

      if (result.success) {
        // alert('카카오 로그인 성공!');
        router.push('/');
      } else {
        alert(result.message || '카카오 로그인 실패!');
      }
    } catch (error) {
      console.error('카카오 로그인 에러:', error);
    }
  } else if (googleIdToken) { // 구글 로그인 콜백
    try {
      const result = await authStore.socialLogin({
        accessToken: googleIdToken,
        provider: 'google',
      })

      if (result.success) {
        // alert('구글 로그인 성공!')
        router.push('/')
      } else {
        alert(result.message || '구글 로그인 실패!')
      }
    } catch (error) {
      console.error('구글 로그인 에러:', error)
    }
  } else if (naverCode && naverState) { // 네이버 로그인 콜백
    try {
      const result = await authStore.socialLogin({
        accessToken: naverCode,
        provider: 'naver',
        state: naverState // 네이버는 state 값도 함께 전달
      });
      if (result.success) {
        // alert('네이버 로그인 성공!');
        router.push('/');
      } else {
        alert(result.message || '네이버 로그인에 실패했습니다.');
      }
    } catch (error) {
      console.error('네이버 로그인 처리 중 오류 발생:', error);
      alert('네이버 로그인 처리 중 오류가 발생했습니다.');
    }
  }
  else {
    console.warn('소셜 로그인 토큰/코드 없음')
  }
})
</script>

<style scoped>
/* body style removed as it's not appropriate here and conflicts */

.social-btn-svg {
  width: 20px;
  height: 20px;
  margin-right: 8px;
}
</style>
