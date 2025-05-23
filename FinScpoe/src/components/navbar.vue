<template>
  <nav class="bg-white shadow-md sticky top-0 z-50">
    <div class="container mx-auto px-4 py-3 flex justify-between items-center">
      <RouterLink :to="{ name: 'main' }" class="text-2xl font-bold text-teal-600 mr-4">FinScope</RouterLink>

      <div class="hidden md:flex flex-grow justify-center items-center space-x-1 lg:space-x-3 menu-bar">
        <RouterLink to="/deposit-page" class="text-gray-700 font-medium text-sm">예적금 비교</RouterLink>
        <RouterLink to="/commodities-price" class="text-gray-700 font-medium text-sm">현물상품</RouterLink>
        <RouterLink to="/stock-info" class="text-gray-700 font-medium text-sm">주식 정보</RouterLink>
        <RouterLink to="/bank-map" class="text-gray-700 font-medium text-sm">은행 지도</RouterLink>
        <RouterLink to="/recommend-deposit" class="text-gray-700 font-medium text-sm">추천 금융상품</RouterLink>
      </div>

      <div class="hidden md:flex items-center space-x-2 ml-4">
        <RouterLink to="/login" id="loginBtn"
          class="bg-teal-600 text-white px-4 py-2 rounded-lg hover:bg-teal-700 text-sm">로그인</RouterLink>
        <RouterLink to="/signup" id="signupBtn"
          class="border border-teal-600 text-teal-600 px-4 py-2 rounded-lg hover:bg-teal-50 text-sm">회원가입</RouterLink>
        <RouterLink to="/my-page" id="myBookmarksBtn"
          class="hidden bg-sky-500 text-white px-4 py-2 rounded-lg hover:bg-sky-600 text-sm">북마크 보기</RouterLink>
        <button id="logoutBtn"
          class="hidden bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 text-sm">로그아웃</button>
        <span id="loggedInUser" class="hidden text-sm font-medium"></span>
      </div>

      <div class="md:hidden">
        <button id="mobileMenuButton" class="text-gray-800 focus:outline-none">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"></path>
          </svg>
        </button>
      </div>
    </div>
    <div id="mobileMenu" class="md:hidden hidden bg-white shadow-lg py-2">
      <RouterLink to="/deposit-page" class="block px-6 py-2 text-sm hover:bg-teal-50">예적금 비교</RouterLink>
      <RouterLink to="/commodities-price" class="block px-6 py-2 text-sm hover:bg-teal-50">현물상품</RouterLink>
      <RouterLink to="/stock-info" class="block px-6 py-2 text-sm hover:bg-teal-50">주식 정보</RouterLink>
      <RouterLink to="/bank-map" class="block px-6 py-2 text-sm hover:bg-teal-50">은행 지도</RouterLink>
      <RouterLink to="/recommend-deposit" class="block px-6 py-2 text-sm hover:bg-teal-50">추천 금융상품</RouterLink>
      <hr class="my-2 border-gray-200">
      <div v-if="!isLoggedIn">
        <RouterLink to="/login" id="mobileLoginBtn" class="block px-6 py-2 text-sm hover:bg-teal-50">로그인</RouterLink>
        <RouterLink to="/signup" id="mobileSignupBtn" class="block px-6 py-2 text-sm hover:bg-teal-50">회원가입</RouterLink>
      </div>
      <div v-else>
        <RouterLink to="/my-page" id="mobileMyBookmarksBtn" class="hidden block px-6 py-2 text-sm hover:bg-teal-50">
          마이페이지</RouterLink>
        <button @click="useAuthStore.logout" to="/my-page" id="mobileMyBookmarksBtn"
          class="hidden block px-6 py-2 text-sm hover:bg-teal-50">로그아웃</button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/user'
const user = useAuthStore()
const isLoggedIn = user.accessToken || null
</script>
