<template>
  <main class="flex-grow container mx-auto px-4 sm:px-6 py-8 md:py-12">
    <div v-if="loading" class="text-center py-10">
      <p class="text-gray-500">게시글을 불러오는 중...</p>
    </div>
    <div v-else-if="error" class="text-center py-10">
      <p class="text-red-500">{{ error }}</p>
      <router-link :to="{ name: 'board-list' }" class="mt-4 inline-block bg-teal-600 text-white py-2 px-4 rounded-lg hover:bg-teal-700">
        목록으로 돌아가기
      </router-link>
    </div>
    <div v-else-if="post" id="postDetailSection" class="board-section bg-white p-6 md:p-8 rounded-xl shadow-xl border border-gray-200">
      <div class="flex justify-between items-center mb-4">
        <h1 id="detailPostTitle" class="text-3xl md:text-4xl font-bold text-gray-800">{{ post.title }}</h1>
        <router-link :to="{ name: 'board-list' }" class="bg-teal-600 text-white py-2 px-5 rounded-lg hover:bg-teal-700 text-sm font-medium transition-colors">
          목록
        </router-link>
      </div>
      <div class="post-detail-header text-sm text-gray-500 mb-6 border-b pb-4">
        <p>작성자: <span class="font-semibold text-teal-700">{{ post.author_nickname || post.author }}</span></p>
        <p>작성일: <span class="font-medium text-gray-700">{{ formatDate(post.created_at) }}</span></p>
        <p>조회수: <span class="font-medium text-gray-700">{{ post.views }}</span></p>
      </div>
      <div id="detailPostContent" class="prose prose-sm sm:prose lg:prose-lg xl:prose-xl max-w-none mb-10 leading-relaxed text-gray-700" v-html="post.content"></div>
      
      <div class="flex items-center space-x-3 mb-8">
        <button 
          :class="['flex items-center space-x-1.5 px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200 border', 
                   post.is_liked ? 'bg-red-500 text-white border-red-500 hover:bg-red-600' : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-100 hover:border-gray-400']"
          @click="toggleLike"
          :disabled="!isLoggedIn"
        >
          <svg :class="['w-4 h-4', post.is_liked ? 'fill-current' : '']" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" />
        </svg>
        <span>좋아요 ({{ post.likes_count }})</span>
      </button>
      <button 
        :class="['flex items-center space-x-1.5 px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200 border', 
                 post.is_bookmarked ? 'bg-blue-500 text-white border-blue-500 hover:bg-blue-600' : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-100 hover:border-gray-400']"
        @click="toggleBookmark"
        :disabled="!isLoggedIn"
      >
        <svg :class="['w-4 h-4', post.is_bookmarked ? 'fill-current' : '']" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path d="M5 4a2 2 0 012-2h6a2 2 0 012 2v14l-5-2.5L5 18V4z" />
        </svg>
        <span>북마크 ({{ post.bookmarks_count }})</span>
      </button>
      <template v-if="post.author_id === authStore.user?.id">
        <router-link :to="{ name: 'board-edit', params: { id: post.id } }"
          class="bg-sky-600 text-white py-2 px-4 rounded-lg hover:bg-sky-700 text-sm font-medium transition-colors"
        >
          게시글 수정
        </router-link>
        <button 
          class="bg-red-600 text-white py-2 px-4 rounded-lg hover:bg-red-700 text-sm font-medium transition-colors"
            @click="handleDeletePost"
          >
            삭제
          </button>
        </template>
      </div>

      <div class="comments-section">
      <h2 class="text-2xl font-semibold text-gray-800 mb-6 pt-6 border-t">댓글 ({{ comments.length }})</h2>
      <div id="detailPostComments" class="space-y-6">
        <div v-if="comments.length === 0" class="text-gray-500 py-4">아직 댓글이 없습니다. 첫 댓글을 작성해보세요!</div>
        <div v-for="comment in comments" :key="comment.id" class="bg-slate-50 p-5 rounded-lg shadow-sm border border-slate-200">
          <div class="flex justify-between items-start mb-1">
            <p class="font-semibold text-teal-700 text-md">{{ comment.user_nickname || comment.user }}</p>
            <p class="text-xs text-gray-400">{{ formatDate(comment.created_at, true) }}</p>
          </div>
          <!-- Conditional display for view mode vs edit mode -->
          <template v-if="editingCommentId === comment.id">
            <!-- Edit Mode -->
            <textarea v-model="editingCommentContent" class="w-full p-2 border border-gray-300 rounded-md text-sm mb-2 focus:ring-1 focus:ring-teal-500 focus:border-teal-500" rows="3" placeholder="댓글 수정..."></textarea>
            <div class="flex justify-end space-x-2 mt-1">
              <button @click="saveEditedComment()" class="text-xs font-medium text-green-600 hover:text-green-700 px-3 py-1 rounded hover:bg-green-50 focus:outline-none focus:ring-1 focus:ring-green-500">저장</button>
              <button @click="cancelEditComment" class="text-xs font-medium text-gray-500 hover:text-gray-700 px-3 py-1 rounded hover:bg-gray-100 focus:outline-none focus:ring-1 focus:ring-gray-400">취소</button>
            </div>
          </template>
          <template v-else>
            <!-- View Mode -->
            <p class="text-gray-700 text-sm leading-relaxed whitespace-pre-wrap">{{ comment.content }}</p> <!-- Added whitespace-pre-wrap -->
            <div class="flex justify-end space-x-3 mt-3">
              <template v-if="comment.user_id === authStore.user?.id">
                <button 
                  class="text-xs font-medium text-blue-600 hover:text-blue-700 hover:underline"
                  @click="startEditComment(comment)"
                >
                  수정
                </button>
                <button 
                  class="text-xs font-medium text-red-600 hover:text-red-700 hover:underline"
                  @click="handleDeleteComment(comment.id)"
                >
                  삭제
                </button>
              </template>
            </div>
          </template>
          </div>
        </div>
      <form id="addCommentForm" class="mt-8 pt-6 border-t" @submit.prevent="handleSubmitComment">
        <h3 class="text-lg font-semibold text-gray-700 mb-3">댓글 남기기</h3>
        <textarea v-model="newCommentContent" 
                  class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500 mb-3 text-sm" 
                  placeholder="여기에 댓글을 작성하세요..." rows="4" required :disabled="!isLoggedIn"></textarea>
        <button type="submit" class="bg-teal-600 text-white py-2.5 px-5 rounded-lg hover:bg-teal-700 text-sm font-medium transition-colors" :disabled="!isLoggedIn">댓글 등록</button>
        <p v-if="!isLoggedIn" class="text-red-600 text-xs mt-2">댓글을 작성하려면 로그인이 필요합니다.</p>
      </form>
    </div>
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
  <!-- <Footer /> Removed -->
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
// import Footer from '@/components/footer.vue'; // Removed import
import { useAuthStore } from '@/stores/user.js';
import api from '@/api/axios';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const post = ref(null);
const comments = ref([]);
const newCommentContent = ref('');
const loading = ref(true);
const error = ref(null);
const showLoginRequiredModal = ref(false);

const editingCommentId = ref(null);
const editingCommentContent = ref('');

const isLoggedIn = computed(() => authStore.isLoggedIn);
const postId = computed(() => route.params.id);

const fetchPostDetail = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await api.get(`/api/boards/posts/${postId.value}/`);
    post.value = response.data;
    comments.value = response.data.comments || [];
  } catch (err) {
    console.error('Error fetching post detail:', err);
    error.value = '게시글을 불러오는 데 실패했습니다. 해당 게시글이 없거나 오류가 발생했습니다.';
    if (err.response && err.response.status === 404) {
        error.value = '해당 게시글을 찾을 수 없습니다.';
    }
  } finally {
    loading.value = false;
  }
};

const toggleLike = async () => {
  if (!isLoggedIn.value) { showLoginRequiredModal.value = true; return; }
  try {
    const response = await api.post(`/api/boards/posts/${post.value.id}/like/`);
    post.value.is_liked = response.data.is_liked; // Assuming API returns updated post or just like status
    post.value.likes_count = response.data.likes_count;
  } catch (err) {
    console.error('Error toggling like:', err);
    alert('좋아요 처리에 실패했습니다.');
  }
};

const toggleBookmark = async () => {
  if (!isLoggedIn.value) { showLoginRequiredModal.value = true; return; }
  try {
    const response = await api.post(`/api/boards/posts/${post.value.id}/bookmark/`);
    post.value.is_bookmarked = response.data.is_bookmarked; // Assuming API returns updated post or just bookmark status
    post.value.bookmarks_count = response.data.bookmarks_count;
  } catch (err) {
    console.error('Error toggling bookmark:', err);
    alert('북마크 처리에 실패했습니다.');
  }
};

const handleDeletePost = async () => {
  if (!isLoggedIn.value) { showLoginRequiredModal.value = true; return; }
  if (confirm('정말로 이 게시글을 삭제하시겠습니까?')) {
    try {
      await api.delete(`/api/boards/posts/${post.value.id}/`);
      alert('게시글이 성공적으로 삭제되었습니다.');
      router.push({ name: 'board-list' });
    } catch (err) {
      console.error('Error deleting post:', err);
      alert('게시글 삭제에 실패했습니다.');
    }
  }
};

const handleSubmitComment = async () => {
  if (!isLoggedIn.value) { showLoginRequiredModal.value = true; return; }
  if (!newCommentContent.value.trim()) {
    alert('댓글 내용을 입력해주세요.');
    return;
  }
  try {
    const response = await api.post(`/api/boards/posts/${post.value.id}/comments/`, { content: newCommentContent.value });
    comments.value.push(response.data); // Add new comment to the list
    newCommentContent.value = '';
    // Optionally, re-fetch post to update comment count if not handled by API response
    // await fetchPostDetail(); 
    alert('댓글이 성공적으로 등록되었습니다.');
  } catch (err) {
    console.error('Error submitting comment:', err);
    alert('댓글 등록에 실패했습니다.');
  }
};

const startEditComment = (commentToEdit) => {
  if (!isLoggedIn.value) {
    showLoginRequiredModal.value = true;
    return;
  }
  editingCommentId.value = commentToEdit.id;
  editingCommentContent.value = commentToEdit.content;
};

const cancelEditComment = () => {
  editingCommentId.value = null;
  editingCommentContent.value = '';
};

const saveEditedComment = async () => {
  if (!editingCommentId.value) { // Check if an edit is actually in progress
    alert('수정할 댓글이 선택되지 않았습니다.');
    return;
  }
  if (!editingCommentContent.value.trim()) {
    alert('댓글 내용이 비어있습니다.');
    return;
  }
  if (!isLoggedIn.value) {
    showLoginRequiredModal.value = true;
    return;
  }
  try {
    await api.put(`/api/boards/posts/${post.value.id}/comments/${editingCommentId.value}/`, { content: editingCommentContent.value });
    await fetchPostDetail(); 
    // alert('댓글이 성공적으로 수정되었습니다.'); // Removed alert
    editingCommentId.value = null; 
    editingCommentContent.value = '';
  } catch (err) {
    console.error('Error saving edited comment:', err.response?.data || err.message);
    alert('댓글 수정에 실패했습니다. 내용을 확인하거나 다시 시도해주세요.');
  }
};

const handleDeleteComment = async (commentId) => {
  if (!isLoggedIn.value) { showLoginRequiredModal.value = true; return; }
  if (confirm('정말로 이 댓글을 삭제하시겠습니까?')) {
    try {
      await api.delete(`/api/boards/posts/${post.value.id}/comments/${commentId}/`);
      await fetchPostDetail(); // Re-fetch to remove deleted comment
      alert('댓글이 성공적으로 삭제되었습니다.');
    }
    catch (err) {
      console.error('Error deleting comment:', err);
      alert('댓글 삭제에 실패했습니다.');
    }
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

onMounted(() => {
  fetchPostDetail();
});
</script>

<style scoped>
/* Add Tailwind's typography plugin for v-html content if not already global */
/* @import '@tailwindcss/typography'; */
.prose :where(div):not(:where([class~="not-prose"] *)) {
    /* Example to style content from v-html if needed, or use Tailwind typography */
    line-height: 1.75;
}
.prose :where(p):not(:where([class~="not-prose"] *)) {
    margin-top: 1.25em;
    margin-bottom: 1.25em;
}
</style>
