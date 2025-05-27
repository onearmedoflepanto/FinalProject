<template>
  <div class="space-y-8">
    <h2 class="text-3xl font-semibold text-gray-100">저장된 AI 추천</h2>

    <div v-if="isLoading" class="text-center py-10">
      <p class="text-xl text-gray-400">저장된 추천을 불러오는 중...</p>
    </div>

    <div v-else-if="!savedRecommendations || savedRecommendations.length === 0" class="text-center py-10">
      <p class="text-xl text-gray-400">저장된 AI 추천이 없습니다.</p>
      <RouterLink :to="{ name: 'ai-recommendations' }"
        class="mt-4 inline-block bg-primary hover:bg-primary-dark text-white font-semibold py-2 px-6 rounded-lg transition-colors">
        AI 추천 받으러 가기
      </RouterLink>
    </div>

    <div v-else class="space-y-6">
      <div v-for="savedRec in sortedRecommendations" :key="savedRec.id" 
           class="bg-gray-800 p-6 rounded-lg shadow-xl border border-gray-700">
        <div class="mb-4">
          <p class="text-sm text-gray-500">저장일: {{ new Date(savedRec.saved_at).toLocaleString() }}</p>
          <div v-if="savedRec.user_profile_at_recommendation" class="mt-2 text-xs text-gray-400">
            <p>추천 당시 프로필:</p>
            <ul class="list-disc list-inside ml-4">
              <li>나이: {{ savedRec.user_profile_at_recommendation.age || 'N/A' }}</li>
              <li>연봉: {{ savedRec.user_profile_at_recommendation.salary ? savedRec.user_profile_at_recommendation.salary.toLocaleString() + '원' : 'N/A' }}</li>
              <li>투자 성향: {{ savedRec.user_profile_at_recommendation.investment_tendency || 'N/A' }}</li>
            </ul>
          </div>
        </div>
        
        <h3 class="text-xl font-semibold text-primary mb-3">추천 포트폴리오:</h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div v-for="(item, index) in parseRecommendationData(savedRec.recommendation_data)" :key="index"
               class="bg-gray-700 p-4 rounded-md shadow-md">
            <p class="font-semibold text-gray-100">{{ item.name }}</p>
            <p class="text-sm text-gray-300 capitalize">{{ item.type === 'deposit' ? '예/적금' : '주식' }}</p>
          </div>
        </div>
        <!-- Add a delete button if needed -->
        <!-- <button @click="deleteRecommendation(savedRec.id)" class="mt-4 text-red-500 hover:text-red-400 text-sm">삭제</button> -->
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '@/stores/user';
import { RouterLink } from 'vue-router';

const authStore = useAuthStore();
const isLoading = ref(false);

// Directly use the user data from the store
const savedRecommendations = computed(() => authStore.user?.saved_ai_recommendations || []);

const sortedRecommendations = computed(() => {
  // Sort by saved_at date, newest first
  return [...savedRecommendations.value].sort((a, b) => new Date(b.saved_at) - new Date(a.saved_at));
});

const parseRecommendationData = (jsonDataString) => {
  try {
    return JSON.parse(jsonDataString);
  } catch (e) {
    console.error("Failed to parse recommendation_data:", e);
    return []; // Return empty array on error
  }
};

onMounted(async () => {
  // Ensure user data is loaded if not already present
  if (!authStore.user && authStore.isLoggedIn) {
    isLoading.value = true;
    await authStore.loadUser();
    isLoading.value = false;
  }
});

// Optional: Implement deleteRecommendation if needed
// const deleteRecommendation = async (recommendationId) => {
//   if (!confirm('이 추천을 삭제하시겠습니까?')) return;
//   try {
//     // await api.delete(`/api/accounts/saved-ai-recommendations/${recommendationId}/`);
//     // await authStore.loadUser(); // Refresh user data
//     alert('추천이 삭제되었습니다.');
//   } catch (error) {
//     console.error('Error deleting recommendation:', error);
//     alert('추천 삭제 중 오류가 발생했습니다.');
//   }
// };
</script>

<style scoped>
/* Add any specific styles */
</style>
