<template>
  <div class="content-section p-6 sm:p-8">
    <h2 class="text-2xl font-bold text-primary-light mb-6 pb-3 border-b-2 border-primary-dark">북마크</h2>

    <!-- Favorite Stocks Section -->
    <section class="mb-10">
      <h3 class="sub-section-title-alt-dark-local mb-4">관심 주식</h3>
      <div v-if="loadingStocks" class="text-center text-gray-400 py-4">관심 주식 정보를 불러오는 중...</div>
      <div v-else-if="favoriteStocks.length === 0" class="text-gray-400 p-6 text-center bg-gray-700 rounded-md">관심 주식으로 등록된 항목이 없습니다.</div>
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="stock in favoriteStocks" :key="stock.id || stock.name" class="list-item-card-dark-local">
          <h4 class="text-lg font-semibold text-primary-light hover:text-primary mb-1">
            <!-- Assuming a route like 'stock-detail' or similar exists. Adjust if necessary. -->
            <!-- For now, just display name. Link can be added if route exists. -->
            {{ stock.name }}
          </h4>
          <p v-if="stock.code" class="text-sm text-gray-400">종목 코드: {{ stock.code }}</p>
          <!-- Add more stock details if available and relevant -->
        </div>
      </div>
    </section>

    <!-- Bookmarked Posts Section (Placeholder) -->
    <section class="mb-10">
      <h3 class="sub-section-title-alt-dark-local mb-4">북마크한 게시글</h3>
      <div class="text-gray-400 p-6 text-center bg-gray-700 rounded-md">북마크한 게시글이 없습니다. (구현 예정)</div>
      <!-- Placeholder for bookmarked posts list -->
    </section>

    <!-- Bookmarked Videos Section (Placeholder) -->
    <section>
      <h3 class="sub-section-title-alt-dark-local mb-4">북마크한 영상</h3>
      <div class="text-gray-400 p-6 text-center bg-gray-700 rounded-md">북마크한 영상이 없습니다. (구현 예정)</div>
      <!-- Placeholder for bookmarked videos list -->
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api/axios'; // Assuming your axios instance is here
import { useAuthStore } from '@/stores/user';

const authStore = useAuthStore();
const favoriteStocks = ref([]);
const loadingStocks = ref(true);

const fetchFavoriteStocks = async () => {
  if (!authStore.isLoggedIn) {
    loadingStocks.value = false;
    return;
  }
  loadingStocks.value = true;
  try {
    const response = await api.get('/api/stocks/my_favorites/');
    favoriteStocks.value = response.data;
  } catch (error) {
    console.error('Error fetching favorite stocks:', error);
    favoriteStocks.value = []; // Clear on error
  } finally {
    loadingStocks.value = false;
  }
};

onMounted(() => {
  fetchFavoriteStocks();
});
</script>

<style scoped>
.content-section {
  animation: fadeIn 0.5s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Styles copied from UserActivitiesSection for consistency */
.list-item-card-dark-local {
  @apply bg-gray-900 p-4 rounded-lg border border-gray-700 shadow-md hover:shadow-lg transition-shadow duration-200;
}

.sub-section-title-alt-dark-local {
  @apply text-lg font-semibold text-gray-200 mb-3 pb-2 border-b border-gray-700;
}
</style>
