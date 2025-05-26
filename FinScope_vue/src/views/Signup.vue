<template>
  <main class="flex-grow container mx-auto px-6 py-16 flex flex-col justify-center items-center">
    <div class="bg-white p-8 rounded-lg shadow-xl w-full max-w-md border border-gray-200">
      <h1 class="text-3xl font-bold mb-6 text-center text-teal-600">회원가입</h1>
      
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
        <span class="inline-block bg-white px-2 text-xs text-gray-500 relative -top-2.5">또는 이메일로 가입</span>
      </div>

      <form @submit.prevent="handleSignupSubmit">
        <div class="mb-4">
          <label for="signupName" class="block text-sm font-medium text-gray-700 mb-1">이름</label>
          <input type="text" id="signupName" v-model="name" class="w-full p-3 border border-gray-400 rounded-lg focus:ring-2 focus:ring-teal-500" required>
        </div>
        <div class="mb-4">
          <label for="signupEmail" class="block text-sm font-medium text-gray-700 mb-1">이메일</label>
          <input type="email" id="signupEmail" v-model="email" class="w-full p-3 border border-gray-400 rounded-lg focus:ring-2 focus:ring-teal-500" required>
        </div>
        <div class="mb-4">
          <label for="signupPassword" class="block text-sm font-medium text-gray-700 mb-1">비밀번호</label>
          <input type="password" id="signupPassword" v-model="password" class="w-full p-3 border border-gray-400 rounded-lg focus:ring-2 focus:ring-teal-500" required>
        </div>
          <div class="mb-6">
          <label for="signupConfirmPassword" class="block text-sm font-medium text-gray-700 mb-1">비밀번호 확인</label>
          <input type="password" id="signupConfirmPassword" v-model="confirmPassword" class="w-full p-3 border border-gray-400 rounded-lg focus:ring-2 focus:ring-teal-500" required>
        </div>
        <button type="submit" class="w-full bg-teal-600 text-white py-3 rounded-lg hover:bg-teal-700 font-semibold">회원가입</button>
          <p class="text-sm text-center mt-4">
          이미 계정이 있으신가요? <router-link to="/login" class="text-teal-600 hover:underline">로그인</router-link>
        </p>
      </form>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/user';

const name = ref(''); // This will be used for 'nickname' and potentially 'username' if distinct username isn't required by backend for signup form
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const router = useRouter();
const authStore = useAuthStore();

const handleSignupSubmit = async () => {
  if (!name.value || !email.value || !password.value) {
    alert('모든 필수 정보를 입력해주세요.');
    return;
  }
  if (password.value !== confirmPassword.value) {
    alert('비밀번호가 일치하지 않습니다.');
    return;
  }
  try {
    // Assuming 'name' field maps to 'nickname' and 'username' can be derived from email or be the email itself if backend allows.
    // The Django backend sign_up view expects 'username', 'password', 'email', 'nickname'.
    // Let's use email as username for simplicity if not specified otherwise, or name if it's meant to be username.
    // For this example, let's assume 'name' is 'nickname' and 'username' is derived from email or is the email.
    // The store's signup action expects an object (formData).
    const formData = {
      username: email.value, // Or derive from name if preferred: name.value.replace(/\s+/g, '').toLowerCase()
      email: email.value,
      password: password.value,
      nickname: name.value 
    };

    const result = await authStore.signup(formData);
    
    if (result.success) {
      alert(result.message || '회원가입 성공! 로그인 페이지로 이동합니다.');
      router.push('/login'); // Redirect to login page after signup
    } else {
      alert(result.message || '회원가입에 실패했습니다. 다시 시도해주세요.');
    }
  } catch (error) {
    console.error('Signup component error:', error);
    alert('회원가입 처리 중 오류가 발생했습니다.');
  }
};

const handleGoogleLogin = () => {
  // Placeholder for Google login
  console.log('Google login clicked');
  alert('Google 로그인은 현재 지원되지 않습니다.');
  // window.location.href = '/api/accounts/google/login/'; // Or your Django Google login URL
};

const handleKakaoLogin = () => {
  // Placeholder for Kakao login
  console.log('Kakao login clicked');
  alert('카카오 로그인은 현재 지원되지 않습니다.');
};

</script>

<style scoped>
body {
  font-family: 'Inter', sans-serif;
  background-color: #f8fafc; /* 배경색 */
}
.social-btn-svg {
  width: 20px;
  height: 20px;
  margin-right: 8px;
}
/* Add other styles from SignUp.html if needed, ensuring they are scoped or global as appropriate */
</style>
