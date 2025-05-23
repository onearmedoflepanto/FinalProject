<template>
  <div class="bg-white text-gray-800">
    <navbar />
    <main id="mainPage" class="pt-0">
      <div class="carousel-container" @mouseenter="pauseCarousel" @mouseleave="startCarousel">
        <div class="carousel-content-overlay animate-active">
          <h1 class="text-4xl md:text-5xl font-bold">FinScope</h1>
          <p class="text-xl md:text-2xl mt-2">AI에 기반한 종합 금융 솔루션</p>
        </div>

        <div class="carousel-slide" v-for="(url, index) in imgUrl" :key="index"
          :class="{ active: currentSlide === index }">
          <img :src="url" :alt="`슬라이드 ${index + 1}`" />
        </div>

        <div class="carousel-dots">
          <span v-for="(dot, i) in imgUrl" :key="i" class="carousel-dot" :class="{ active: currentSlide === i }"
            @click="goToSlide(i)" />
        </div>
      </div>

      <div class="container mx-auto px-6 py-8 md:py-12">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8 items-stretch" style="min-height: 350px;">
          <div class="info-box-container">
            <h3>실시간 환율</h3>
            <div class="info-box-content">
              <p class="text-sm">주요 통화별 현재 환율 변동을 확인하세요.</p>
              <div class="mt-4 flex-grow bg-gray-100 rounded flex items-center justify-center text-gray-400 text-sm">
                환율 차트 영역 (Chart.js 연동 예정)
              </div>
            </div>
          </div>

          <div class="info-box-container">
            <h3>실시간 현물 가격</h3>
            <div class="info-box-content">
              <p class="text-sm">금, 원유 등 주요 현물 가격 정보를 제공합니다.</p>
              <div class="mt-4 flex-grow bg-gray-100 rounded flex items-center justify-center text-gray-400 text-sm">
                현물 가격 차트 영역 (Toss API 연동 예정)
              </div>
            </div>
          </div>

          <div class="info-box-container">
            <h2>오늘의 뉴스</h2>
            <div class="info-box-content news-scroll">
              <div v-for="(news, i) in dummyNews" :key="i" class="py-2 border-b border-gray-200 last:border-b-0">
                <h4 class="font-medium text-sm text-gray-700 hover:text-teal-600 cursor-pointer">{{ news.title }}</h4>
                <p class="text-xs text-gray-500">{{ news.source }} - {{ news.time }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import navbar from '@/components/navbar.vue'
import img1 from '@/assets/images/finance_01.jpg'
import img2 from '@/assets/images/finance_02.jpg'
import img3 from '@/assets/images/finance_03.jpg'
import img4 from '@/assets/images/finance_04.jpg'

export default {
  components: {
    navbar,
  },
  data() {
    return {
      imgUrl: [
        img1, img2, img3, img4
      ],
      currentSlide: 0,
      intervalRef: null,
      dummyNews: [
        { title: "뉴스 제목 1: 시장 동향 분석", source: "FinScope News", time: "1시간 전" },
        { title: "뉴스 제목 2: 주요 경제 지표 발표", source: "경제일보", time: "2시간 전" },
        { title: "뉴스 제목 3: 기술주 강세 전망", source: "테크 투데이", time: "3시간 전" },
        { title: "뉴스 제목 4: 국제 유가 변동", source: "글로벌 마켓", time: "4시간 전" },
        { title: "뉴스 제목 5: 새로운 투자 기회", source: "투자 인사이트", time: "5시간 전" }
      ]
    };
  },
  methods: {
    goToSlide(index) {
      this.currentSlide = index;
      this.resetCarousel();
    },
    nextSlide() {
      this.currentSlide = (this.currentSlide + 1) % this.imgUrl.length;
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
    }
  },
  mounted() {
    this.startCarousel();
  },
  beforeUnmount() {
    this.pauseCarousel();
  }
};
</script>

<style scoped>
.carousel-container {
  position: relative;
  width: 100%;
  overflow: hidden;
}

.carousel-slide {
  display: none;
  width: 100%;
  transition: opacity 0.7s ease-in-out;
}

.carousel-slide.active {
  display: block;
  opacity: 1;
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

.animate-active>h1,
.animate-active>p {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 0.7s, transform 0.7s ease-out;
}
</style>
