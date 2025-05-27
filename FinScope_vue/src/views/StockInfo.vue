<template>
  <main class="container mx-auto px-4 sm:px-6 py-8 text-gray-100 bg-gray-900"> <!-- Ensure main background is dark -->
    <!-- Results Section -->
    <div v-if="showResults && route.query.search">
      <h1 class="text-3xl font-bold mb-6 text-center text-gray-100">"<span>{{ searchQueryDisplay }}</span>" 검색 결과</h1>
      <div class="content-section"> <!-- Removed v-if="currentView === 'stockInfo'" -->
        <!-- Main content wrapper for dark theme -->
        <div class="bg-gray-800 p-6 rounded-lg shadow-xl border border-gray-700 mb-8">
          <div class="md:col-span-2 space-y-8">
            <!-- Chart Section - Dark Theme -->
            <div class="bg-gray-700 p-6 rounded-lg shadow-lg">
              <div class="flex justify-between items-center mb-4">
                <h2 class="text-2xl font-semibold text-gray-100">차트</h2>
                <div class="space-x-2">
                  <button @click="changePeriod('1d')" :class="['px-3 py-1 text-sm rounded', selectedPeriod === '1d' ? 'bg-primary text-white' : 'bg-gray-600 text-gray-300 hover:bg-gray-500']">일</button>
                  <button @click="changePeriod('1m')" :class="['px-3 py-1 text-sm rounded', selectedPeriod === '1m' ? 'bg-primary text-white' : 'bg-gray-600 text-gray-300 hover:bg-gray-500']">개월</button>
                  <button @click="changePeriod('1y')" :class="['px-3 py-1 text-sm rounded', selectedPeriod === '1y' ? 'bg-primary text-white' : 'bg-gray-600 text-gray-300 hover:bg-gray-500']">연</button>
                </div>
              </div>
              <canvas ref="candleChart" class="w-full h-64 md:h-80"></canvas> <!-- Chart.js handles canvas bg, ensure ticks/labels are light -->
              <!-- Stock Bookmark button removed -->
              <!-- 
              <div class="mt-6 text-center">
                <button @click="handleBookmark"
                  :class="[isStockFavorite ? 'bg-red-600 hover:bg-red-700' : 'bg-yellow-600 hover:bg-yellow-700', 'text-white px-6 py-2 rounded-lg transition-colors']">
                  {{ isStockFavorite ? '북마크 해제' : '북마크에 저장' }}
                </button>
              </div>
              -->
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
              <!-- Videos Section - Dark Theme -->
              <div class="bg-gray-700 p-4 rounded-lg shadow-lg h-[400px] overflow-y-auto">
                <h2 class="text-2xl font-semibold mb-4 text-gray-100">관련 영상 목록</h2>
                <div class="space-y-4 news-scroll pr-2">
                  <p v-if="videos.length === 0" class="text-gray-400">관련 영상을 찾을 수 없습니다.</p>
                  <div v-for="video in videos" :key="video.id" class="video-list-item dark-video-list-item" @click="navigateToVideoDetail(video)">
                    <img :src="video.thumbnailUrl || 'https://placehold.co/120x90/cccccc/E2E8F0?text=Video'"
                      :alt="video.title" class="video-thumbnail"
                      onerror="this.src='https://placehold.co/120x90/cccccc/E2E8F0?text=No+Thumb';">
                    <div class="video-info">
                      <h3 class="text-gray-100 font-semibold mb-1">{{ video.title }}</h3>
                      <p class="text-gray-400 text-xs">{{ video.channelTitle }}</p>
                      <p class="text-gray-400 text-xs">게시일: {{ video.publishedAt }}</p>
                    </div>
                  </div>
                </div>
              </div>
              <!-- News Section - Dark Theme -->
              <div class="bg-gray-700 p-4 rounded-lg shadow-lg h-[400px] overflow-y-auto">
                <h2 class="text-2xl font-semibold mb-4 text-gray-100">관련 뉴스</h2>
                <div class="space-y-4 news-scroll pr-2">
                  <div v-for="(news, i) in newsList" :key="i" class="py-2 border-b border-gray-600 last:border-b-0">
                    <RouterLink :to="{ name: 'news-detail', query: { url: news.link, title: news.title, description: news.description } }"
                      class="font-medium text-sm text-gray-100 hover:text-gray-300 cursor-pointer">
                      <br>
                      {{ news.title }}
                      <br>
                      {{ news.description }}
                    </RouterLink>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- In-page Video Detail Section is removed -->
      </div>
    </div>
  </main>

  <!-- AI Modal (Vue 컴포넌트로 분리하거나 필요에 따라 구현) -->
  <!-- Ensure Modal also fits dark theme if it's part of this page's redesign scope -->
  <div v-if="aiModalOpen" class="modal fixed inset-0 z-[100] flex items-center justify-center p-4">
    <div class="modal-content bg-gray-800 border border-gray-700 p-6 rounded-lg shadow-xl w-full max-w-lg overflow-y-auto">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold text-gray-100">AI 정보</h2>
        <button @click="aiModalOpen = false" class="text-gray-300 hover:text-gray-100 text-2xl">×</button>
      </div>
      <div class="text-gray-300 whitespace-pre-wrap">AI 정보 내용이 여기에 표시됩니다.</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router'; // Import useRouter
import { useAuthStore } from '@/stores/user'; // Import authStore for bookmarking
import {
  Chart,
  TimeScale,
  LinearScale,
  Tooltip,
  Title
} from 'chart.js'
import { CandlestickController, CandlestickElement } from 'chartjs-chart-financial';
import 'chartjs-adapter-date-fns'
import axios from 'axios'
import api from '@/api/axios'

const route = useRoute()
const router = useRouter(); // Initialize useRouter
// currentView is removed
const searchQueryDisplay = ref('')
const showResults = ref(false)
const selectedPeriod = ref('1d') // Default to 1 day (intraday)

const candleChart = ref(null)

const videos = ref([])
const newsList = ref([]) // 뉴스 목록을 반응형 상태로 선언
// selectedVideo is removed
const aiModalOpen = ref(false)
const YOUTUBE_API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY
const authStore = useAuthStore(); 

// const isStockFavorite = ref(false); // Removed for stock bookmark removal
// const stockNameForBookmark = ref(''); // Removed for stock bookmark removal

Chart.register(TimeScale, LinearScale, Tooltip, Title, CandlestickController, CandlestickElement)



const fetchVideos = async (query) => {
  if (!query || !YOUTUBE_API_KEY) {
    videos.value = []
    return
  }
  try {
    const response = await axios.get('https://www.googleapis.com/youtube/v3/search', {
      params: {
        part: 'snippet',
        q: query + ' 주식',
        key: YOUTUBE_API_KEY,
        maxResults: 5,
        type: 'video',
      },
    });
    videos.value = response.data.items.map(item => ({
      id: item.id.videoId,
      title: item.snippet.title,
      channelTitle: item.snippet.channelTitle,
      publishedAt: new Date(item.snippet.publishedAt).toLocaleDateString(),
      thumbnailUrl: item.snippet.thumbnails.default.url,
    }));
  } catch (error) {
    console.error('Error fetching videos from YouTube:', error)
    videos.value = []
    if (error.response && error.response.data && error.response.data.error) {
      const youtubeError = error.response.data.error
      console.error('YouTube API Error Details:', youtubeError.message)
      if (youtubeError.errors && youtubeError.errors.length > 0) {
        alert(`YouTube API 오류: ${youtubeError.errors[0].reason}. API 키 할당량 또는 설정을 확인하세요.`)
      }
    } else {
      alert('YouTube 영상을 불러오는 중 오류가 발생했습니다.')
    }
  }
};

const loadNewsData = async function () {
  const response = await api.get('/api/stocks/news-list/')
  return response.data
}

// showVideoDetail, backToStockInfo, videoPlayerUrl are removed

const navigateToVideoDetail = (video) => {
  router.push({ 
    name: 'video-detail', 
    params: { videoId: video.id },
    query: { 
      title: video.title, 
      channelTitle: video.channelTitle, 
      publishedAt: video.publishedAt,
      thumbnailUrl: video.thumbnailUrl 
    }
  });
};

// fetchStockFavoriteStatus function removed
// handleBookmark function removed (or commented out if preferred)

/*
const handleBookmark = async () => { 
  // This function is now disabled
  alert('주식 북마크 기능이 현재 비활성화되어 있습니다.');
};
*/

const handleVideoBookmark = async (video) => {
  if (!authStore.isLoggedIn) {
    alert('로그인이 필요한 기능입니다.');
    // Optionally, redirect to login: router.push({ name: 'login', query: { redirect: route.fullPath } });
    return;
  }
  if (!video || !video.id) {
    alert('북마크할 영상 정보가 없습니다.');
    return;
  }
  try {
    const videoData = {
      video_id: video.id,
      title: video.title,
      thumbnail_url: video.thumbnailUrl,
      channel_title: video.channelTitle,
      published_at: video.publishedAt // Ensure this is a string as expected by backend
    };
    await authStore.bookmarkVideo(videoData); // This action needs to be created in the store
    alert('영상이 북마크에 추가되었습니다.');
  } catch (error) {
    console.error('Error bookmarking video:', error);
    alert(error.response?.data?.detail || '영상 북마크 중 오류가 발생했습니다.');
  }
};

async function loadChartData(searchQuery, period = '1d') { // Added period parameter
  if (!searchQuery) {
    console.warn('검색어 없이 차트 데이터를 로드할 수 없습니다.');
    return null
  }
  // Pass the period to the API
  const response = await api.get(`/api/stocks/stock-chart/${searchQuery}/`, { params: { period } })
  return response.data
}

async function renderChart(chartData, period = '1d') { // Added period parameter
  if (!candleChart.value) {
    console.error('차트 컨텍스트가 준비되지 않았습니다.')
    return;
  }
  if (!chartData || chartData.length === 0) {
    console.warn('차트 데이터가 비어있어 차트를 렌더링하지 않습니다.')
    const existingChart = Chart.getChart(candleChart.value)
    if (existingChart) {
      existingChart.destroy()
    }
    return
  }

  try {
    const existingChart = Chart.getChart(candleChart.value)
    if (existingChart) {
      existingChart.destroy()
    }

    const firstDataPointTime = new Date(chartData[0].x)

    if (isNaN(firstDataPointTime.getTime())) {
      console.error('첫 번째 데이터 포인트의 시간(x) 형식이 유효하지 않습니다.')
      return;
    }

    const year = firstDataPointTime.getFullYear();
    const month = (firstDataPointTime.getMonth() + 1).toString().padStart(2, '0');
    const day = firstDataPointTime.getDate().toString().padStart(2, '0');

    let minTime, maxTime, timeUnit, tooltipFormat, displayFormats;

    if (period === '1m') {
      timeUnit = 'day';
      tooltipFormat = 'yyyy-MM-dd';
      displayFormats = { day: 'MM-dd' };
      // Let Chart.js auto-scale min/max for '1m' by leaving minTime/maxTime undefined for scales.x.min/max
    } else if (period === '1y') {
      timeUnit = 'month'; // Or 'day' if more granularity is desired for 1 year
      tooltipFormat = 'yyyy-MM';
      displayFormats = { month: 'yyyy-MM' };
      // Let Chart.js auto-scale min/max for '1y'
    } else { // Default to '1d' (intraday)
      timeUnit = 'minute';
      tooltipFormat = 'yyyy-MM-dd HH:mm';
      displayFormats = { minute: 'HH:mm', hour: 'HH:mm' };
      minTime = `${year}-${month}-${day}T09:00:00`;
      maxTime = `${year}-${month}-${day}T15:30:00`;
    }

    new Chart(candleChart.value, {
      type: 'candlestick',
      data: {
        datasets: [{
          label: '주식 차트',
          data: chartData, // loadChartData에서 반환된 데이터 사용
        }]
      },
      options: {
        scales: {
          x: {
            type: 'time',
            time: {
              unit: timeUnit,
              tooltipFormat: tooltipFormat,
              displayFormats: displayFormats
            },
            // For '1m' and '1y', let Chart.js determine min/max from data unless specific range is needed
            min: (period === '1m' || period === '1y') ? undefined : minTime,
            max: (period === '1m' || period === '1y') ? undefined : maxTime,
          },
          y: {
            beginAtZero: false
          }
        }
      }
    });
  } catch (error) {
    console.error('차트 렌더링 중 오류 발생:', error);
  }
}


// Function to fetch and display data based on a search term
const fetchDataForQuery = async (query) => {
  // stockNameForBookmark.value = query; // Removed
  if (!query) {
    searchQueryDisplay.value = '검색어를 입력해주세요.';
    videos.value = [];
    newsList.value = [];
    const existingChart = Chart.getChart(candleChart.value);
    if (existingChart) existingChart.destroy();
    showResults.value = false;
    return;
  }

  searchQueryDisplay.value = query;
  fetchVideos(query);
  newsList.value = await loadNewsData();
  // if (authStore.isLoggedIn) { // Removed call to fetchStockFavoriteStatus
  //   fetchStockFavoriteStatus(query); 
  // } else {
  //   isStockFavorite.value = false;
  // }

  try {
    const chartData = await loadChartData(query, selectedPeriod.value); // Pass selectedPeriod
    showResults.value = true;
    await nextTick();

    if (chartData) {
      renderChart(chartData, selectedPeriod.value); // Pass selectedPeriod
    } else {
      console.error('차트 데이터를 불러오지 못했습니다.');
      const existingChart = Chart.getChart(candleChart.value);
      if (existingChart) existingChart.destroy();
    }
  } catch (error) {
    console.error('데이터 로딩 중 오류 발생:', error);
    showResults.value = false;
    await nextTick();
    const existingChart = Chart.getChart(candleChart.value);
    if (existingChart) existingChart.destroy();
  }
};

const changePeriod = async (newPeriod) => {
  selectedPeriod.value = newPeriod;
  if (route.query.search) {
    await fetchDataForQuery(route.query.search); // Re-fetch data with new period
  }
};

onMounted(async () => {
  if (route.query.search) {
    await fetchDataForQuery(route.query.search);
  } else {
    searchQueryDisplay.value = '표시할 검색어가 없습니다.';
    showResults.value = false;
  }
});

watch(() => route.query.search, async (newSearchQuery, oldSearchQuery) => {
  if (newSearchQuery && newSearchQuery !== oldSearchQuery) {
    // Reset period to default when search query changes, or keep current? For now, keep.
    // selectedPeriod.value = '1d'; 
    await fetchDataForQuery(newSearchQuery);
  } else if (!newSearchQuery) {
    searchQueryDisplay.value = '표시할 검색어가 없습니다.';
    showResults.value = false;
    videos.value = [];
    newsList.value = [];
    const existingChart = Chart.getChart(candleChart.value);
    if (existingChart) existingChart.destroy();
  }
}, { immediate: false });

// searchQueryDisplay는 이제 URL을 통해 관리되므로, 직접적인 watch는 제거하거나 수정합니다.
// 만약 내부 검색 기능 등으로 searchQueryDisplay가 직접 변경될 경우를 대비한다면 유지할 수 있으나,
// 현재 요구사항은 URL 기반이므로 route.query.search를 watch하는 것이 더 적합합니다.
// watch(searchQueryDisplay, async (newQuery) => {
//   // 이 부분은 URL 변경에 의해 트리거되므로, 중복 호출을 피하기 위해 route.query.search watch로 대체
// });

</script>

<style scoped>
.dark-video-list-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #4b5563; /* border-gray-600 */
  border-radius: 0.5rem;
  background-color: #374151; /* bg-gray-700 */
  cursor: pointer;
  transition: background-color 0.2s ease-in-out;
}

.dark-video-list-item:hover {
  background-color: #4b5563; /* bg-gray-600 */
}

.video-thumbnail {
  width: 120px;
  height: 90px;
  object-fit: cover;
  border-radius: 0.375rem;
  flex-shrink: 0;
}

/* .dark-video-title and .dark-video-meta classes are removed as styles are applied directly now */

/* Ensure main tag takes full height if needed, or App.vue handles it */
main.bg-gray-900 {
  min-height: calc(100vh - theme('spacing.headerHeight', '0px')); /* Assuming header height is managed */
}


/* Original styles that might still be relevant or need adjustment */
body {
  font-family: 'Inter', sans-serif;
  /* background-color is now on main for this page */
}

main {
  flex-grow: 1;
}

.hidden {
  display: none !important;
}

.news-scroll::-webkit-scrollbar {
  width: 4px;
}

.news-scroll::-webkit-scrollbar-thumb {
  background-color: #14b8a6; /* teal-500, might need adjustment for dark theme */
  border-radius: 20px;
}

.video-detail-container iframe {
  width: 100%;
  aspect-ratio: 16 / 9;
  max-height: 500px;
  border-radius: 0.5rem;
  border: 1px solid #4b5563; /* Changed to border-gray-600 equivalent for dark theme */
}

.content-section {
  /* Common class for main content areas */
}

.modal {
  background-color: rgba(0, 0, 0, 0.5);
  /* Dimmed background for modal */
}
</style>
