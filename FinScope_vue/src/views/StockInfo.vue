<template>
  <main class="container mx-auto px-4 sm:px-6 py-8 text-gray-800">
    <h1 class="text-3xl font-bold mb-2 text-center">검색 결과: "<span>{{ searchQueryDisplay }}</span>"</h1>
    <div>
      <div v-if="currentView === 'stockInfo'" class="content-section">
        <div class="bg-white p-6 rounded-lg shadow-lg mb-8">
          <div class="md:col-span-2 space-y-8">
            <div class="bg-white p-6 rounded-lg shadow-lg">
              <h2 class="text-2xl font-semibold mb-4">차트</h2>
              <canvas ref="candleChart" class="w-full h-64 md:h-80"></canvas>
              <div class="mt-6 text-center">
                <button @click="handleBookmark"
                  class="bg-yellow-500 text-white px-6 py-2 rounded-lg hover:bg-yellow-600">북마크에 저장</button>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">

              <div class="bg-white p-4 rounded-lg shadow-lg h-[400px] overflow-y-auto">
                <h2 class="text-2xl font-semibold mb-4">관련 영상 목록</h2>
                <div class="space-y-4 news-scroll pr-2">
                  <p v-if="videos.length === 0" class="text-gray-500">관련 영상을 찾을 수 없습니다.</p>
                  <div v-for="video in videos" :key="video.id" class="video-list-item" @click="showVideoDetail(video)">
                    <img :src="video.thumbnailUrl || 'https://placehold.co/120x90/cccccc/E2E8F0?text=Video'"
                      :alt="video.title" class="video-thumbnail"
                      onerror="this.src='https://placehold.co/120x90/cccccc/E2E8F0?text=No+Thumb';">
                    <div class="video-info">
                      <h3>{{ video.title }}</h3>
                      <p>{{ video.channelTitle }}</p>
                      <p>게시일: {{ video.publishedAt }}</p>
                    </div>
                  </div>
                </div>
              </div>
              <div class="bg-white p-4 rounded-lg shadow-lg h-[400px] overflow-y-auto">
                <h2 class="text-2xl font-semibold mb-4">관련 뉴스</h2>
                <div class="space-y-4 news-scroll pr-2">
                  <div v-for="(news, i) in newsList" :key="i" class="py-2 border-b border-gray-200 last:border-b-0">
                    <a :href="news.url" target="_blank" rel="noopener noreferrer"
                      class="font-medium text-sm text-gray-700 hover:text-teal-600 cursor-pointer">
                      <br>
                      {{ news.title }}
                      <br>
                      {{ news.description }}
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="currentView === 'videoDetail'" class="content-section bg-white p-6 rounded-lg shadow-lg">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-2xl font-semibold text-teal-700">{{ selectedVideo.title }}</h2>
            <button @click="backToStockInfo"
              class="bg-gray-500 text-white py-2 px-4 rounded-lg hover:bg-gray-600 text-sm">목록으로</button>
          </div>
          <div class="video-detail-container mb-4">
            <iframe :src="videoPlayerUrl" title="YouTube video player" frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
              allowfullscreen></iframe>
          </div>
          <p class="text-sm text-gray-600 mb-1">채널: <span class="font-medium">{{ selectedVideo.channelTitle }}</span>
          </p>
          <p class="text-sm text-gray-600">게시일: <span class="font-medium">{{ selectedVideo.publishedAt }}</span></p>
        </div>
      </div>
    </div>
  </main>

  <!-- AI Modal (Vue 컴포넌트로 분리하거나 필요에 따라 구현) -->
  <div v-if="aiModalOpen" class="modal fixed inset-0 z-[100] flex items-center justify-center p-4">
    <div class="modal-content bg-white p-6 rounded-lg shadow-xl w-full max-w-lg overflow-y-auto">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold">AI 정보</h2>
        <button @click="aiModalOpen = false" class="text-gray-500 hover:text-gray-700 text-2xl">×</button>
      </div>
      <!-- Modal Loader and Body -->
      <div class="text-gray-700 whitespace-pre-wrap">AI 정보 내용이 여기에 표시됩니다.</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute } from 'vue-router'; // useRoute 추가
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
const currentView = ref('stockInfo')
const searchQueryDisplay = ref('')

const candleChart = ref(null)

const videos = ref([])
const newsList = ref([]) // 뉴스 목록을 반응형 상태로 선언
const selectedVideo = ref({})
const aiModalOpen = ref(false)
const YOUTUBE_API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY

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

const showVideoDetail = (video) => {
  selectedVideo.value = video;
  currentView.value = 'videoDetail';
};

const backToStockInfo = () => {
  currentView.value = 'stockInfo';
  // 비어있는 if 블록 제거
  selectedVideo.value = {};
};

const videoPlayerUrl = computed(() => {
  if (selectedVideo.value && selectedVideo.value.id) {
    return `https://www.youtube.com/embed/${selectedVideo.value.id}`
  }
  return ''
})

const handleBookmark = () => {
  alert(`'${searchQueryDisplay.value}' 북마크 저장 기능은 준비 중입니다.`)
  // 실제 북마크 로직 추가
};

async function loadChartData(searchQuery) {
  if (!searchQuery) {
    console.warn('검색어 없이 차트 데이터를 로드할 수 없습니다.');
    return null
  }
  const response = await api.get(`/api/stocks/stock-chart/${searchQuery}/`)
  return response.data
}

async function renderChart(chartData) {
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
    const month = (firstDataPointTime.getMonth() + 1).toString().padStart(2, '0')
    const day = firstDataPointTime.getDate().toString().padStart(2, '0')

    const minTime = `${year}-${month}-${day}T09:00:00`
    const maxTime = `${year}-${month}-${day}T15:30:00`

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
              unit: 'minute',
              tooltipFormat: 'yyyy-MM-dd HH:mm', // 툴팁에는 날짜와 시간 모두 표시
              displayFormats: { // 축 레이블에는 시간만 표시
                minute: 'HH:mm',
                hour: 'HH:mm'
              }
            },
            min: minTime,
            max: maxTime,
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


// URL 쿼리에서 검색어를 가져와서 데이터를 로드하는 함수
const loadDataFromQuery = async () => {
  const queryName = route.query.search;
  if (queryName) {
    searchQueryDisplay.value = queryName;
    fetchVideos(queryName);
    newsList.value = await loadNewsData(); // 뉴스 데이터는 검색어와 무관하게 로드하거나, 필요시 수정

    try {
      const chartData = await loadChartData(queryName);
      if (chartData) {
        renderChart(chartData);
      } else {
        console.error('차트 데이터를 불러오지 못했습니다.');
        // 차트 데이터가 없을 경우 기존 차트 제거 또는 플레이스홀더 표시
        const existingChart = Chart.getChart(candleChart.value);
        if (existingChart) {
          existingChart.destroy();
        }
      }
    } catch (error) {
      console.error('차트 로딩 중 오류 발생:', error);
    }
  } else {
    searchQueryDisplay.value = '검색어를 입력해주세요.';
    // 검색어가 없을 경우 기본 상태 처리 (예: 차트 숨기기, 안내 메시지 표시)
    videos.value = [];
    newsList.value = [];
    const existingChart = Chart.getChart(candleChart.value);
    if (existingChart) {
      existingChart.destroy();
    }
  }
};

onMounted(async () => {
  await loadDataFromQuery();
});

// 라우트 쿼리가 변경될 때마다 데이터 다시 로드
watch(() => route.query.search, async (newSearchQuery, oldSearchQuery) => {
  if (newSearchQuery !== oldSearchQuery) {
    await loadDataFromQuery();
  }
});

// searchQueryDisplay는 이제 URL을 통해 관리되므로, 직접적인 watch는 제거하거나 수정합니다.
// 만약 내부 검색 기능 등으로 searchQueryDisplay가 직접 변경될 경우를 대비한다면 유지할 수 있으나,
// 현재 요구사항은 URL 기반이므로 route.query.search를 watch하는 것이 더 적합합니다.
// watch(searchQueryDisplay, async (newQuery) => {
//   // 이 부분은 URL 변경에 의해 트리거되므로, 중복 호출을 피하기 위해 route.query.search watch로 대체
// });

</script>

<style scoped>
/* 기존 스타일 유지 */
body {
  /* Vue에서는 이 스타일이 전역으로 적용되도록 하거나, App.vue 등으로 옮겨야 합니다. 여기서는 일단 유지합니다. */
  font-family: 'Inter', sans-serif;
  background-color: #f8fafc;
  /* display: flex; flex-direction: column; min-height: 100vh; /* App.vue에서 관리 */
}

main {
  flex-grow: 1;
}

.hidden {
  display: none !important;
}

/* Vue의 v-show와 유사하나, v-if/v-show 사용 권장 */

.news-scroll::-webkit-scrollbar {
  width: 4px;
}

.news-scroll::-webkit-scrollbar-thumb {
  background-color: #14b8a6;
  border-radius: 20px;
}

.video-list-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  background-color: #f9fafb;
  cursor: pointer;
  transition: box-shadow 0.2s ease-in-out;
}

.video-list-item:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.video-thumbnail {
  width: 120px;
  height: 90px;
  object-fit: cover;
  border-radius: 0.375rem;
  flex-shrink: 0;
}

.video-info h3 {
  font-size: 1rem;
  font-weight: 600;
  color: #14b8a6;
  /* Tailwind teal-600 */
  margin-bottom: 0.25rem;
}

.video-info p {
  font-size: 0.75rem;
  color: #6b7280;
  /* Tailwind gray-500 */
}

.video-detail-container iframe {
  width: 100%;
  aspect-ratio: 16 / 9;
  max-height: 500px;
  border-radius: 0.5rem;
  border: 1px solid #d1d5db;
  /* Tailwind gray-3 00 */
}

.content-section {
  /* Common class for main content areas */
}

.modal {
  background-color: rgba(0, 0, 0, 0.5);
  /* Dimmed background for modal */
}
</style>
