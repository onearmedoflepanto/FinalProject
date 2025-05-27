<template>
  <main class="container mx-auto px-4 sm:px-6 py-8 text-gray-800">
    <h1 class="text-3xl font-bold mb-2 text-center">검색 결과: <span>{{ searchQueryDisplay }}/ {{ stockCode }}</span>
    </h1>
    <div>
      <div v-if="currentView === 'stockInfo'" class="content-section">
        <div class="bg-white p-6 rounded-lg shadow-lg mb-8">
          <div class="md:col-span-2 space-y-8">
            <div class="bg-white p-6 rounded-lg shadow-lg">
              <h2 class="text-2xl font-semibold mb-4 text-center">{{ `${dayjs().format('MM월 DD일')} 5분봉 그래프` }}</h2>
              <canvas ref="candleChart" class="w-full h-64 md:h-80"></canvas>
              <div class="mt-6 text-center">
                <button @click="handleBookmark"
                  class="bg-yellow-500 text-white px-6 py-2 rounded-lg hover:bg-yellow-600">북마크에 저장</button>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">

              <div class="bg-white p-4 rounded-lg shadow-lg h-[400px] overflow-y-auto">
                <h2 class="text-2xl font-semibold mb-4 text-center">관련 영상 목록</h2>
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
                <h2 class="text-2xl font-semibold mb-4 text-center">관련 뉴스</h2>
                <div class="space-y-4 news-scroll pr-2">
                  <div v-for="(news, i) in newsList?.items" :key="i"
                    class="py-1 border-b border-gray-200 last:border-b-0">
                    <a :href="news.link" target="_blank" rel="noopener noreferrer"
                      class="font-medium text-sm text-gray-700 hover:text-teal-600 cursor-pointer">
                      <h4 class="text-center mb-1"><strong>{{ news.title }}</strong></h4>
                      <p>{{ news.description }}</p>
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
import { useRoute, useRouter } from 'vue-router'; // useRoute 추가
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
import dayjs from 'dayjs'

const route = useRoute()
const router = useRouter()
const currentView = ref('stockInfo')
const searchQueryDisplay = ref('')

const candleChart = ref(null)

const videos = ref([])
const newsList = ref([])
const selectedVideo = ref({})
const aiModalOpen = ref(false)
const YOUTUBE_API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY
const stockCode = ref('')

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
    })
    videos.value = response.data.items.map(item => ({
      id: item.id.videoId,
      title: item.snippet.title,
      channelTitle: item.snippet.channelTitle,
      publishedAt: new Date(item.snippet.publishedAt).toLocaleDateString(),
      thumbnailUrl: item.snippet.thumbnails.default.url,
    }))
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
  const query = searchQueryDisplay.value
  const response = await api.get(`/api/stocks/get-news/?q=${query}}`)
  return response.data
}

const showVideoDetail = (video) => {
  selectedVideo.value = video;
  currentView.value = 'videoDetail'
};

const backToStockInfo = () => {
  currentView.value = 'stockInfo'
  selectedVideo.value = {}
}

const videoPlayerUrl = computed(() => {
  if (selectedVideo.value && selectedVideo.value.id) {
    return `https://www.youtube.com/embed/${selectedVideo.value.id}`
  }
  return ''
})

const handleBookmark = () => {
  alert(`'${searchQueryDisplay.value}' 북마크 저장 기능은 준비 중입니다.`)
}

async function loadChartData(searchQuery) {
  if (!searchQuery) {
    console.warn('검색어 없이 차트 데이터를 로드할 수 없습니다.')
    return null
  }
  const response = await api.get(`/api/stocks/stock-chart/${searchQuery}/`)
  console.log(response)
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

    let minTime, maxTime;
    if (stockCode.value.match(/^[A-Z]/)) { // stockCode가 알파벳으로 시작하면 외국 주식
      minTime = new Date(chartData[0].x).toISOString().slice(0, 19);
      maxTime = new Date(chartData[chartData.length - 1].x).toISOString().slice(0, 19);
    } else {
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
        plugins: {
          legend: {
            display: false  // 🔥 범례 숨기기
          }
        },
        scales: {
          x: {
            type: 'time',
            time: {
              unit: 'minute',
              stepSize: 5,
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
    console.error('차트 렌더링 중 오류 발생:', error)
  }
}


const loadDataFromQuery = async () => {
  const queryName = route.query.search;
  if (queryName) {
    searchQueryDisplay.value = queryName;
    fetchVideos(queryName);
    try {
      newsList.value = await loadNewsData();
    } catch (error) {
      console.error('뉴스 로딩 중 오류 발생:', error);
      newsList.value = { items: [] };
    }

    try {
      const chartData = await loadChartData(queryName);
      if (chartData) {
        renderChart(chartData);
      } else {
        console.error('차트 데이터를 불러오지 못했습니다.');
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
    videos.value = [];
    newsList.value = [];
    const existingChart = Chart.getChart(candleChart.value);
    if (existingChart) {
      existingChart.destroy();
    }
  }
};

onMounted(async () => {
  if (!route.query.search) {
    router.push('/stock-search');
    return;
  }

  loadNewsData()
  await loadDataFromQuery();
  if (searchQueryDisplay.value && searchQueryDisplay.value !== '검색어를 입력해주세요.') {
    try {
      const response = await api.get(`/api/stocks/chart-code/${searchQueryDisplay.value}`);
      if (response.data && response.data.code && response.data.code.result && response.data.code.result.items && response.data.code.result.items.length > 0) {
        stockCode.value = response.data.code.result.items[0].code;
      } else {
        console.warn('주식 코드를 찾을 수 없거나 API 응답 형식이 다릅니다.');
        stockCode.value = ''; // 또는 적절한 기본값 설정
      }
    } catch (error) {
      console.error('주식 코드 조회 중 오류 발생:', error);
      stockCode.value = ''; // 또는 적절한 기본값 설정
    }
  } else {
    stockCode.value = ''; // 검색어가 없는 경우
  }
})

watch(() => route.query.search, async (newSearchQuery, oldSearchQuery) => {
  if (newSearchQuery !== oldSearchQuery) {
    await loadDataFromQuery()
  }
})

</script>

<style scoped>
body {
  font-family: 'Inter', sans-serif;
  background-color: #f8fafc;
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
