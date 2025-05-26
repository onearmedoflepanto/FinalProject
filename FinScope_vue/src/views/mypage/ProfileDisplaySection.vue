<template>
  <div class="content-section">
    <h2 class="text-2xl font-semibold mb-6 text-gray-800 border-b-2 border-emerald-500 pb-3">기본 정보</h2>
    <div v-if="userData" class="space-y-5">
      <div><label class="block text-xs font-medium text-gray-500 uppercase tracking-wider">아이디</label><p class="text-gray-900 text-lg">{{ userData.userId }}</p></div>
      <div><label class="block text-xs font-medium text-gray-500 uppercase tracking-wider">이메일</label><p class="text-gray-900 text-lg">{{ userData.email }}</p></div>
      <div><label class="block text-xs font-medium text-gray-500 uppercase tracking-wider">닉네임</label><p class="text-gray-900 text-lg">{{ userData.nickname }}</p></div>
      <div><label class="block text-xs font-medium text-gray-500 uppercase tracking-wider">나이</label><p class="text-gray-900 text-lg">{{ userData.age || '정보 없음' }}</p></div>
      <div><label class="block text-xs font-medium text-gray-500 uppercase tracking-wider">현재 가진 금액 (원)</label><p class="text-gray-900 text-lg">{{ formatCurrency(userData.assets) }}</p></div>
      <div><label class="block text-xs font-medium text-gray-500 uppercase tracking-wider">연봉 (원)</label><p class="text-gray-900 text-lg">{{ formatCurrency(userData.salary) }}</p></div>
      <div><label class="block text-xs font-medium text-gray-500 uppercase tracking-wider">저축 성향</label><p class="text-gray-900 text-lg">{{ userData.savingsTendency || '정보 없음' }}</p></div>
    </div>
    <div v-else class="text-gray-500 p-4 text-center">
      사용자 정보를 불러오는 중이거나 표시할 정보가 없습니다.
    </div>
  </div>
</template>

<script setup>
import { reactive, watch, onMounted } from 'vue';
import { useAuthStore } from '@/stores/user';
import { storeToRefs } from 'pinia';

const authStore = useAuthStore();
const { user: authUser, isLoggedIn } = storeToRefs(authStore);

const userData = reactive({
  userId: '',
  email: '',
  nickname: '',
  age: null,
  assets: null,
  salary: null,
  savingsTendency: '',
});

const formatCurrency = (value) => {
  if (value === null || value === undefined || isNaN(Number(value))) return '0';
  return Number(value).toLocaleString('ko-KR');
};

const updateLocalUserData = (newUser) => {
  if (newUser) {
    userData.userId = newUser.username || newUser.userId || '';
    userData.email = newUser.email || '';
    userData.nickname = newUser.nickname || '';
    userData.age = newUser.age || null;
    userData.assets = newUser.assets || null;
    userData.salary = newUser.salary || null;
    userData.savingsTendency = newUser.savings_tendency || newUser.savingsTendency || '';
  } else {
    Object.keys(userData).forEach(key => {
      const type = typeof userData[key];
      if (type === 'string') userData[key] = '';
      else if (type === 'number') userData[key] = null;
      else userData[key] = null;
    });
  }
};

watch(authUser, (newUser) => {
  updateLocalUserData(newUser);
}, { immediate: true, deep: true });

onMounted(async () => {
  if (isLoggedIn.value && !authUser.value) {
    await authStore.loadUser(); // This will trigger the watcher
  } else {
    updateLocalUserData(authUser.value); // Populate if already loaded
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
</style>
