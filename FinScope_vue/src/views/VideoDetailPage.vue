<template>
  <main class="container mx-auto px-4 sm:px-6 py-8 text-gray-100 bg-gray-900 min-h-screen">
    <div v-if="videoData.title" class="max-w-3xl mx-auto">
      <button @click="goBack" class="mb-4 bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg text-sm transition-colors">
        &larr; 뒤로가기
      </button>
      <h1 class="text-3xl font-bold mb-4 text-gray-100">{{ videoData.title }}</h1>
      <div class="aspect-w-16 aspect-h-9 mb-4">
        <iframe 
          :src="embedUrl" 
          title="YouTube video player" 
          frameborder="0" 
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
          allowfullscreen
          class="w-full h-full rounded-lg shadow-lg border border-gray-700"
        ></iframe>
      </div>
      <div class="bg-gray-800 p-6 rounded-lg shadow-xl border border-gray-700">
        <p class="text-lg text-gray-300 mb-1">채널: <span class="font-semibold">{{ videoData.channelTitle }}</span></p>
        <p class="text-md text-gray-400 mb-4">게시일: {{ videoData.publishedAt }}</p>
        <button 
          @click="handleVideoBookmarkInternal"
          class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg font-semibold transition-colors w-full sm:w-auto"
        >
          이 영상 북마크
        </button>
      </div>

      <!-- Video Summary Section -->
      <div class="mt-6 bg-gray-800 p-6 rounded-lg shadow-xl border border-gray-700">
        <h2 class="text-2xl font-semibold text-gray-100 mb-3">영상 요약</h2>
        <div v-if="isLoadingSummary" class="text-center text-gray-400">
          <p>요약 정보를 불러오는 중입니다...</p>
          <!-- Optional: Add a spinner/loader animation here -->
        </div>
        <div v-else-if="summaryError" class="text-red-400">
          <p>요약 정보 로딩 실패: {{ summaryError }}</p>
        </div>
        <div v-else-if="videoSummary" class="text-gray-300 whitespace-pre-wrap">
          {{ videoSummary }}
        </div>
        <div v-else class="text-gray-400">
          <p>제공된 요약 정보가 없습니다.</p>
        </div>
      </div>
    </div>
    <div v-else class="text-center py-10">
      <p class="text-xl text-gray-400">영상 정보를 불러오는 중이거나, 유효하지 않은 영상입니다.</p>
    </div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/user';
import api from '@/api/axios'; // Import api

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const videoSummary = ref('');
const isLoadingSummary = ref(false);
const summaryError = ref('');

const videoData = ref({
  id: route.params.videoId, // Get from route param
  title: route.query.title || '',
  channelTitle: route.query.channelTitle || '',
  publishedAt: route.query.publishedAt || '',
  thumbnailUrl: route.query.thumbnailUrl || '' // Though not directly used here, good to have
});

const embedUrl = computed(() => {
  if (videoData.value.id) {
    return `https://www.youtube.com/embed/${videoData.value.id}`;
  }
  return '';
});

const goBack = () => {
  router.go(-1); // Or router.push({ name: 'stock-info', query: { search: 'PREVIOUS_SEARCH_TERM_IF_AVAILABLE' }})
};

const handleVideoBookmarkInternal = async () => {
  if (!authStore.isLoggedIn) {
    alert('로그인이 필요한 기능입니다.');
    router.push({ name: 'login', query: { redirect: route.fullPath } });
    return;
  }
  if (!videoData.value || !videoData.value.id) {
    alert('북마크할 영상 정보가 없습니다.');
    return;
  }
  try {
    const bookmarkPayload = {
      video_id: videoData.value.id,
      title: videoData.value.title,
      thumbnail_url: videoData.value.thumbnailUrl, // Pass thumbnail if available
      channel_title: videoData.value.channelTitle,
      published_at: videoData.value.publishedAt 
    };
    await authStore.bookmarkVideo(bookmarkPayload);
    alert('영상이 북마크에 추가되었습니다.');
  } catch (error) {
    console.error('Error bookmarking video:', error);
    alert(error.response?.data?.detail || '영상 북마크 중 오류가 발생했습니다.');
  }
};

onMounted(() => {
  // If title is not passed via query, it means direct navigation or missing data
  if (!videoData.value.title && videoData.value.id) {
    console.warn('Video title not available from query params. Display might be incomplete.');
  }
  if (videoData.value.id) {
    fetchVideoSummary(videoData.value.id);
  } else {
    console.error('Video ID is missing, cannot fetch summary.');
    summaryError.value = '비디오 ID가 없어 요약을 불러올 수 없습니다.';
  }
});

const fetchVideoSummary = async (videoId) => {
  if (!videoId) return;
  isLoadingSummary.value = true;
  summaryError.value = '';
  videoSummary.value = '';
  try {
    // Use the correct API path as defined in Django urls.py for stocks app
    const response = await api.get(`/api/stocks/video-summary/${videoId}/`);
    videoSummary.value = response.data.summary;
  } catch (error) {
    console.error('Error fetching video summary:', error);
    summaryError.value = error.response?.data?.error || '영상 요약을 불러오는 중 오류가 발생했습니다.';
  } finally {
    isLoadingSummary.value = false;
  }
};

</script>

<style scoped>
/* Add any specific styles for VideoDetailPage if needed */
main {
  padding-top: 2rem; /* Add some padding at the top */
}
.aspect-w-16 {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 aspect ratio */
}
.aspect-w-16 iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
