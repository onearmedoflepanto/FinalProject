<template>
  <div class="bg-gray-900 text-gray-100 min-h-screen py-6 md:py-8">
    <main class="flex-grow container mx-auto px-4 sm:px-6">
      <div id="postListSection" class="board-section bg-gray-800 p-4 md:p-6 rounded-xl border border-gray-700" v-if="currentSection === 'postListSection'">
        <div class="flex justify-between items-center mb-8">
          <h1 class="text-3xl md:text-4xl font-bold text-primary-light">자유 게시판</h1>
          <button id="createPostBtn"
            class="bg-primary hover:bg-primary-dark text-white font-semibold py-2.5 px-5 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-light focus:ring-opacity-75 transition duration-150 ease-in-out text-base"
            @click="showCreatePostForm">
          글쓰기
        </button>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full table-fixed">
          <thead>
            <tr class="border-b border-gray-700">
              <th class="py-3 px-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider w-1/12">번호</th>
              <th class="py-3 px-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider w-6/12">제목</th>
              <th class="py-3 px-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider w-2/12">작성자</th>
              <th class="py-3 px-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider w-2/12">작성일</th>
              <th class="py-3 px-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider w-1/12">조회수</th>
            </tr>
          </thead>
          <tbody id="postList" class="divide-y divide-gray-700">
            <tr v-if="posts.length === 0">
              <td colspan="5" class="py-12 text-center text-gray-500 text-lg">게시글이 없습니다. 새로운 글을 작성해보세요!</td>
            </tr>
            <tr v-for="post in posts" :key="post.id" class="hover:bg-gray-700/50 transition-colors duration-150">
              <td class="py-4 px-4 whitespace-nowrap text-sm text-gray-300 w-1/12">{{ post.id }}</td>
              <td class="py-4 px-4 whitespace-nowrap text-sm text-gray-100 w-6/12 truncate">
                <a href="#" class="text-sky-400 hover:text-sky-300 hover:underline font-medium"
                  @click.prevent="showPostDetail(post.id)">
                  {{ post.title }}
                  <span v-if="post.comments_count > 0" class="text-xs text-gray-400 ml-1">[{{ post.comments_count
                  }}]</span>
                </a>
              </td>
              <td class="py-4 px-4 whitespace-nowrap text-sm text-gray-300 w-2/12">{{ post.author_nickname ||
                post.author }}</td>
              <td class="py-4 px-4 whitespace-nowrap text-sm text-gray-300 w-2/12">{{ formatDate(post.created_at) }}
              </td>
              <td class="py-4 px-4 whitespace-nowrap text-sm text-gray-300 w-1/12">{{ post.views }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="mt-8 flex justify-center items-center pagination">
        <!-- Pagination controls will go here if implemented -->
      </div>
    </div>

    <PostDetail v-if="currentSection === 'postDetailSection'" :post="currentPost" :comments="comments" 
      :on-back-to-list="showPostList" @toggle-like="toggleLike"
      @toggle-bookmark="toggleBookmark" @edit-post="editPost"
      @delete-post="deletePost" @submit-comment="submitComment" @edit-comment="editComment"
      @delete-comment="deleteComment" />

    <div id="postFormSection" class="board-section bg-gray-800 p-6 md:p-8 rounded-xl shadow-xl border border-gray-700"
      v-if="currentSection === 'postFormSection'">
      <h1 id="postFormTitle" class="text-2xl md:text-3xl font-bold text-primary-light mb-6">{{ formModeTitle }}</h1>
      <form id="postForm" @submit.prevent="submitPost">
        <div class="mb-4">
          <label for="postTitleInput" class="block text-sm font-medium text-gray-300 mb-1">제목</label>
          <input type="text" id="postTitleInput" v-model="postForm.title" class="form-input-dark" required>
        </div>
        <div class="mb-6">
          <label for="postContentInput" class="block text-sm font-medium text-gray-300 mb-1">내용</label>
          <textarea id="postContentInput" v-model="postForm.content" class="form-textarea-dark" rows="10"
            required></textarea>
        </div>
        <div class="flex justify-end space-x-3">
          <button type="button" id="cancelPostBtn"
            class="bg-gray-600 text-gray-300 py-2 px-4 rounded-lg hover:bg-gray-500" @click="showPostList">취소</button>
          <button type="submit" id="submitPostBtn"
            class="bg-primary hover:bg-primary-dark text-white py-2 px-4 rounded-lg">{{ formMode === 'create' ? '등록' :
              '수정'
            }}</button>
          </div>
        </form>
      </div>

      <div id="loginRequiredSection"
        class="board-section bg-gray-800 p-6 md:p-8 rounded-xl shadow-xl border border-gray-700 text-center"
        v-if="currentSection === 'loginRequiredSection'">
        <h2 class="text-xl font-semibold text-red-400 mb-4">로그인 필요</h2>
        <p class="text-gray-300 mb-6">글을 작성하거나 댓글을 달려면 로그인이 필요합니다.</p>
        <router-link to="/login" class="bg-primary hover:bg-primary-dark text-white py-2 px-6 rounded-lg text-sm">로그인 페이지로
          이동</router-link>
        <button id="closeLoginRequiredBtn" class="mt-4 text-sm text-gray-400 hover:text-gray-200 underline"
          @click="showPostList">닫기</button>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import NavigationBar from '../components/NavigationBar.vue';
import Footer from '../components/footer.vue';
import PostDetail from '../components/PostDetail.vue'; // Import PostDetail
import { useAuthStore } from '../stores/user.js';
import api from '../api/axios'; // Changed from 'axios'

const authStore = useAuthStore();
const isLoggedIn = computed(() => authStore.isLoggedIn);

const posts = ref([]);
const currentPost = ref({});
const comments = ref([]);
// const newCommentContent = ref(''); // Removed as it's managed by PostDetail
const postForm = reactive({
  id: null,
  title: '',
  content: '',
});
const formMode = ref('create'); // 'create' or 'edit'

const currentSection = ref('postListSection'); // Controls which section is visible

// Pagination state
const totalPosts = ref(0);
const currentPage = ref(1);
// const pageSize = 10; // Removed as not used directly, totalPages was also removed
const nextUrl = ref(null);
const previousUrl = ref(null);

const formModeTitle = computed(() => {
  return formMode.value === 'create' ? '새 글 작성' : '글 수정';
});

const showBoardSection = (sectionId) => {
  console.log('[Board.vue] showBoardSection called with:', sectionId);
  console.log('[Board.vue] currentSection BEFORE change:', currentSection.value);
  currentSection.value = sectionId;
  console.log('[Board.vue] currentSection AFTER change:', currentSection.value);
};

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

const showCreatePostForm = () => {
  if (!isLoggedIn.value) {
    showBoardSection('loginRequiredSection');
    return;
  }
  formMode.value = 'create';
  postForm.id = null;
  postForm.title = '';
  postForm.content = '';
  showBoardSection('postFormSection');
};

const showPostDetail = async (postId) => {
  try {
    const response = await api.get(`/api/boards/posts/${postId}/`);
    currentPost.value = response.data;
    comments.value = response.data.comments; // Assuming comments are nested
    showBoardSection('postDetailSection');
  } catch (error) {
    console.error('Error fetching post detail:', error);
    alert('게시글 상세 정보를 불러오는 데 실패했습니다.');
  }
};

const showPostList = () => {
  console.log('[Board.vue] showPostList called');
  fetchPosts(currentPage.value); // Restore fetchPosts call
  showBoardSection('postListSection');
  console.log('[Board.vue] showPostList finished');
};

const submitPost = async () => {
  try {
    if (formMode.value === 'create') {
      await api.post('/api/boards/posts/', postForm);
      alert('게시글이 성공적으로 등록되었습니다.');
    } else { // edit mode
      await api.put(`/api/boards/posts/${postForm.id}/`, postForm);
      alert('게시글이 성공적으로 수정되었습니다.');
    }
    showPostList();
  } catch (error) {
    console.error('Error submitting post:', error);
    alert('게시글 등록/수정에 실패했습니다.');
  }
};

const editPost = (postId) => {
  const postToEdit = posts.value.find(p => p.id === postId);
  if (postToEdit) {
    formMode.value = 'edit';
    postForm.id = postToEdit.id;
    postForm.title = postToEdit.title;
    postForm.content = postToEdit.content;
    showBoardSection('postFormSection');
  }
};

const deletePost = async (postId) => {
  if (confirm('정말로 이 게시글을 삭제하시겠습니까?')) {
    try {
      await api.delete(`/api/boards/posts/${postId}/`);
      alert('게시글이 성공적으로 삭제되었습니다.');
      showPostList();
    } catch (error) {
      console.error('Error deleting post:', error);
      alert('게시글 삭제에 실패했습니다.');
    }
  }
};

const submitComment = async (content) => { // Receive content from emitted event
  if (!isLoggedIn.value) {
    showBoardSection('loginRequiredSection');
    return;
  }
  if (!content.trim()) {
    alert('댓글 내용을 입력해주세요.');
    return;
  }
  try {
    await api.post(`/api/boards/posts/${currentPost.value.id}/comments/`, { content: content });
    // newCommentContent.value = ''; // This is now managed by PostDetail
    showPostDetail(currentPost.value.id); // Refresh post detail to show new comment
    alert('댓글이 성공적으로 등록되었습니다.');
  } catch (error) {
    console.error('Error submitting comment:', error);
    alert('댓글 등록에 실패했습니다.');
  }
};

const editComment = async (comment) => {
  const newContent = prompt('댓글을 수정하세요:', comment.content);
  if (newContent !== null && newContent.trim() !== '') {
    try {
      await api.put(`/api/boards/posts/${currentPost.value.id}/comments/${comment.id}/`, { content: newContent });
      showPostDetail(currentPost.value.id); // Refresh post detail
      alert('댓글이 성공적으로 수정되었습니다.');
    } catch (error) {
      console.error('Error editing comment:', error);
      alert('댓글 수정에 실패했습니다.');
    }
  }
};

const deleteComment = async (commentId) => {
  if (confirm('정말로 이 댓글을 삭제하시겠습니까?')) {
    try {
      await api.delete(`/api/boards/posts/${currentPost.value.id}/comments/${commentId}/`);
      showPostDetail(currentPost.value.id); // Refresh post detail
      alert('댓글이 성공적으로 삭제되었습니다.');
    }
    catch (error) {
      console.error('Error deleting comment:', error);
      alert('댓글 삭제에 실패했습니다.');
    }
  }
};

const toggleLike = async (postId) => {
  if (!isLoggedIn.value) {
    showBoardSection('loginRequiredSection');
    return;
  }
  try {
    const response = await api.post(`/api/boards/posts/${postId}/like/`, {});
    currentPost.value = response.data; // Update local post data
  } catch (error) {
    console.error('Error toggling like:', error);
    alert('좋아요 처리에 실패했습니다.');
  }
};

const toggleBookmark = async (postId) => {
  if (!isLoggedIn.value) {
    showBoardSection('loginRequiredSection');
    return;
  }
  try {
    const response = await api.post(`/api/boards/posts/${postId}/bookmark/`, {});
    currentPost.value = response.data; // Update local post data
  } catch (error) {
    console.error('Error toggling bookmark:', error);
    alert('북마크 처리에 실패했습니다.');
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

// Pagination methods
// const totalPages = computed(() => Math.ceil(totalPosts.value / pageSize)); // Removed as not used in template

// const goToPage = (page) => { // Removed as not used in template
//   if (page >= 1 && page <= totalPages.value) {
//     fetchPosts(page);
//   }
// };

// const nextPage = () => { // Removed as not used in template
//   if (nextUrl.value) {
//     const url = new URL(nextUrl.value);
//     const page = url.searchParams.get('page');
//     fetchPosts(parseInt(page));
//   }
// };

// const previousPage = () => { // Removed as not used in template
//   if (previousUrl.value) {
//     const url = new URL(previousUrl.value);
//     const page = url.searchParams.get('page');
//     fetchPosts(parseInt(page));
//   }
// };

onMounted(() => {
  fetchPosts();
});
</script>
