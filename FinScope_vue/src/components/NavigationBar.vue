<template>
  <nav class="bg-white shadow-md sticky top-0 z-50">
    <div class="container mx-auto px-4 py-3 flex justify-between items-center">
      <RouterLink :to="{ name: 'main' }" class="text-2xl font-bold text-teal-600 mr-4">FinScope</RouterLink>

      <div class="hidden md:flex flex-grow justify-center items-center space-x-1 lg:space-x-3 menu-bar">
        <RouterLink to="/deposit-page" class="text-gray-700 font-medium text-sm">예적금 비교</RouterLink>
        <RouterLink to="/commodities-price" class="text-gray-700 font-medium text-sm">현물상품</RouterLink>
        <RouterLink to="/stock-search" class="text-gray-700 font-medium text-sm">주식 정보</RouterLink>
        <RouterLink to="/bank-map" class="text-gray-700 font-medium text-sm">은행 찾기</RouterLink>
        <RouterLink to="/recommend-deposit" class="text-gray-700 font-medium text-sm">추천 금융상품</RouterLink>
        <RouterLink to="/board" class="text-gray-700 font-medium text-sm">게시판</RouterLink>
      </div>

      <div class="hidden md:flex items-center space-x-2 ml-4">
        <RouterLink v-if="!isLoggedIn" to="/login"
          class="bg-teal-600 text-white px-4 py-2 rounded-lg hover:bg-teal-700 text-sm">로그인</RouterLink>
        <RouterLink v-if="!isLoggedIn" to="/signup"
          class="border border-teal-600 text-teal-600 px-4 py-2 rounded-lg hover:bg-teal-50 text-sm">회원가입</RouterLink>
        <RouterLink v-if="isLoggedIn" to="/my-page"
          class="bg-sky-500 text-white px-4 py-2 rounded-lg hover:bg-sky-600 text-sm">마이페이지</RouterLink>
        <button v-if="isLoggedIn" @click="handleLogout"
          class="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 text-sm">로그아웃</button>
        <span v-if="isLoggedIn && authStore.user" class="text-sm font-medium">{{
          authStore.user.username }}</span>
      </div>

      <div class="md:hidden">
        <button @click="toggleMobileMenu" class="text-gray-800 focus:outline-none">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"></path>
          </svg>
        </button>
      </div>
    </div>
    <!-- Mobile Menu Dropdown -->
    <div :class="[isMobileMenuOpen ? 'block' : 'hidden', 'md:hidden', 'bg-white shadow-lg py-2']">
      <RouterLink to="/deposit-page" @click="closeMobileMenu"
        class="block px-6 py-2 text-sm text-gray-700 hover:bg-teal-50 hover:text-teal-600">예적금 비교
      </RouterLink>
      <RouterLink to="/commodities-price" @click="closeMobileMenu"
        class="block px-6 py-2 text-sm text-gray-700 hover:bg-teal-50 hover:text-teal-600">현물상품
      </RouterLink>
      <RouterLink to="/stock-info" @click="closeMobileMenu"
        class="block px-6 py-2 text-sm text-gray-700 hover:bg-teal-50 hover:text-teal-600">주식 정보
      </RouterLink>
      <RouterLink to="/bank-map" @click="closeMobileMenu"
        class="block px-6 py-2 text-sm text-gray-700 hover:bg-teal-50 hover:text-teal-600">은행 찾기
      </RouterLink>
      <RouterLink to="/recommend-deposit" @click="closeMobileMenu"
        class="block px-6 py-2 text-sm text-gray-700 hover:bg-teal-50 hover:text-teal-600">추천
        금융상품</RouterLink>
      <RouterLink to="/board" @click="closeMobileMenu"
        class="block px-6 py-2 text-sm text-gray-700 hover:bg-teal-50 hover:text-teal-600">게시판</RouterLink>
      <hr class="my-2 border-gray-200">
      <div v-if="!isLoggedIn">
        <RouterLink to="/login" @click="closeMobileMenu"
          class="block px-6 py-2 text-sm text-gray-700 hover:bg-teal-50 hover:text-teal-600">로그인</RouterLink>
        <RouterLink to="/signup" @click="closeMobileMenu"
          class="block px-6 py-2 text-sm text-gray-700 hover:bg-teal-50 hover:text-teal-600">회원가입</RouterLink>
      </div>
      <div v-else>
        <RouterLink to="/my-page" @click="closeMobileMenu"
          class="block px-6 py-2 text-sm text-gray-700 hover:bg-teal-50 hover:text-teal-600">
          마이페이지</RouterLink>
        <button @click="handleLogout"
          class="w-full text-left block px-6 py-2 text-sm text-gray-700 hover:bg-teal-50 hover:text-teal-600">로그아웃</button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { RouterLink } from 'vue-router';
import { useAuthStore } from '@/stores/user';
import { computed, onMounted, ref } from 'vue'; // Added ref

const authStore = useAuthStore();
const isLoggedIn = computed(() => authStore.accessToken);

const isMobileMenuOpen = ref(false);

function toggleMobileMenu() {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
}

function closeMobileMenu() {
  isMobileMenuOpen.value = false;
}

function handleLogout() {
  authStore.logout();
  closeMobileMenu();
}

onMounted(() => {
  if (isLoggedIn.value && !authStore.user) {
    authStore.loadUser();
  }
});
</script>
