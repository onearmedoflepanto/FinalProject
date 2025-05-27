<template>
  <main class="flex-grow container mx-auto px-4 sm:px-6 py-10 md:py-16 bg-gray-900 text-gray-100 min-h-screen">
    <h1 class="text-4xl md:text-5xl font-extrabold mb-10 md:mb-12 text-center text-primary-light">
      <span class="text-primary">{{ userProfileName }}</span>님의 프로필
    </h1>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
      <!-- Sidebar Navigation -->
      <div class="lg:col-span-3 bg-gray-800 p-6 rounded-lg shadow-xl flex flex-col">
        <h2 class="text-xl font-semibold mb-6 text-gray-200 border-b border-gray-700 pb-3">계정 관리</h2>
        <nav class="space-y-2">
          <router-link 
            :to="{ name: 'my-page-profile' }" 
            custom 
            v-slot="{ navigate, isActive, isExactActive }">
            <button @click="navigate" :class="['sidebar-button-layout', isExactActive ? 'sidebar-button-active-primary' : 'sidebar-button-inactive-dark']">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" /></svg>
              기본 정보 보기
            </button>
          </router-link>
          <router-link 
            :to="{ name: 'my-page-edit-profile' }" 
            custom 
            v-slot="{ navigate, isActive }">
            <button @click="navigate" :class="['sidebar-button-layout', isActive ? 'sidebar-button-active-primary' : 'sidebar-button-inactive-dark']">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" viewBox="0 0 20 20" fill="currentColor"><path d="M17.414 2.586a2 2 0 00-2.828 0L7 10.172V13h2.828l7.586-7.586a2 2 0 000-2.828z" /><path fill-rule="evenodd" d="M2 6a2 2 0 012-2h4a1 1 0 010 2H4v10h10v-4a1 1 0 112 0v4a2 2 0 01-2 2H4a2 2 0 01-2-2V6z" clip-rule="evenodd" /></svg>
              기본 정보 수정
            </button>
          </router-link>
          <router-link 
            :to="{ name: 'my-page-saved-products' }" 
            custom 
            v-slot="{ navigate, isActive }">
            <button @click="navigate" :class="['sidebar-button-layout', isActive ? 'sidebar-button-active-primary' : 'sidebar-button-inactive-dark']">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" viewBox="0 0 20 20" fill="currentColor"><path d="M5 4a2 2 0 012-2h6a2 2 0 012 2v14l-5-3.03L5 18V4z" /></svg>
              저장한 상품
            </button>
          </router-link>
          <router-link 
            :to="{ name: 'my-page-activities' }" 
            custom 
            v-slot="{ navigate, isActive }">
            <button @click="navigate" :class="['sidebar-button-layout', isActive ? 'sidebar-button-active-primary' : 'sidebar-button-inactive-dark']">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a1 1 0 110 2h-3a1 1 0 01-1-1v-2a1 1 0 00-1-1H9a1 1 0 00-1 1v2a1 1 0 01-1 1H5a1 1 0 110-2V4zm3 1h2v2H7V5zm2 4H7v2h2V9zm2-4h2v2h-2V5zm2 4h-2v2h2V9z" clip-rule="evenodd" /></svg>
              내가 작성한 글
            </button>
          </router-link>
          <router-link 
            :to="{ name: 'my-page-bookmarks' }" 
            custom 
            v-slot="{ navigate, isActive }">
            <button @click="navigate" :class="['sidebar-button-layout', isActive ? 'sidebar-button-active-primary' : 'sidebar-button-inactive-dark']">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" viewBox="0 0 20 20" fill="currentColor"><path d="M5 4a2 2 0 012-2h6a2 2 0 012 2v14l-5-2.5L5 18V4z" /></svg>
              북마크
            </button>
          </router-link>
          <router-link 
            :to="{ name: 'my-page-ai-saved-recommendations' }" 
            custom 
            v-slot="{ navigate, isActive }">
            <button @click="navigate" :class="['sidebar-button-layout', isActive ? 'sidebar-button-active-primary' : 'sidebar-button-inactive-dark']">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M7 2a1 1 0 00-.707 1.707L7.586 5H5a2 2 0 00-2 2v2.586l-1.293 1.293a1 1 0 000 1.414L5 13.586V16a2 2 0 002 2h.586l1.293 1.293a1 1 0 001.414 0L11.586 18H12a2 2 0 002-2v-2.586l1.293-1.293a1 1 0 000-1.414L12 9.414V7a2 2 0 00-2-2h-2.586l-1.293-1.293A1 1 0 007 2zm0 2.414L8.293 3.707a1 1 0 00.204-.125A1 1 0 019.586 3H12v2.586l.293.293a1 1 0 001.414 0L15 4.586V7h-2.586l-.293-.293a1 1 0 00-1.414 0L9.414 8H7V2.414zM5 7h2v2H5V7zm0 4h2v2H5v-2zm10-4h-2V7h2v2zm0 4h-2v2h2v-2z" clip-rule="evenodd" /></svg>
              저장된 AI 추천
            </button>
          </router-link>
        </nav>
      </div>

      <!-- Main Content Area for Child Routes -->
      <div class="lg:col-span-9 bg-gray-800 p-0 rounded-lg shadow-xl min-h-[400px]">
        <router-view v-slot="{ Component, route }">
          <transition name="fade" mode="out-in">
            <component v-if="Component" :is="Component" :key="route.path" />
          </transition>
        </router-view>
      </div>
    </div>
  </main>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/user';
import { storeToRefs } from 'pinia';

const route = useRoute();
const authStore = useAuthStore();
const { user: authUser } = storeToRefs(authStore);

const userProfileName = computed(() => authUser.value?.nickname || authUser.value?.username || '사용자');

// Styles for router-link buttons might need to be adjusted or defined in <style>
</script>

<style scoped>
/* Basic fade transition (styles can remain even if transition tag is commented out) */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Sidebar Button Styling for MyPageLayout - Dark Theme */
.sidebar-button-layout { /* Base class for layout's sidebar buttons */
  @apply w-full flex items-center text-left py-3 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:ring-opacity-50 transition duration-150 ease-in-out text-base font-medium;
}
.sidebar-button-active-primary {
  @apply bg-primary text-white shadow-md; /* Uses primary color from Tailwind config */
}
.sidebar-button-inactive-dark {
  @apply text-gray-300 hover:bg-gray-700 hover:text-primary-light;
}
.sidebar-button-layout svg { /* Ensure SVGs within these buttons also transition if needed */
  transition: transform 0.2s ease-in-out;
}
.sidebar-button-layout:hover svg {
  transform: scale(1.1);
}
</style>
