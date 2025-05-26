<template>
  <main class="flex-grow container mx-auto px-6 py-16 flex flex-col justify-center items-center">
    <div class="bg-white p-8 rounded-lg shadow-xl w-full max-w-md border border-gray-200">
      <h1 class="text-3xl font-bold mb-6 text-center text-teal-600">로그인</h1>

      <div class="mb-6 flex flex-col space-y-3">
        <button type="button" @click="handleGoogleLogin" class="w-full flex items-center justify-center p-3 border border-gray-400 rounded-lg hover:bg-gray-50 text-sm font-medium text-gray-700">
          <svg class="social-btn-svg" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
            <path d="M1 1h22v22H1z" fill="none"/>
          </svg>
          Google로 로그인
        </button>
         <button type="button" @click="handleKakaoLogin" class="w-full flex items-center justify-center p-3 bg-[#FEE500] text-black rounded-lg hover:bg-yellow-400 text-sm font-medium border border-gray-300">
          <svg class="social-btn-svg" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2.248c-5.523 0-10 3.594-10 8.024 0 3.034 2.006 5.666 4.922 6.947.004.113.01.294.01.294l-.34 2.46s.282-.192.502-.36c.22-.17.712-.574 1.006-.81.408.07.823.128 1.244.172.306.03.615.047.928.047 5.523 0 10-3.594 10-8.024S17.523 2.248 12 2.248z" fill="#191919"></path>
          </svg>
          카카오로 로그인
        </button>
      </div>

      <div class="my-4 text-center">
        <hr class="border-gray-300">
        <span class="inline-block bg-white px-2 text-xs text-gray-500 relative -top-2.5">또는 이메일로 로그인</span>
      </div>

      <form @submit.prevent="handleLoginSubmit">
        <div class="mb-4">
          <label for="loginUsername" class="block text-sm font-medium text-gray-700 mb-1">아이디 또는 이메일</label>
          <input type="text" id="loginUsername" v-model="username" class="w-full p-3 border border-gray-400 rounded-lg focus:ring-2 focus:ring-teal-500" required>
        </div>
        <div class="mb-6">
          <label for="loginPassword" class="block text-sm font-medium text-gray-700 mb-1">비밀번호</label>
          <input type="password" id="loginPassword" v-model="password" class="w-full p-3 border border-gray-400 rounded-lg focus:ring-2 focus:ring-teal-500" required>
        </div>
        <button type="submit" class="w-full bg-teal-600 text-white py-3 rounded-lg hover:bg-teal-700 font-semibold">로그인</button>
      </form>

      <p class="text-sm text-center mt-4">
        계정이 없으신가요? <router-link to="/signup" class="text-teal-600 hover:underline">회원가입</router-link>
      </p>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router'; // Import useRoute
import { useAuthStore } from '@/stores/user';

const username = ref('');
const password = ref('');
const router = useRouter();
const route = useRoute(); // Get the current route instance
const authStore = useAuthStore();

const handleLoginSubmit = async () => {
  if (!username.value || !password.value) {
    alert('아이디와 비밀번호를 모두 입력해주세요.');
    return;
  }
  try {
    const result = await authStore.login(username.value, password.value);
    if (result.success) {
      // alert('로그인 성공!'); // Optional: remove alert for smoother UX
      const redirectPath = route.query.redirect || '/';
      router.push(redirectPath);
    } else {
      alert(result.message || '로그인에 실패했습니다. 아이디 또는 비밀번호를 확인해주세요.');
    }
  } catch (error) {
    // This catch block might be redundant if the store action already catches and returns a structured error.
    // However, it can catch unexpected errors during the store action call itself.
    console.error('Login component error:', error);
    alert('로그인 처리 중 오류가 발생했습니다.');
  }
};

const handleGoogleLogin = () => {
  // Placeholder for Google login
  console.log('Google login clicked');
  alert('Google 로그인은 현재 지원되지 않습니다.');
  // Potentially redirect to Django's Google login URL if it handles the OAuth flow
  // window.location.href = 'http://localhost:8000/api/accounts/google/login/'; 
};

const handleKakaoLogin = () => {
  // Placeholder for Kakao login
  console.log('Kakao login clicked');
  alert('카카오 로그인은 현재 지원되지 않습니다.');
};
</script>

<style scoped>
/* Using Tailwind CSS, so specific styles from login.html (Bootstrap) are not directly copied.
   The layout and appearance are achieved using Tailwind utility classes in the template. */
body { /* This will likely be handled by a global style or App.vue */
  font-family: 'Inter', sans-serif;
  background-color: #f8fafc;
}
.social-btn-svg {
  width: 20px;
  height: 20px;
  margin-right: 8px;
}
</style>
