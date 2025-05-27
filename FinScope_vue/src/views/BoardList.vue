<template>
  <div class="bg-gray-900 min-h-screen py-8 md:py-12 text-gray-100">
    <main class="flex-grow container mx-auto px-4 sm:px-6">
      <div id="postListSection" class="board-section bg-gray-800 p-6 md:p-8 rounded-xl shadow-xl border border-gray-700">
        <div class="flex justify-between items-center mb-6">
          <h1 class="text-2xl md:text-3xl font-bold text-primary-light">자유 게시판</h1>
        <router-link :to="{ name: 'board-create' }"
          class="bg-primary hover:bg-primary-dark text-white py-2 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-light focus:ring-opacity-50 transition duration-150 ease-in-out text-sm font-medium">
          글쓰기
        </router-link>
      </div>

      <!-- Table Layout Start -->
      <div class="overflow-x-auto rounded-lg shadow">
        <table class="w-full min-w-[640px]">
          <thead class="bg-gray-700">
            <tr>
              <th class="px-4 py-3 text-left text-sm font-medium text-gray-300 uppercase tracking-wider w-[8%]">번호</th>
              <th class="px-4 py-3 text-left text-sm font-medium text-gray-300 uppercase tracking-wider w-[40%]">제목</th>
              <th class="px-4 py-3 text-left text-sm font-medium text-gray-300 uppercase tracking-wider w-[15%]">작성자</th>
              <th class="px-4 py-3 text-left text-sm font-medium text-gray-300 uppercase tracking-wider w-[15%]">작성일</th>
              <th class="px-4 py-3 text-center text-sm font-medium text-gray-300 uppercase tracking-wider w-[11%]">댓글</th>
              <th class="px-4 py-3 text-center text-sm font-medium text-gray-300 uppercase tracking-wider w-[11%]">조회수</th>
            </tr>
          </thead>
          <tbody class="bg-gray-800 divide-y divide-gray-700">
            <tr v-if="posts.length === 0">
              <td colspan="6" class="px-4 py-10 text-center text-gray-400">게시글이 없습니다.</td>
            </tr>
            <tr v-for="post in posts" :key="post.id" class="hover:bg-gray-700/50 transition-colors duration-150">
              <td class="px-4 py-3 text-sm text-gray-400">{{ post.id }}</td>
              <td class="px-4 py-3 text-sm text-gray-100">
                <router-link :to="{ name: 'board-detail', params: { id: post.id } }" 
                             class="text-primary-light hover:text-primary hover:underline font-medium truncate block" :title="post.title">
                  {{ post.title }}
                </router-link>
              </td>
              <td class="px-4 py-3 text-sm text-gray-400">{{ post.author_nickname || post.author_username }}</td>
              <td class="px-4 py-3 text-sm text-gray-400">{{ formatDate(post.created_at) }}</td>
              <td class="px-4 py-3 text-sm text-gray-400 text-center">{{ post.comments_count }}</td>
              <td class="px-4 py-3 text-sm text-gray-400 text-center">{{ post.views }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <!-- Table Layout End -->

      <div class="mt-8 flex justify-center items-center pagination">
        <!-- Pagination controls will go here if implemented -->
      </div>
    </div>
    <div id="loginRequiredSection"
      class="board-section bg-gray-800 p-6 md:p-8 rounded-xl shadow-xl border border-gray-700 text-center"
      v-if="showLoginRequired">
      <h2 class="text-xl font-semibold text-red-400 mb-4">로그인 필요</h2>
      <p class="text-gray-300 mb-6">글을 작성하려면 로그인이 필요합니다.</p>
      <router-link to="/login" class="bg-primary hover:bg-primary-dark text-white py-2 px-6 rounded-lg text-sm">로그인 페이지로
        이동</router-link>
      <button id="closeLoginRequiredBtn" class="mt-4 text-sm text-gray-400 hover:text-gray-200 underline"
        @click="showLoginRequired = false">닫기</button>
    </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import Footer from '@/components/footer.vue';
import { useAuthStore } from '@/stores/user.js';
import api from '@/api/axios';

const posts = ref([]);
const router = useRouter();
const authStore = useAuthStore();
const isLoggedIn = computed(() => authStore.isLoggedIn);
const showLoginRequired = ref(false);

// Pagination state (can be expanded later)
const totalPosts = ref(0);
const currentPage = ref(1);
const nextUrl = ref(null);
const previousUrl = ref(null);

const fetchPosts = async (page = 1) => {
  try {
    const response = await api.get(`/api/boards/posts/?page=${page}`);
    posts.value = response.data.results;
    totalPosts.value = response.data.count;
    nextUrl.value = response.data.next;
    previousUrl.value = response.data.previous;
    currentPage.value = page;
  } catch (error) {
    console.error('Error fetching posts:', error);
    alert('게시글을 불러오는 데 실패했습니다.');
  }
};

const formatDate = (dateString, includeTime = false) => {
  if (!dateString) return '';
  const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
  if (includeTime) {
    options.hour = '2-digit';
    options.minute = '2-digit';
    options.second = '2-digit';
  }
  return new Date(dateString).toLocaleDateString(undefined, options);
};

// Check login status for create post button, though router guards will also handle it
// This local check is for UI feedback (showing login required message)
const handleCreatePostClick = () => {
  if (!isLoggedIn.value) {
    showLoginRequired.value = true;
  } else {
    router.push({ name: 'board-create' });
  }
};

onMounted(() => {
  fetchPosts();
});
</script>
