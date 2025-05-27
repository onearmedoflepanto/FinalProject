<template>
  <main class="flex-grow container mx-auto px-4 sm:px-6 py-8 md:py-12">
    <div class="board-section bg-white p-6 md:p-8 rounded-xl shadow-xl border border-gray-200">
      <h1 class="text-2xl md:text-3xl font-bold text-teal-700 mb-6">{{ formModeTitle }}</h1>
      <form @submit.prevent="submitPost">
        <div class="mb-4">
          <label for="postTitleInput" class="block text-sm font-medium text-gray-700 mb-1">제목</label>
          <input type="text" id="postTitleInput" v-model="postForm.title" 
                 class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500" required>
        </div>
        <div class="mb-6">
          <label for="postContentInput" class="block text-sm font-medium text-gray-700 mb-1">내용</label>
          <textarea id="postContentInput" v-model="postForm.content" 
                    class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500" rows="10" required></textarea>
        </div>
        <div class="flex justify-end space-x-3">
          <router-link :to="{ name: 'board-list' }"
            class="bg-gray-200 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-300">취소</router-link>
          <button type="submit"
            class="bg-teal-600 text-white py-2 px-4 rounded-lg hover:bg-teal-700">{{ formMode === 'create' ? '등록' : '수정' }}</button>
        </div>
      </form>
    </div>
     <div id="loginRequiredModal" v-if="showLoginRequiredModal" 
        class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex justify-center items-center z-50">
      <div class="bg-white p-6 md:p-8 rounded-xl shadow-xl border border-gray-200 text-center w-full max-w-md">
        <h2 class="text-xl font-semibold text-red-600 mb-4">로그인 필요</h2>
        <p class="text-gray-700 mb-6">이 작업을 수행하려면 로그인이 필요합니다.</p>
        <router-link :to="{ name: 'login', query: { redirect: $route.fullPath } }" 
                     class="bg-teal-600 text-white py-2 px-6 rounded-lg hover:bg-teal-700 text-sm">
          로그인 페이지로 이동
        </router-link>
        <button class="mt-4 ml-2 text-sm text-gray-500 hover:text-gray-700 underline"
                @click="showLoginRequiredModal = false">
          닫기
        </button>
      </div>
    </div>
  </main>
  <Footer />
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Footer from '@/components/footer.vue';
import { useAuthStore } from '@/stores/user.js';
import api from '@/api/axios';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const postForm = reactive({
  id: null,
  title: '',
  content: '',
});
const formMode = ref('create'); // 'create' or 'edit'
const postId = computed(() => route.params.id); // For edit mode
const showLoginRequiredModal = ref(false);

const isLoggedIn = computed(() => authStore.isLoggedIn);

const formModeTitle = computed(() => {
  return formMode.value === 'create' ? '새 글 작성' : '글 수정';
});

const fetchPostForEdit = async () => {
  if (postId.value) {
    formMode.value = 'edit';
    try {
      const response = await api.get(`/api/boards/posts/${postId.value}/`);
      const post = response.data;
      // Ensure the current user is the author before populating form
      if (post.author_id !== authStore.user?.id) {
        alert('이 게시글을 수정할 권한이 없습니다.');
        router.push({ name: 'board-detail', params: { id: postId.value } });
        return;
      }
      postForm.id = post.id;
      postForm.title = post.title;
      postForm.content = post.content;
    } catch (error) {
      console.error('Error fetching post for editing:', error);
      alert('게시글 정보를 불러오는 데 실패했습니다.');
      router.push({ name: 'board-list' });
    }
  } else {
    formMode.value = 'create';
    postForm.id = null;
    postForm.title = '';
    postForm.content = '';
  }
};

const submitPost = async () => {
  if (!isLoggedIn.value) {
    showLoginRequiredModal.value = true;
    return;
  }
  try {
    if (formMode.value === 'create') {
      const response = await api.post('/api/boards/posts/', { title: postForm.title, content: postForm.content });
      alert('게시글이 성공적으로 등록되었습니다.');
      router.push({ name: 'board-detail', params: { id: response.data.id } }); // Navigate to new post's detail
    } else { // edit mode
      await api.put(`/api/boards/posts/${postForm.id}/`, { title: postForm.title, content: postForm.content });
      alert('게시글이 성공적으로 수정되었습니다.');
      router.push({ name: 'board-detail', params: { id: postForm.id } });
    }
  } catch (error) {
    console.error('Error submitting post:', error.response?.data || error.message);
    alert('게시글 등록/수정에 실패했습니다. 입력 내용을 확인해주세요.');
  }
};

onMounted(() => {
  if (!isLoggedIn.value && (route.name === 'board-create' || route.name === 'board-edit')) {
    showLoginRequiredModal.value = true;
    // Optionally, redirect if modal is not preferred for direct access attempts
    // router.push({ name: 'login', query: { redirect: route.fullPath }});
  } else {
    fetchPostForEdit();
  }
});
</script>
