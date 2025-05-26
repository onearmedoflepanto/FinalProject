<template>
  <div id="postDetailSection" class="board-section bg-white p-6 md:p-8 rounded-xl shadow-xl border border-gray-200">
    <div class="flex justify-between items-center mb-4">
      <h1 id="detailPostTitle" class="text-2xl md:text-3xl font-bold text-teal-700">{{ post.title }}</h1>
      <button id="backToListBtnFromDetail" class="bg-gray-500 text-white py-2 px-4 rounded-lg hover:bg-gray-600 text-sm" @click.prevent="handleBackToList">
        목록으로
      </button>
    </div>
    <div class="post-detail-header text-sm text-gray-500">
      <p>작성자: <span id="detailPostAuthor" class="font-medium text-gray-700">{{ post.author }}</span></p>
      <p>작성일: <span id="detailPostDate" class="font-medium text-gray-700">{{ formatDate(post.created_at) }}</span></p>
      <p>조회수: <span id="detailPostViews" class="font-medium text-gray-700">{{ post.views }}</span></p>
    </div>
    <div id="detailPostContent" class="post-detail-content mt-6 mb-8" v-html="post.content"></div>
    
    <div class="flex items-center space-x-4 mb-6">
      <button 
        :class="['flex items-center space-x-1 px-3 py-1.5 rounded-full text-sm font-medium transition-colors duration-200', post.is_liked ? 'bg-red-500 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300']"
        @click="$emit('toggle-like', post.id)"
        :disabled="!isLoggedIn"
      >
        <svg :class="['w-4 h-4', post.is_liked ? 'fill-current' : '']" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" />
        </svg>
        <span>{{ post.likes_count }}</span>
      </button>
      <button 
        :class="['flex items-center space-x-1 px-3 py-1.5 rounded-full text-sm font-medium transition-colors duration-200', post.is_bookmarked ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300']"
        @click="$emit('toggle-bookmark', post.id)"
        :disabled="!isLoggedIn"
      >
        <svg :class="['w-4 h-4', post.is_bookmarked ? 'fill-current' : '']" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path d="M5 4a2 2 0 012-2h6a2 2 0 012 2v14l-5-2.5L5 18V4z" />
        </svg>
        <span>{{ post.bookmarks_count }}</span>
      </button>
      <template v-if="post.author_id === authStore.user?.id">
        <button 
          class="bg-yellow-500 text-white py-1.5 px-3 rounded-lg hover:bg-yellow-600 text-sm font-medium"
          @click="$emit('edit-post', post.id)"
        >
          수정
        </button>
        <button 
          class="bg-red-500 text-white py-1.5 px-3 rounded-lg hover:bg-red-600 text-sm font-medium"
          @click="$emit('delete-post', post.id)"
        >
          삭제
        </button>
      </template>
    </div>

    <div class="comments-section">
      <h2 class="text-xl font-semibold text-gray-800 mb-4">댓글 ({{ post.comments_count }})</h2>
      <div id="detailPostComments" class="space-y-4">
        <div v-if="comments.length === 0" class="text-sm text-gray-500">아직 댓글이 없습니다.</div>
        <div v-for="comment in comments" :key="comment.id" class="bg-gray-50 p-4 rounded-lg border border-gray-200">
          <p class="font-semibold text-gray-700 text-sm">{{ comment.user }}</p>
          <p class="text-xs text-gray-500 mb-1">{{ formatDate(comment.created_at, true) }}</p>
          <p class="text-gray-600 text-sm">{{ comment.content }}</p>
          <div class="flex justify-end space-x-2 mt-2">
            <template v-if="comment.user_id === authStore.user?.id">
              <button 
                class="text-blue-500 hover:text-blue-700 text-xs"
                @click="$emit('edit-comment', comment)"
              >
                수정
              </button>
              <button 
                class="text-red-500 hover:text-red-700 text-xs"
                @click="$emit('delete-comment', comment.id)"
              >
                삭제
              </button>
            </template>
          </div>
        </div>
      </div>
      <form id="addCommentForm" class="mt-6" @submit.prevent="$emit('submit-comment', newCommentContent)">
        <textarea v-model="newCommentContent" class="form-textarea mb-2" placeholder="댓글을 입력하세요..." rows="3" required :disabled="!isLoggedIn"></textarea>
        <button type="submit" class="bg-teal-600 text-white py-2 px-4 rounded-lg hover:bg-teal-700 text-sm" :disabled="!isLoggedIn">댓글 등록</button>
        <p v-if="!isLoggedIn" class="text-red-500 text-sm mt-2">댓글을 작성하려면 로그인이 필요합니다.</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useAuthStore } from '../stores/user.js';
import { useRouter } from 'vue-router'; // Import useRouter

const props = defineProps({
  post: {
    type: Object,
    required: true,
  },
  comments: {
    type: Array,
    required: true,
  },
  onBackToList: { // Add new prop for the function
    type: Function,
    required: true,
  }
});

const emit = defineEmits([
  // 'back-to-list', // Remove this as we are using a direct prop call
  'toggle-like',
  'toggle-bookmark',
  'edit-post',
  'delete-post',
  'submit-comment',
  'edit-comment',
  'delete-comment',
]);

const authStore = useAuthStore();
const router = useRouter(); // Get router instance
const isLoggedIn = computed(() => authStore.isLoggedIn);
const newCommentContent = ref('');

const handleBackToList = () => {
  if (props.onBackToList) {
    props.onBackToList();
  }
  // router.push('/board'); // Force navigation to /board - Replaced by prop call
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
</script>
