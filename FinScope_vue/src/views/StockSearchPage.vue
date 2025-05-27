<template>
  <main class="container mx-auto px-4 sm:px-6 py-8 text-gray-100 flex flex-col items-center justify-center min-h-[calc(100vh-150px)]">
    <div class="w-full max-w-xl text-center">
      <h1 class="text-4xl font-bold mb-8 text-gray-100">주식 정보 검색</h1>
      <div class="flex">
        <input 
          type="text" 
          v-model="searchQuery" 
          @keyup.enter="performSearch"
          placeholder="회사명을 입력하세요..."
          class="w-full p-4 border border-gray-600 rounded-l-lg focus:ring-2 focus:ring-primary-light focus:border-transparent outline-none bg-gray-700 text-gray-100 placeholder-gray-400 text-lg"
        />
        <button 
          @click="performSearch"
          class="bg-primary hover:bg-primary-dark text-white px-4 py-4 rounded-r-lg font-semibold transition-colors text-lg whitespace-nowrap"
        >
          검색
        </button>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const searchQuery = ref('');
const router = useRouter();

const performSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({ name: 'stock-info', query: { search: searchQuery.value.trim() } });
  }
};
</script>

<style scoped>
/* Styles for the search page, can be adjusted as needed */
main {
  background-color: #111827; /* bg-gray-900 */
}
</style>
