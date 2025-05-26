<template>
  <div class="content-section">
    <h2 class="text-2xl font-semibold mb-6 text-gray-800 border-b-2 border-emerald-500 pb-3">내가 작성한 활동</h2>
    <div class="mb-8">
      <h3 class="sub-section-title">내가 작성한 게시글</h3>
      <div class="space-y-4 max-h-[300px] overflow-y-auto pr-2">
        <div v-if="!myBoardPosts || myBoardPosts.length === 0" class="text-gray-500 p-4 text-center">작성한 게시글이 없습니다.</div>
        <div v-for="post in myBoardPosts" :key="post.id" class="list-item">
          <h3 class="text-emerald-600 hover:text-emerald-700"><router-link :to="{ name: 'board-detail', params: { id: post.id } }">{{ post.title }}</router-link></h3>
          <p class="content-preview text-gray-600 text-sm whitespace-pre-wrap">{{ truncateText(post.content, 100) }}</p>
          <div class="details mt-1 flex justify-between items-center">
            <p class="text-xs text-gray-500">작성일: <span>{{ formatDate(post.created_at) }}</span></p>
            <router-link :to="{ name: 'board-detail', params: { id: post.id } }" class="text-xs text-emerald-600 hover:underline font-medium">자세히 보기 &rarr;</router-link>
          </div>
        </div>
      </div>
    </div>
    <div>
      <h3 class="sub-section-title">내가 작성한 댓글</h3>
      <div class="space-y-4 max-h-[300px] overflow-y-auto pr-2">
        <div v-if="!myComments || myComments.length === 0" class="text-gray-500 p-4 text-center">작성한 댓글이 없습니다.</div>
        <div v-for="comment in myComments" :key="comment.id" class="list-item">
          <h4 class="text-gray-700">댓글 단 게시글: <router-link :to="{ name: 'board-detail', params: { id: comment.post } }" class="text-emerald-600 hover:text-emerald-700 hover:underline">{{ comment.post_title }}</router-link></h4>
          <p class="content-preview text-gray-600 text-sm whitespace-pre-wrap">{{ truncateText(comment.content, 100) }}</p>
          <div class="details mt-1 flex justify-between items-center">
            <p class="text-xs text-gray-500">작성일: <span>{{ formatDate(comment.created_at) }}</span></p>
            <router-link :to="{ name: 'board-detail', params: { id: comment.post } }" class="text-xs text-emerald-600 hover:underline font-medium">원문 보기 &rarr;</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { useAuthStore } from '@/stores/user';
import { storeToRefs } from 'pinia';

const authStore = useAuthStore();
const { user: authUser, isLoggedIn } = storeToRefs(authStore);

const myBoardPosts = ref([]);
const myComments = ref([]);

const formatDate = (dateString, includeTime = false) => {
  if (!dateString) return '';
  const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
  if (includeTime) {
    options.hour = '2-digit';
    options.minute = '2-digit';
  }
  return new Date(dateString).toLocaleDateString('ko-KR', options);
};

const truncateText = (text, maxLength = 100) => {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};

const updateActivities = (newUser) => {
  if (newUser) {
    myBoardPosts.value = newUser.authored_posts || [];
    myComments.value = newUser.authored_comments || [];
  } else {
    myBoardPosts.value = [];
    myComments.value = [];
  }
};

watch(authUser, (newUser) => {
  updateActivities(newUser);
}, { immediate: true, deep: true });

onMounted(async () => {
  if (isLoggedIn.value && !authUser.value) {
    await authStore.loadUser(); // Watcher will update activities
  } else {
    updateActivities(authUser.value); // Populate if already loaded
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
.list-item {
    background-color: #f9fafb; /* gray-50 */
    padding: 1rem; /* p-4 */
    border: 1px solid #e5e7eb; /* border-gray-200 */
    border-radius: 0.5rem; /* rounded-lg */
    transition: box-shadow 0.2s ease-in-out;
    margin-bottom: 1rem; /* Added for spacing between items */
}
.list-item:hover {
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06); /* shadow-md */
}
.list-item h3 { /* For post titles */
    font-size: 1.125rem; /* text-lg */
    font-weight: 600; /* font-semibold */
    /* color: #14b8a6; */ /* Let router-link handle color */
    margin-bottom: 0.25rem;
}
.list-item h4 { /* For comment's post title */
    font-size: 0.95rem; /* Adjusted from MyPage.vue for consistency */
    font-weight: 500;
    /* color: #374151; */ /* Let router-link handle color */
    margin-bottom: 0.25rem;
}
.list-item p.content-preview {
    font-size: 0.875rem; /* text-sm */
    /* color: #4b5563; */ /* text-gray-600 */
    margin-bottom: 0.5rem;
}
.list-item .details {
    margin-top: 0.5rem; /* mt-2 */
}
.list-item .details span {
    font-weight: 500; /* font-medium */
    color: #1f2937; /* text-gray-800 */
}
.sub-section-title {
    font-size: 1.25rem; /* text-xl */
    font-weight: 600; /* font-semibold */
    color: #374151; /* text-gray-700 */
    padding-bottom: 0.5rem; /* pb-2 */
    border-bottom: 1px solid #d1d5db; /* border-b border-gray-300 */
    margin-bottom: 1rem; /* mb-4 */
}
.max-h-\[300px\] { /* Ensure this class is available or define it */
  max-height: 300px;
}
</style>
