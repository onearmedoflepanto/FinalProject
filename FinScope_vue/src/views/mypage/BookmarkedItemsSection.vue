<template>
  <div class="content-section p-6 sm:p-8">
    <h2 class="text-2xl font-bold text-primary-light mb-6 pb-3 border-b-2 border-primary-dark">북마크</h2>

    <!-- Favorite Stocks Section Removed -->
    <!-- 
    <section class="mb-10">
      <h3 class="sub-section-title-alt-dark-local mb-4">관심 주식</h3>
      <div v-if="loadingStocks" class="text-center text-gray-400 py-4">관심 주식 정보를 불러오는 중...</div>
      <div v-else-if="favoriteStocks.length === 0" class="text-gray-400 p-6 text-center bg-gray-700 rounded-md">관심 주식으로 등록된 항목이 없습니다.</div>
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="stock in favoriteStocks" :key="stock.id || stock.name" class="list-item-card-dark-local">
          <h4 class="text-lg font-semibold text-primary-light hover:text-primary mb-1">
            {{ stock.name }}
          </h4>
          <p v-if="stock.code" class="text-sm text-gray-400">종목 코드: {{ stock.code }}</p>
        </div>
      </div>
    </section>
    -->

    <!-- Bookmarked Posts Section -->
    <section class="mb-10">
      <h3 class="sub-section-title-alt-dark-local mb-4">북마크한 게시글</h3>
      <div v-if="loadingPosts" class="text-center text-gray-400 py-4">북마크한 게시글 정보를 불러오는 중...</div>
      <div v-else-if="bookmarkedPosts.length === 0" class="text-gray-400 p-6 text-center bg-gray-700 rounded-md">북마크한 게시글이 없습니다.</div>
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="post in bookmarkedPosts" :key="post.id" class="list-item-card-dark-local">
          <RouterLink :to="{ name: 'board-detail', params: { id: post.id } }">
            <div class="p-3">
              <h4 class="text-md font-semibold text-primary-light hover:text-primary mb-1 truncate" :title="post.title">
                {{ post.title }}
              </h4>
              <p class="text-xs text-gray-400">작성자: {{ post.author }}</p>
              <p class="text-xs text-gray-500">작성일: {{ new Date(post.created_at).toLocaleDateString() }}</p>
              <!-- Add more post details if available, like views or likes_count -->
            </div>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- Bookmarked Videos Section -->
    <section>
      <h3 class="sub-section-title-alt-dark-local mb-4">북마크한 영상</h3>
      <div v-if="loadingVideos" class="text-center text-gray-400 py-4">북마크한 영상 정보를 불러오는 중...</div>
      <div v-else-if="bookmarkedVideos.length === 0" class="text-gray-400 p-6 text-center bg-gray-700 rounded-md">북마크한 영상이 없습니다.</div>
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="video in bookmarkedVideos" :key="video.video_id" class="list-item-card-dark-local">
          <RouterLink :to="{ name: 'video-detail', params: { videoId: video.video_id }, query: { title: video.title, channelTitle: video.channel_title, publishedAt: video.published_at, thumbnailUrl: video.thumbnail_url } }">
            <img :src="video.thumbnail_url || 'https://placehold.co/320x180/cccccc/E2E8F0?text=Video'" 
                 :alt="video.title" 
                 class="w-full h-40 object-cover rounded-t-md mb-2"
                 onerror="this.src='https://placehold.co/320x180/cccccc/E2E8F0?text=No+Thumb';">
            <div class="p-3">
              <h4 class="text-md font-semibold text-primary-light hover:text-primary mb-1 truncate" :title="video.title">
                {{ video.title }}
              </h4>
              <p class="text-xs text-gray-400 truncate" :title="video.channel_title">채널: {{ video.channel_title }}</p>
              <p class="text-xs text-gray-500">게시일: {{ video.published_at }}</p>
            </div>
          </RouterLink>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
// import api from '@/api/axios'; // api import no longer needed if fetchFavoriteStocks is removed
import { useAuthStore } from '@/stores/user';
import { RouterLink } from 'vue-router';

const authStore = useAuthStore();
// const favoriteStocks = ref([]); // Removed
// const loadingStocks = ref(true); // Removed
const loadingVideos = ref(false); 
const loadingPosts = ref(false);

const bookmarkedVideos = computed(() => authStore.user?.bookmarked_videos || []);
const bookmarkedPosts = computed(() => authStore.user?.bookmarked_posts || []);

// fetchFavoriteStocks function removed
/*
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
*/

onMounted(() => {
  // fetchFavoriteStocks(); // Removed call
  if (!authStore.user && authStore.isLoggedIn) {
    loadingVideos.value = true;
    loadingPosts.value = true;
    authStore.loadUser().finally(() => {
      loadingVideos.value = false;
      loadingPosts.value = false;
    });
  }
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
