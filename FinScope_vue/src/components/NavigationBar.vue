<template>
  <nav class="bg-gray-900 shadow-md sticky top-0 z-50">
    <div class="container mx-auto px-4 py-3 flex justify-between items-center">
      <RouterLink :to="{ name: 'main' }" class="logo-link text-2xl font-bold mr-4 transition-colors" style="color: white !important;">FinScope</RouterLink>

      <div class="hidden md:flex flex-grow justify-center items-center space-x-1 lg:space-x-2 menu-bar">
        <RouterLink to="/deposit-page" class="nav-link">예적금 비교</RouterLink>
        <RouterLink to="/commodities-price" class="nav-link">현물상품</RouterLink>
        <RouterLink :to="{ name: 'stock-search-page' }" class="nav-link">주식 정보</RouterLink>
        <RouterLink to="/bank-map" class="nav-link">은행 찾기</RouterLink>
        <RouterLink :to="{ name: 'ai-recommendations' }" class="nav-link">AI 추천</RouterLink>
        <RouterLink to="/board" class="nav-link">게시판</RouterLink>
      </div>

      <div class="hidden md:flex items-center space-x-3 ml-4"> 
        <RouterLink v-if="!isLoggedIn" to="/login"
          class="bg-primary hover:bg-primary-dark text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-150">로그인</RouterLink>
        <RouterLink v-if="!isLoggedIn" to="/signup"
          class="bg-teal-500 hover:bg-teal-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-150">회원가입</RouterLink>
        
        <RouterLink v-if="isLoggedIn" to="/my-page"
          class="bg-primary hover:bg-primary-dark text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-150">마이페이지</RouterLink>
        <button v-if="isLoggedIn" @click="handleLogout"
          class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-150">로그아웃</button>
        <!-- User nickname display removed as per request -->
      </div>

      <div class="md:hidden">
        <button @click="toggleMobileMenu" class="text-gray-300 hover:text-primary-light focus:outline-none">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
          </svg>
        </button>
      </div>
    </div>
    <!-- Mobile Menu Dropdown -->
    <div :class="[isMobileMenuOpen ? 'block' : 'hidden', 'md:hidden', 'bg-gray-800 shadow-lg py-2']">
      <RouterLink to="/deposit-page" @click="closeMobileMenu" class="mobile-nav-link">예적금 비교</RouterLink>
      <RouterLink to="/commodities-price" @click="closeMobileMenu" class="mobile-nav-link">현물상품</RouterLink>
      <RouterLink :to="{ name: 'stock-search-page' }" @click="closeMobileMenu" class="mobile-nav-link">주식 정보</RouterLink>
      <RouterLink to="/bank-map" @click="closeMobileMenu" class="mobile-nav-link">은행 찾기</RouterLink>
      <RouterLink :to="{ name: 'ai-recommendations' }" @click="closeMobileMenu" class="mobile-nav-link">AI 추천</RouterLink>
      <RouterLink to="/board" @click="closeMobileMenu" class="mobile-nav-link">게시판</RouterLink>
      <hr class="my-2 border-gray-700">
      <div v-if="!isLoggedIn">
        <RouterLink to="/login" @click="closeMobileMenu" class="mobile-nav-link">로그인</RouterLink>
        <RouterLink to="/signup" @click="closeMobileMenu" class="mobile-nav-link">회원가입</RouterLink>
      </div>
      <div v-else>
        <RouterLink to="/my-page" @click="closeMobileMenu" class="mobile-nav-link">마이페이지</RouterLink>
        <button @click="handleLogout"
          class="w-full text-left block px-6 py-2 text-sm text-red-400 hover:bg-red-700 hover:text-white transition-colors duration-150">로그아웃</button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { RouterLink } from 'vue-router';
import { useAuthStore } from '@/stores/user';
import { computed, onMounted, ref } from 'vue';

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

<style scoped>
.nav-link {
  @apply text-gray-300 font-medium text-sm px-3 py-2 rounded-md transition-colors duration-200 ease-in-out;
}

.nav-link:hover {
  @apply text-white bg-gray-700;
}

/* Exact match active link */
.router-link-exact-active {
  @apply text-white bg-primary font-semibold;
}

.mobile-nav-link {
  @apply block px-6 py-2 text-sm text-gray-300 hover:bg-gray-700 hover:text-primary-light;
}

.mobile-nav-link.router-link-exact-active {
  @apply text-primary bg-gray-700 font-semibold;
}
.logo-link.router-link-exact-active {
  @apply bg-transparent;
}
</style>
