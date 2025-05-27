<template>
  <div class="bg-white text-gray-800">
    <main id="mainPage" class="pt-0">
      <div class="carousel-container" @mouseenter="pauseCarousel" @mouseleave="startCarousel">
        <div class="carousel-content-overlay" :key="currentSlide">
          <h1 class="text-4xl md:text-5xl font-bold">FinScope</h1>
          <p class="text-xl md:text-2xl mt-2">AI에 기반한 종합 금융 솔루션</p>
        </div>

        <div class="carousel-slide" v-for="(url, index) in imgUrl" :key="index"
          :class="{ active: currentSlide === index }">
          <img :src="url" :alt="`슬라이드 ${index + 1}`" />
        </div>

      </div>

      <div class="container mx-auto px-6 py-8 md:py-12">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8 items-stretch min-h-[600px];">
          <div class="info-box-container">
            <h3>실시간 환율</h3>
            <div class="info-box-content">
              <p class="text-sm">주요 통화별 현재 환율 변동을 확인하세요.</p>
              <div class="mt-4 flex-grow bg-gray-100 rounded flex items-center justify-center text-gray-400 text-sm">
                <exchangeRateChart />
              </div>
            </div>
          </div>

          <div class="info-box-container">
            <h3>실시간 현물 가격</h3>
            <div class="info-box-content">
              <p class="text-sm">금, 원유 등 주요 현물 가격 정보를 제공합니다.</p>
              <div class="mt-4 flex-grow bg-gray-100 rounded flex items-center justify-center text-gray-400 text-sm">
                <commoditiesChart />
              </div>
            </div>
          </div>

          <div class="info-box-container">
            <h2>오늘의 뉴스</h2>
            <div class="info-box-content news-scroll">
              <div v-for="news in newsList" :key="news.link" class="py-2 border-b border-gray-200 last:border-b-0">
                <router-link :to="{ name: 'news-detail', query: { url: news.link } }"
                  class="font-medium text-sm text-gray-700 hover:text-teal-600 cursor-pointer">
                  {{ news.title }}
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import commoditiesChart from '@/components/commoditiesChart.vue'
import exchangeRateChart from "@/components/exchangeRateChart.vue"


</script>

<script>
import NavigationBar from '@/components/NavigationBar.vue'
import img1 from '@/assets/images/finance_01.jpg'
import img2 from '@/assets/images/finance_02.jpg'
import img3 from '@/assets/images/finance_03.jpg'
import img4 from '@/assets/images/finance_04.jpg'
import axios from 'axios'

export default {
  components: {
    NavigationBar,
  },
  data() {
    return {
      imgUrl: [
        img1, img2, img3, img4
      ],
      currentSlide: 0,
      intervalRef: null,
      newsList: [],
    }
  },
  methods: {
    goToSlide(index) {
      this.currentSlide = index;
      this.resetCarousel();
    },
    nextSlide() {
      this.currentSlide = (this.currentSlide + 1) % this.imgUrl.length;
      console.log('Current slide:', this.currentSlide); // Add console log for debugging
    },
    startCarousel() {
      if (!this.intervalRef) {
        this.intervalRef = setInterval(this.nextSlide, 3000);
      }
    },
    pauseCarousel() {
      clearInterval(this.intervalRef);
      this.intervalRef = null;
    },
    resetCarousel() {
      this.pauseCarousel();
      this.startCarousel();
    },
    async fetchNews() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/stocks/news-list/')
        this.newsList = response.data
      }
      catch (error) {
        console.error('뉴스 api 요청 실패', error)
      }
    }
  },
  mounted() {
    this.startCarousel()
    this.fetchNews()
  },
  beforeUnmount() {
    this.pauseCarousel()
  }
}
</script>

<style scoped>
.carousel-container {
  position: relative;
  width: 100%;
  overflow: hidden;
  height: 65vh;
  /* Ensure the container has a height */
}

.carousel-slide {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  opacity: 0;
  transition: opacity 0.7s ease-in-out;
  visibility: hidden;
  /* Hide non-active slides */
}

.carousel-slide.active {
  opacity: 1;
  visibility: visible;
  /* Show active slide */
}

.carousel-slide img {
  width: 100%;
  height: 65vh;
  object-fit: cover;
  display: block;
}

.carousel-dots {
  text-align: center;
  padding: 10px 0;
  position: absolute;
  bottom: 20px;
  width: 100%;
  z-index: 15;
}

.carousel-dot {
  cursor: pointer;
  height: 10px;
  width: 10px;
  margin: 0 4px;
  background-color: rgba(255, 255, 255, 0.4);
  border-radius: 50%;
  display: inline-block;
  transition: background-color 0.3s ease;
}

.carousel-dot.active,
.carousel-dot:hover {
  background-color: rgba(255, 255, 255, 0.9);
}

.carousel-content-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 10;
  color: white;
  text-align: center;
  width: 90%;
  max-width: 800px;
  padding: 2rem;
}

.carousel-content-overlay h1,
.carousel-content-overlay p {
  animation: fadeInSlideUp 0.7s ease-out forwards;
  /* Apply animation */
}

@keyframes fadeInSlideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
