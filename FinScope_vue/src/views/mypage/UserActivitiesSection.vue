<template>
  <div class="content-section p-6 sm:p-8">
    <h2 class="text-2xl font-bold text-primary-light mb-6 pb-3 border-b-2 border-primary-dark">내가 작성한 활동</h2>
    <div class="mb-10">
      <h3 class="sub-section-title-alt-dark-local">내가 작성한 게시글</h3>
      <div class="space-y-4 max-h-[300px] overflow-y-auto pr-3 custom-scrollbar-dark-local">
        <div v-if="!myBoardPosts || myBoardPosts.length === 0" class="text-gray-400 p-6 text-center bg-gray-700 rounded-md">작성한 게시글이 없습니다.</div>
        <div v-for="post in myBoardPosts" :key="post.id" class="list-item-card-dark-local">
          <h3 class="text-lg font-semibold text-primary-light hover:text-primary mb-1"><router-link :to="{ name: 'board-detail', params: { id: post.id } }">{{ post.title }}</router-link></h3>
          <p class="text-sm text-gray-300 mb-2 whitespace-pre-wrap leading-relaxed">{{ truncateText(post.content, 120) }}</p>
          <div class="flex justify-between items-center text-xs">
            <p class="text-gray-400">작성일: <span class="font-medium text-gray-200">{{ formatDate(post.created_at) }}</span></p>
            <router-link :to="{ name: 'board-detail', params: { id: post.id } }" class="text-primary-light hover:underline font-medium">자세히 보기 &rarr;</router-link>
          </div>
        </div>
      </div>
    </div>
    <div>
      <h3 class="sub-section-title-alt-dark-local">내가 작성한 댓글</h3>
      <div class="space-y-4 max-h-[300px] overflow-y-auto pr-3 custom-scrollbar-dark-local">
        <div v-if="!myComments || myComments.length === 0" class="text-gray-400 p-6 text-center bg-gray-700 rounded-md">작성한 댓글이 없습니다.</div>
        <div v-for="comment in myComments" :key="comment.id" class="list-item-card-dark-local">
          <h4 class="text-sm font-medium text-gray-300 mb-1">댓글 단 게시글: <router-link :to="{ name: 'board-detail', params: { id: comment.post } }" class="text-primary-light hover:text-primary hover:underline">{{ comment.post_title }}</router-link></h4>
          <p class="text-sm text-gray-300 mb-2 whitespace-pre-wrap leading-relaxed">{{ truncateText(comment.content, 120) }}</p>
          <div class="flex justify-between items-center text-xs">
            <p class="text-gray-400">작성일: <span class="font-medium text-gray-200">{{ formatDate(comment.created_at) }}</span></p>
            <router-link :to="{ name: 'board-detail', params: { id: comment.post } }" class="text-primary-light hover:underline font-medium">원문 보기 &rarr;</router-link>
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

/* Dark Theme List Item Card Styling specific to this component */
.list-item-card-dark-local {
  @apply bg-gray-900 p-4 rounded-lg border border-gray-700 shadow-md hover:shadow-lg transition-shadow duration-200;
}

/* Dark Theme Sub-section Title specific to this component */
.sub-section-title-alt-dark-local {
  @apply text-lg font-semibold text-gray-200 mb-3 pb-2 border-b border-gray-700;
}

/* Dark Theme Custom Scrollbar specific to this component */
.custom-scrollbar-dark-local::-webkit-scrollbar {
  width: 8px;
}
.custom-scrollbar-dark-local::-webkit-scrollbar-track {
  background: #1f2937; /* gray-800 or a slightly darker shade than content bg */
  border-radius: 10px;
}
.custom-scrollbar-dark-local::-webkit-scrollbar-thumb {
  background: #4b5563; /* gray-600 */
  border-radius: 10px;
}
.custom-scrollbar-dark-local::-webkit-scrollbar-thumb:hover {
  background: #6b7280; /* gray-500 */
}

.max-h-\[300px\] { 
  max-height: 300px;
}
</style>
