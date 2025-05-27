<template>
  <main class="container mx-auto px-4 sm:px-6 py-8 text-gray-100 bg-gray-900 min-h-screen">
    <div class="max-w-3xl mx-auto">
      <h1 class="text-3xl font-bold mb-8 text-center">AI 금융상품 추천</h1>

      <!-- Initial Screen with a large button -->
      <div v-if="showInitialScreen && authStore.isLoggedIn" class="text-center py-20">
        <button @click="startRecommendationProcess" 
          class="bg-primary hover:bg-primary-dark text-white font-bold py-4 px-8 rounded-lg text-xl shadow-lg transition-transform transform hover:scale-105">
          AI를 활용하여 최적의 금융 상품 찾기
        </button>
      </div>

      <div v-if="!authStore.isLoggedIn" class="text-center p-8 bg-gray-800 rounded-lg shadow-xl">
        <p class="text-xl mb-4">추천을 받으려면 로그인이 필요합니다.</p>
        <RouterLink :to="{ name: 'login', query: { redirect: route.fullPath } }"
          class="bg-primary hover:bg-primary-dark text-white font-semibold py-2 px-6 rounded-lg transition-colors">
          로그인하기
        </RouterLink>
      </div>
      
      <!-- Main content area, shown after initial button click or if not logged in (login prompt shows) -->
      <div v-if="!showInitialScreen && authStore.isLoggedIn">
        <div v-if="isLoadingProfile" class="text-center py-10">
          <p class="text-xl">사용자 정보를 불러오는 중...</p>
        </div>
        <div v-else-if="!userProfile" class="text-center py-10 text-red-400">
          <p class="text-xl">사용자 프로필 정보를 불러올 수 없습니다. 마이페이지에서 프로필을 완성해주세요.</p>
           <RouterLink :to="{ name: 'my-page-edit-profile' }"
            class="mt-4 inline-block bg-primary hover:bg-primary-dark text-white font-semibold py-2 px-6 rounded-lg transition-colors">
            프로필 수정하기
          </RouterLink>
        </div>
        <div v-else>
          <div class="bg-gray-800 p-6 rounded-lg shadow-xl border border-gray-700 mb-8">
            <h2 class="text-2xl font-semibold mb-4">내 프로필 기반 추천</h2>
            <p class="text-gray-400 mb-1">나이: {{ userProfile.age || '정보 없음' }}</p>
            <p class="text-gray-400 mb-1">연봉: {{ userProfile.salary ? userProfile.salary.toLocaleString() + '원' : '정보 없음' }}</p>
            <p class="text-gray-400 mb-4">투자 성향: {{ userProfile.investment_tendency || '정보 없음' }}</p>
            <button @click="fetchRecommendations" :disabled="isLoadingRecommendations"
              class="w-full bg-primary hover:bg-primary-dark text-white font-semibold py-3 px-6 rounded-lg transition-colors disabled:opacity-50">
              {{ isLoadingRecommendations ? '추천 생성 중...' : 'AI 추천 받기' }}
            </button>
          </div>

          <div v-if="recommendationError" class="mt-6 p-4 bg-red-900 border border-red-700 rounded-lg text-red-300">
            <p>오류: {{ recommendationError }}</p>
          </div>

          <div v-if="recommendations.length > 0" class="mt-8">
            <h2 class="text-2xl font-semibold mb-6 text-center">추천 포트폴리오</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div v-for="(item, index) in recommendations" :key="index"
                class="bg-gray-800 p-6 rounded-lg shadow-xl border border-gray-700 hover:shadow-primary/50 transition-shadow">
                <h3 class="text-xl font-semibold text-primary mb-2">{{ item.name }}</h3>
                <p class="text-gray-400 capitalize">종류: {{ item.type === 'deposit' ? '예/적금' : '주식' }}</p>
                <!-- Add more details if available from financial_products.json or stock info -->
              </div>
            </div>
            <div class="mt-8 text-center">
              <button @click="saveRecommendation" :disabled="isSavingRecommendation"
                class="bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors disabled:opacity-50">
                {{ isSavingRecommendation ? '저장 중...' : '이 추천 저장하기' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '@/stores/user';
import api from '@/api/axios';
import { useRoute, useRouter } from 'vue-router'; // Import useRouter for navigation

const authStore = useAuthStore();
const route = useRoute(); 
const router = useRouter(); 

const userProfile = ref(null);
const isLoadingProfile = ref(false);
const recommendations = ref([]);
const isLoadingRecommendations = ref(false);
const recommendationError = ref('');
const isSavingRecommendation = ref(false);
const showInitialScreen = ref(true); // New state for UI flow

const startRecommendationProcess = () => {
  console.log('startRecommendationProcess called');
  showInitialScreen.value = false;
  if (!userProfile.value && authStore.isLoggedIn) {
    console.log('User profile not yet loaded, calling fetchUserProfile from startRecommendationProcess');
    fetchUserProfile(); 
  } else {
    console.log('User profile already available or user not logged in.');
  }
};

const fetchUserProfile = async () => {
  console.log('fetchUserProfile called. isLoggedIn:', authStore.isLoggedIn);
  if (authStore.user) {
    userProfile.value = authStore.user;
    console.log('User profile taken directly from store:', userProfile.value);
  } else if (authStore.isLoggedIn) {
    isLoadingProfile.value = true;
    console.log('Loading user profile from API...');
    await authStore.loadUser(); // Ensure user data is loaded
    userProfile.value = authStore.user;
    isLoadingProfile.value = false;
    console.log('User profile loaded from API:', userProfile.value);
  } else {
    console.log('User not logged in, cannot fetch profile.');
  }
};

const fetchRecommendations = async () => {
  console.log('fetchRecommendations called');
  if (!userProfile.value) {
    recommendationError.value = '사용자 프로필 정보가 필요합니다. (fetchRecommendations)';
    console.error('User profile is null in fetchRecommendations');
    return;
  }
  // Ensure essential profile fields for recommendation are present
  if (!userProfile.value.age || !userProfile.value.salary || !userProfile.value.investment_tendency) {
    recommendationError.value = '추천을 위해 프로필 정보(나이, 연봉, 투자 성향)를 모두 입력해주세요.';
    console.error('Missing essential profile fields for recommendation:', userProfile.value);
    // Optionally, guide user to edit profile
    // router.push({ name: 'my-page-edit-profile' });
    return;
  }

  isLoadingRecommendations.value = true;
  recommendationError.value = '';
  recommendations.value = [];
  console.log('Fetching recommendations with user profile:', userProfile.value);

  try {
    // Prepare user_info for the backend
    const userInfoPayload = {
      age: userProfile.value.age,
      assets: userProfile.value.assets, // Assuming assets is part of user profile
      salary: userProfile.value.salary,
      tendency: userProfile.value.investment_tendency 
    };
    // The backend expects user_info as a JSON string in query params
    const response = await api.get('/api/stocks/recommend/', { 
      params: { user_info: JSON.stringify(userInfoPayload) } 
    });
    // The backend's get_ai_recommend view tries to json.loads the response.text from get_recommend
    // Ensure the response.data is already the parsed JSON array
    if (typeof response.data === 'string') {
        recommendations.value = JSON.parse(response.data);
    } else {
        recommendations.value = response.data;
    }

  } catch (error) {
    console.error('Error fetching recommendations:', error);
    recommendationError.value = error.response?.data?.detail || error.response?.data?.error || '추천을 받아오는 중 오류가 발생했습니다.';
    if (error.response?.data && typeof error.response.data === 'string' && error.response.data.includes("Financial data not available")) {
        recommendationError.value = '추천에 필요한 금융상품 데이터를 불러올 수 없습니다. 관리자에게 문의하세요.';
    }
  } finally {
    isLoadingRecommendations.value = false;
  }
};

const saveRecommendation = async () => {
  if (!authStore.isLoggedIn) {
    alert('로그인이 필요한 기능입니다.');
    router.push({ name: 'login', query: { redirect: route.fullPath } });
    return;
  }
  if (recommendations.value.length === 0) {
    alert('저장할 추천 내용이 없습니다.');
    return;
  }
  isSavingRecommendation.value = true;
  try {
    const payload = {
      recommendation_data: JSON.stringify(recommendations.value), // Store as JSON string
      user_profile_at_recommendation: { // Snapshot of user profile
        age: userProfile.value.age,
        assets: userProfile.value.assets,
        salary: userProfile.value.salary,
        investment_tendency: userProfile.value.investment_tendency
      }
    };
    // This action needs to be created in the store
    await authStore.saveAiRecommendation(payload); 
    alert('추천이 마이페이지에 저장되었습니다.');
  } catch (error) {
    console.error('Error saving recommendation:', error);
    alert(error.response?.data?.detail || error.message || '추천 저장 중 오류가 발생했습니다.');
  } finally {
    isSavingRecommendation.value = false;
  }
};

onMounted(() => {
  console.log('RecommendedProductsPage onMounted. isLoggedIn:', authStore.isLoggedIn, 'showInitialScreen:', showInitialScreen.value);
  if (authStore.isLoggedIn) {
    fetchUserProfile();
  }
});
</script>

<style scoped>
/* Add any specific styles for this page */
main {
  padding-top: 2rem;
}
</style>
