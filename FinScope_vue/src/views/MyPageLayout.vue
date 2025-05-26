<template>
  <main class="flex-grow container mx-auto px-4 sm:px-6 py-8 md:py-12">
    <h1 class="text-3xl md:text-4xl font-bold mb-8 md:mb-10 text-center text-emerald-700">
      <span class="text-green-600">{{ userProfileName }}</span>님의 프로필
    </h1>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 md:gap-8">
      <!-- Sidebar Navigation -->
      <div class="lg:col-span-1 bg-white p-6 rounded-xl shadow-xl border border-gray-200 flex flex-col justify-start">
        <h2 class="text-2xl font-semibold mb-6 text-gray-800 border-b-2 border-emerald-500 pb-3">계정 관리</h2>
        <nav class="space-y-3">
          <router-link 
            :to="{ name: 'my-page-profile' }" 
            custom 
            v-slot="{ navigate, isActive, isExactActive }">
            <button @click="navigate" :class="['w-full text-left py-3 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-opacity-50 transition duration-150 ease-in-out text-base font-medium', isExactActive ? 'bg-emerald-600 text-white' : 'bg-emerald-500 text-white hover:bg-emerald-600']">
              기본 정보 보기
            </button>
          </router-link>
          <router-link 
            :to="{ name: 'my-page-edit-profile' }" 
            custom 
            v-slot="{ navigate, isActive }">
            <button @click="navigate" :class="['w-full text-left py-3 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-opacity-50 transition duration-150 ease-in-out text-base font-medium', isActive ? 'bg-emerald-600 text-white' : 'bg-emerald-500 text-white hover:bg-emerald-600']">
              기본 정보 수정
            </button>
          </router-link>
          <router-link 
            :to="{ name: 'my-page-saved-products' }" 
            custom 
            v-slot="{ navigate, isActive }">
            <button @click="navigate" :class="['w-full text-left py-3 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-opacity-50 transition duration-150 ease-in-out text-base font-medium', isActive ? 'bg-emerald-600 text-white' : 'bg-emerald-500 text-white hover:bg-emerald-600']">
              저장한 상품
            </button>
          </router-link>
          <router-link 
            :to="{ name: 'my-page-activities' }" 
            custom 
            v-slot="{ navigate, isActive }">
            <button @click="navigate" :class="['w-full text-left py-3 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-opacity-50 transition duration-150 ease-in-out text-base font-medium', isActive ? 'bg-emerald-600 text-white' : 'bg-emerald-500 text-white hover:bg-emerald-600']">
              내가 작성한 글
            </button>
          </router-link>
        </nav>
      </div>

      <!-- Main Content Area for Child Routes -->
      <div class="lg:col-span-2 bg-white p-6 rounded-xl shadow-xl border border-gray-200 min-h-[400px]">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </div>
  </main>
</template>

<script setup>
import { computed } from 'vue';
import { useAuthStore } from '@/stores/user';
import { storeToRefs } from 'pinia';

const authStore = useAuthStore();
const { user: authUser } = storeToRefs(authStore);

const userProfileName = computed(() => authUser.value?.nickname || authUser.value?.username || '사용자');

// Styles for router-link buttons might need to be adjusted or defined in <style>
</script>

<style scoped>
/* Basic fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
