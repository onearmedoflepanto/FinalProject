<template>
  <div class="bg-gray-900 text-gray-100">
    <main id="mainPage" class="pt-0">
      <!-- Hero Section (Carousel) -->
      <section id="hero" class="carousel-container" @mouseenter="pauseCarousel" @mouseleave="startCarousel">
        <div class="carousel-content-overlay">
          <h1 class="text-4xl md:text-6xl font-bold text-white">FinScope</h1>
          <p class="text-xl md:text-3xl mt-4 text-gray-300">AI에 기반한 종합 금융 솔루션</p>
        </div>
        <div v-for="(image, index) in imgUrl" :key="image.id || index"
             class="carousel-slide"
             :class="{ 'active': index === currentSlide, 'prev': index === previousSlide }">
          <img :src="image.src || image" :alt="image.alt || `Slide ${index + 1}`" />
        </div>
      </section>

      <!-- Sticky Secondary Navigation -->
      <nav id="secondary-nav" class="sticky top-16 bg-gray-800 shadow-md z-40 py-3 hidden md:block">
        <div class="container mx-auto flex justify-center space-x-1 sm:space-x-2 md:space-x-3 lg:space-x-4">
          <a href="#introduction" @click.prevent="smoothScrollTo('#introduction')" 
             :class="['px-3 sm:px-4 py-2 rounded-full text-xs sm:text-sm font-medium transition-colors duration-200 ease-in-out', activeSection === 'introduction' ? 'bg-primary text-white font-bold' : 'text-gray-300 hover:text-white']">소개</a>
          <a href="#features" @click.prevent="smoothScrollTo('#features')" 
             :class="['px-3 sm:px-4 py-2 rounded-full text-xs sm:text-sm font-medium transition-colors duration-200 ease-in-out', activeSection === 'features' ? 'bg-primary text-white font-bold' : 'text-gray-300 hover:text-white']">주요 기능</a>
          <a href="#financial-products" @click.prevent="smoothScrollTo('#financial-products')" 
             :class="['px-3 sm:px-4 py-2 rounded-full text-xs sm:text-sm font-medium transition-colors duration-200 ease-in-out', activeSection === 'financial-products' ? 'bg-primary text-white font-bold' : 'text-gray-300 hover:text-white']">금융 상품</a>
          <a href="#investment-info" @click.prevent="smoothScrollTo('#investment-info')" 
             :class="['px-3 sm:px-4 py-2 rounded-full text-xs sm:text-sm font-medium transition-colors duration-200 ease-in-out', activeSection === 'investment-info' ? 'bg-primary text-white font-bold' : 'text-gray-300 hover:text-white']">투자 정보</a>
          <a href="#community" @click.prevent="smoothScrollTo('#community')" 
             :class="['px-3 sm:px-4 py-2 rounded-full text-xs sm:text-sm font-medium transition-colors duration-200 ease-in-out', activeSection === 'community' ? 'bg-primary text-white font-bold' : 'text-gray-300 hover:text-white']">커뮤니티</a>
          <a href="#latest-info" @click.prevent="smoothScrollTo('#latest-info')" 
             :class="['px-3 sm:px-4 py-2 rounded-full text-xs sm:text-sm font-medium transition-colors duration-200 ease-in-out', activeSection === 'latest-info' ? 'bg-primary text-white font-bold' : 'text-gray-300 hover:text-white']">최신 뉴스</a>
        </div>
      </nav>

      <!-- Introduction Section -->
      <section id="introduction" class="py-16 md:py-24 bg-gray-900">
        <div class="container mx-auto px-6 text-center">
          <h2 class="text-3xl md:text-4xl font-bold text-primary-light mb-6">FinScope에 오신 것을 환영합니다</h2>
          <p class="text-lg md:text-xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
            FinScope는 AI 기술을 활용하여 복잡한 금융 세계를 쉽고 명확하게 탐색할 수 있도록 돕는 혁신적인 금융 솔루션 플랫폼입니다. 개인 맞춤형 금융 상품 추천, 주변 은행 파악, 실시간 시장 동향 등 다양한 기능을 통해 사용자의 성공적인 금융 여정을 지원합니다.
          </p>
        </div>
      </section>

      <!-- Key Features Section -->
      <section id="features" class="py-16 md:py-24 bg-gray-800">
        <div class="container mx-auto px-6">
          <h2 class="text-3xl md:text-4xl font-bold text-primary-light mb-12 text-center">FinScope 주요 기능</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 md:gap-10">
            <div class="feature-card bg-gray-900 p-6 rounded-lg shadow-xl text-center hover:shadow-primary-light/30">
              <h3 class="text-2xl font-semibold text-white mb-3">AI 기반 맞춤 추천</h3>
              <p class="text-gray-400">사용자의 투자 성향, 재정 목표, 관심사를 정밀하게 분석하여 최적화된 금융 상품을 AI가 추천합니다.</p>
            </div>
            <div class="feature-card bg-gray-900 p-6 rounded-lg shadow-xl text-center hover:shadow-primary-light/30">
              <h3 class="text-2xl font-semibold text-white mb-3">실시간 시장 파악</h3>
              <p class="text-gray-400">주식, 환율, 원자재 등 국내외 주요 금융 시장의 실시간 데이터를 한눈에 제공하여 시장 변화에 신속하게 대응할 수 있도록 지원합니다.</p>
            </div>
            <div class="feature-card bg-gray-900 p-6 rounded-lg shadow-xl text-center hover:shadow-primary-light/30">
              <h3 class="text-2xl font-semibold text-white mb-3">은행 찾기</h3>
              <p class="text-gray-400">현재 위치를 바탕으로 전국의 은행을 검색하여 최적화된 루트와 예상 시간을 알려드립니다.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Financial Products Section -->
      <section id="financial-products" class="py-16 md:py-24 bg-gray-900">
        <div class="container mx-auto px-6">
          <h2 class="text-3xl md:text-4xl font-bold text-primary-light mb-12 text-center">나에게 맞는 금융 상품 찾기</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-10 items-center">
            <div class="text-gray-300 leading-relaxed">
              <h3 class="text-2xl font-semibold text-white mb-4">예적금 비교 및 추천</h3>
              <p class="mb-4">다양한 은행의 예금 및 적금 상품을 한눈에 비교하고, FinScope의 AI 분석을 통해 사용자에게 가장 유리한 조건의 상품을 추천받아보세요. 금리, 조건, 우대혜택까지 꼼꼼하게 비교하여 최적의 선택을 도와드립니다.</p>
              <router-link to="/deposit-page" class="inline-block bg-primary hover:bg-primary-dark text-white font-semibold py-2 px-6 rounded-lg transition-colors">예적금 비교하기</router-link>
            </div>
            <div>
              <img src="@/assets/images/FinScope_logo.jpg" alt="금융 상품 비교" class="rounded-lg shadow-xl w-full h-auto object-cover max-h-50">
            </div>
          </div>
        </div>
      </section>

      <!-- Investment Information Section -->
      <section id="investment-info" class="py-16 md:py-24 bg-gray-800">
        <div class="container mx-auto px-6">
          <h2 class="text-3xl md:text-4xl font-bold text-primary-light mb-12 text-center">실시간 투자 정보 확인</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-10 items-center">
            <div class="order-2 md:order-1">
              <img src="@/assets/images/chart.jpg" alt="투자 정보" class="rounded-lg shadow-xl w-full h-auto object-cover max-h-80">
            </div>
            <div class="text-gray-300 leading-relaxed order-1 md:order-2">
              <h3 class="text-2xl font-semibold text-white mb-4">주식 및 현물 가격 정보</h3>
              <p class="mb-4">국내외 주요 주식 시장의 실시간 시세와 변동 추이, 기업 정보를 확인하고, 금, 원유 등 주요 현물 상품의 가격 변동을 실시간으로 추적하여 성공적인 투자 결정을 내리세요.</p>
              <router-link to="/stock-info" class="inline-block bg-primary hover:bg-primary-dark text-white font-semibold py-2 px-6 rounded-lg transition-colors mr-4">주식 정보 보기</router-link>
              <router-link to="/commodities-price" class="inline-block bg-primary hover:bg-primary-dark text-white font-semibold py-2 px-6 rounded-lg transition-colors">현물 가격 보기</router-link>
            </div>
          </div>
        </div>
      </section>

      <!-- Community Section -->
      <section id="community" class="py-16 md:py-24 bg-gray-900">
        <div class="container mx-auto px-6 text-center">
          <h2 class="text-3xl md:text-4xl font-bold text-primary-light mb-6">함께 나누는 금융 지식</h2>
          <p class="text-lg md:text-xl text-gray-300 max-w-3xl mx-auto leading-relaxed mb-8">
            FinScope 커뮤니티에서 다른 사용자들과 금융 정보를 공유하고, 투자 경험을 나누며 함께 성장하세요. 다양한 주제의 토론과 유용한 팁을 얻을 수 있습니다.
          </p>
          <router-link to="/board" class="inline-block bg-primary-light hover:bg-primary-dark text-white font-semibold py-3 px-8 rounded-lg text-lg transition-colors">커뮤니티 바로가기</router-link>
        </div>
      </section>

      <!-- Latest News Section (formerly Latest Information) -->
      <section id="latest-info" class="py-12 md:py-16 bg-gray-800">
        <div class="container mx-auto px-6">
          <h2 class="text-3xl md:text-4xl font-bold text-primary-light mb-12 text-center">오늘의 금융 소식</h2>
          <div class="space-y-8 md:space-y-10">
            <!-- Charts Row -->
            <!-- Charts Row -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-10 items-stretch">
              <div class="info-box-container bg-gray-900 p-6 rounded-lg shadow-lg flex flex-col">
                <h3 class="text-xl font-semibold text-white mb-3">실시간 환율</h3>
                <div class="info-box-content flex-grow flex flex-col">
                  <p class="text-sm text-gray-400 mb-4">주요 통화별 현재 환율 변동을 확인하세요.</p>
                  <exchangeRateChart class="flex-grow min-h-[280px] md:min-h-[320px] mt-4 rounded" />
                </div>
              </div>
              <div class="info-box-container bg-gray-900 p-6 rounded-lg shadow-lg flex flex-col">
                <h3 class="text-xl font-semibold text-white mb-3">실시간 현물 가격</h3>
                <div class="info-box-content flex-grow flex flex-col">
                  <p class="text-sm text-gray-400 mb-4">금, 원유 등 주요 현물 가격 정보를 제공합니다.</p>
                  <commoditiesChart class="flex-grow min-h-[280px] md:min-h-[320px] mt-4 rounded" />
                </div>
              </div>
            </div>
            <!-- News Row -->
            <div class="info-box-container bg-gray-900 p-6 rounded-lg shadow-lg">
              <h2 class="text-xl font-semibold text-white mb-3">주요 뉴스</h2>
              <div class="info-box-content news-scroll max-h-96 overflow-y-auto"> 
                <div v-if="newsList.length === 0" class="text-gray-500 text-center py-4">뉴스를 불러오는 중입니다...</div>
                <div v-for="newsItem in newsList" :key="newsItem.link" class="py-2 border-b border-gray-700 last:border-b-0">
                  <router-link :to="{ name: 'news-detail', query: { url: newsItem.link } }"
                    class="font-medium text-sm text-gray-300 hover:text-primary-light cursor-pointer">
                    {{ newsItem.title }}
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import commoditiesChart from '@/components/commoditiesChart.vue'
import exchangeRateChart from "@/components/exchangeRateChart.vue"
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
import img1 from '@/assets/images/finance_01.jpg'
import img2 from '@/assets/images/finance_02.jpg'
import img3 from '@/assets/images/finance_03.jpg'
import img4 from '@/assets/images/finance_04.jpg'
import axios from 'axios'

const imgUrl = ref([
  { id: 1, src: img1, alt: 'Finance Image 1' },
  { id: 2, src: img2, alt: 'Finance Image 2' },
  { id: 3, src: img3, alt: 'Finance Image 3' },
  { id: 4, src: img4, alt: 'Finance Image 4' },
]);
const currentSlide = ref(0);
const intervalRef = ref(null);
const newsList = ref([]);
const slideDirection = ref(1); 

const previousSlide = computed(() => {
  return (currentSlide.value - slideDirection.value + imgUrl.value.length) % imgUrl.value.length;
});

const nextSlide = () => {
  slideDirection.value = 1;
  currentSlide.value = (currentSlide.value + 1) % imgUrl.value.length;
};

const startCarousel = () => {
  if (!intervalRef.value) {
    intervalRef.value = setInterval(nextSlide, 2500); 
  }
};

const pauseCarousel = () => {
  clearInterval(intervalRef.value);
  intervalRef.value = null;
};

const fetchNews = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/stocks/news-list/');
    newsList.value = response.data;
  } catch (error) {
    console.error('뉴스 API 요청 실패', error);
  }
};

const activeSection = ref('introduction');
const observer = ref(null);
const sectionElements = ref([]);

const smoothScrollTo = (selector) => {
  const element = document.querySelector(selector);
  if (element) {
    const primaryNavHeight = 64; // Assuming primary navbar is 4rem (64px)
    const secondaryNav = document.getElementById('secondary-nav');
    const secondaryNavHeight = secondaryNav?.offsetHeight || 0;
    // Calculate offset based on whether the secondary nav is currently sticky
    let totalOffset = primaryNavHeight + 20; // Base offset + some padding
    if (secondaryNav && getComputedStyle(secondaryNav).position === 'fixed') {
      totalOffset += secondaryNavHeight;
    }
    
    const elementPosition = element.getBoundingClientRect().top + window.pageYOffset;
    const offsetPosition = elementPosition - totalOffset;

    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    });
  }
};

const handleStickyNav = () => {
  const scrollPosition = window.pageYOffset || document.documentElement.scrollTop;
  const heroSectionHeight = document.getElementById('hero')?.offsetHeight || 0;
  const nav = document.getElementById('secondary-nav');
  const primaryNavHeight = 64; 

  if (nav) {
    if (scrollPosition > heroSectionHeight - primaryNavHeight) {
      nav.classList.add('fixed', 'top-16', 'w-full', 'bg-gray-800', 'shadow-lg');
      nav.classList.remove('hidden');
    } else {
      nav.classList.remove('fixed', 'top-16', 'w-full', 'bg-gray-800', 'shadow-lg');
      nav.classList.add('hidden');
    }
  }
};

const initIntersectionObserver = () => {
  const primaryNavHeight = 64; 
  const secondaryNavHeightEst = 50; // Estimate secondary nav height for rootMargin
  const rootMarginTop = primaryNavHeight + secondaryNavHeightEst;

  const options = {
    root: null, // viewport
    rootMargin: `-${rootMarginTop}px 0px -${window.innerHeight - rootMarginTop - 150}px 0px`, // Target a 150px band at the top
    threshold: 0 // Trigger as soon as any part enters/leaves this band
  };

  observer.value = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        activeSection.value = entry.target.id;
      }
    });
    // If multiple are intersecting, the last one processed by forEach will set activeSection.
    // To ensure the topmost visible section is active:
    const intersectingEntries = entries.filter(e => e.isIntersecting);
    if (intersectingEntries.length > 0) {
        // Sort by position on screen, highest first
        intersectingEntries.sort((a, b) => a.target.getBoundingClientRect().top - b.target.getBoundingClientRect().top);
        activeSection.value = intersectingEntries[0].target.id;
    }


  }, options);

  const sections = ['introduction', 'features', 'financial-products', 'investment-info', 'community', 'latest-info'];
  sectionElements.value = sections.map(id => document.getElementById(id)).filter(el => el);
  sectionElements.value.forEach(section => observer.value.observe(section));
};

onMounted(() => {
  startCarousel();
  fetchNews();
  window.addEventListener('scroll', handleStickyNav);
  handleStickyNav(); // Initial check
  initIntersectionObserver();
});

onBeforeUnmount(() => {
  pauseCarousel();
  window.removeEventListener('scroll', handleStickyNav);
  if (observer.value) {
    sectionElements.value.forEach(section => observer.value.unobserve(section));
    observer.value.disconnect();
  }
});

</script>

<style scoped>
.carousel-container {
  position: relative;
  width: 100%;
  overflow: hidden;
  height: 65vh; 
}

.carousel-slide {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  transform: translateX(100%);
  transition: opacity 0.5s ease-in-out, transform 0.5s ease-in-out;
  visibility: hidden;
}

.carousel-slide.active {
  opacity: 1;
  transform: translateX(0);
  visibility: visible;
  z-index: 1; 
}

.carousel-slide.prev {
  transform: translateX(-100%);
  visibility: visible;
  z-index: 0;
}

.carousel-slide img {
  width: 100%;
  height: 100%;
  object-fit: cover; 
  object-position: center; 
  display: block;
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
  background-color: rgba(0, 0, 0, 0.3); 
  border-radius: 8px;
}

.carousel-content-overlay h1,
.carousel-content-overlay p {
  animation: fadeInSlideUp 1s ease-out forwards;
}

@keyframes fadeInSlideUp {
  from {
    opacity: 0;
    transform: translateY(30px); 
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

#secondary-nav {
  padding-top: 0.75rem; 
  padding-bottom: 0.75rem; 
}

#secondary-nav a {
  padding-left: 0.75rem; 
  padding-right: 0.75rem; 
  padding-top: 0.5rem; 
  padding-bottom: 0.5rem; 
  border-radius: 9999px; 
  font-size: 0.875rem; 
  font-weight: 500; 
  transition-property: color, background-color, border-color, text-decoration-color, fill, stroke;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}


#secondary-nav.fixed {
  top: 4rem; /* Height of the primary navbar */
}

.news-scroll::-webkit-scrollbar {
  width: 8px;
}
.news-scroll::-webkit-scrollbar-track {
  background: #2d3748; 
}
.news-scroll::-webkit-scrollbar-thumb {
  background: #4a5568; 
  border-radius: 4px;
}
.news-scroll::-webkit-scrollbar-thumb:hover {
  background: #2563eb; 
}

.feature-card {
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
}
.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2), 0 10px 10px -5px rgba(0, 0, 0, 0.1);
}
</style>
