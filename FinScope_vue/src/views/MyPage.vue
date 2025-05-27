<template>
  <!-- MyPage Root Template - Dark Theme v2 -->
  <main class="flex-grow container mx-auto px-4 sm:px-6 py-10 md:py-16 bg-gray-900 text-gray-100 min-h-screen">
    <h1 class="text-4xl md:text-5xl font-extrabold mb-10 md:mb-12 text-center text-primary-light">
      <span>{{ userProfileName }}</span>님의 마이페이지
    </h1>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
      <!-- Sidebar Navigation -->
      <div class="lg:col-span-3 bg-gray-800 p-6 rounded-lg shadow-xl flex flex-col">
        <h2 class="text-xl font-semibold mb-6 text-gray-200 border-b border-gray-700 pb-3">계정 관리</h2>
        <nav class="space-y-2">
          <button 
            @click="showSection('userInfoDisplaySection')" 
            :class="['sidebar-button', activeSection === 'userInfoDisplaySection' ? 'sidebar-button-active-primary' : 'sidebar-button-inactive-dark', { hidden: activeSection === 'userInfoEditSection' }]"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" /></svg>
            기본 정보 보기
          </button>
          <button 
            @click="showSection('userInfoEditSection')" 
            :class="['sidebar-button', activeSection === 'userInfoEditSection' ? 'sidebar-button-active-primary' : 'sidebar-button-inactive-dark', { hidden: activeSection === 'userInfoEditSection' }]"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" viewBox="0 0 20 20" fill="currentColor"><path d="M17.414 2.586a2 2 0 00-2.828 0L7 10.172V13h2.828l7.586-7.586a2 2 0 000-2.828z" /><path fill-rule="evenodd" d="M2 6a2 2 0 012-2h4a1 1 0 010 2H4v10h10v-4a1 1 0 112 0v4a2 2 0 01-2 2H4a2 2 0 01-2-2V6z" clip-rule="evenodd" /></svg>
            기본 정보 수정
          </button>
          <button 
            @click="showSection('savedProductsSection')" 
            :class="['sidebar-button', activeSection === 'savedProductsSection' ? 'sidebar-button-active-primary' : 'sidebar-button-inactive-dark']"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" viewBox="0 0 20 20" fill="currentColor"><path d="M5 4a2 2 0 012-2h6a2 2 0 012 2v14l-5-3.03L5 18V4z" /></svg>
            저장한 상품
          </button>
          <button 
            @click="showSection('myPostsSection')" 
            :class="['sidebar-button', activeSection === 'myPostsSection' ? 'sidebar-button-active-primary' : 'sidebar-button-inactive-dark']"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a1 1 0 110 2h-3a1 1 0 01-1-1v-2a1 1 0 00-1-1H9a1 1 0 00-1 1v2a1 1 0 01-1 1H5a1 1 0 110-2V4zm3 1h2v2H7V5zm2 4H7v2h2V9zm2-4h2v2h-2V5zm2 4h-2v2h2V9z" clip-rule="evenodd" /></svg>
            내가 작성한 글
          </button>
        </nav>
      </div>

      <!-- Content Area -->
      <div class="lg:col-span-9 bg-gray-800 p-6 sm:p-8 rounded-lg shadow-xl">
        <div v-if="activeSection === 'userInfoDisplaySection'" class="content-section animate-fadeIn">
          <h2 class="section-title-dark border-primary-dark">기본 정보</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-6">
            <div><label class="info-label-dark">아이디</label><p class="info-value-dark">{{ userData.userId }}</p></div>
            <div><label class="info-label-dark">이메일</label><p class="info-value-dark">{{ userData.email }}</p></div>
            <div><label class="info-label-dark">닉네임</label><p class="info-value-dark">{{ userData.nickname }}</p></div>
            <div><label class="info-label-dark">나이</label><p class="info-value-dark">{{ userData.age || '정보 없음' }}</p></div>
            <div><label class="info-label-dark">현재 가진 금액 (원)</label><p class="info-value-dark">{{ formatCurrency(userData.assets) }}</p></div>
            <div><label class="info-label-dark">연봉 (원)</label><p class="info-value-dark">{{ formatCurrency(userData.salary) }}</p></div>
            <div><label class="info-label-dark">저축 성향</label><p class="info-value-dark">{{ userData.savingsTendency }}</p></div>
          </div>
        </div>

        <div v-if="activeSection === 'userInfoEditSection'" class="content-section animate-fadeIn">
          <h2 class="section-title-dark border-primary-dark">기본 정보 수정</h2>
          <form @submit.prevent="handleProfileEditSubmit" class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4">
              <div><label for="editUserId" class="form-label-dark">아이디</label><input type="text" id="editUserId" :value="editData.userId" class="form-input-dark bg-gray-700 cursor-not-allowed" readonly></div>
              <div><label for="editUserEmail" class="form-label-dark">이메일</label><input type="email" id="editUserEmail" v-model="editData.email" class="form-input-dark" required></div>
              <div><label for="editUserNickname" class="form-label-dark">닉네임</label><input type="text" id="editUserNickname" v-model="editData.nickname" class="form-input-dark" required></div>
              <div><label for="editUserAge" class="form-label-dark">나이</label><input type="number" id="editUserAge" v-model.number="editData.age" class="form-input-dark" placeholder="숫자만 입력"></div>
              <div><label for="editUserAssets" class="form-label-dark">현재 가진 금액 (원)</label><input type="number" id="editUserAssets" v-model.number="editData.assets" class="form-input-dark" placeholder="숫자만 입력" required></div>
              <div><label for="editUserSalary" class="form-label-dark">연봉 (원)</label><input type="number" id="editUserSalary" v-model.number="editData.salary" class="form-input-dark" placeholder="숫자만 입력"></div>
              <div><label for="editUserSavingsTendency" class="form-label-dark">저축 성향</label>
                <select id="editUserSavingsTendency" v-model="editData.savingsTendency" class="form-select-dark">
                  <option disabled value="">선택하세요</option>
                  <option value="알뜰형">알뜰형</option>
                  <option value="균형형">균형형</option>
                  <option value="도전형">도전형</option>
                </select>
              </div>
            </div>
            <hr class="my-6 border-gray-700">
            <h3 class="text-lg font-semibold text-gray-300">비밀번호 변경</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4">
              <div><label for="editCurrentPassword" class="form-label-dark">현재 비밀번호</label><input type="password" id="editCurrentPassword" v-model="editData.currentPassword" class="form-input-dark" placeholder="현재 비밀번호 입력"></div>
              <div><label for="editNewPassword" class="form-label-dark">새 비밀번호</label><input type="password" id="editNewPassword" v-model="editData.newPassword" class="form-input-dark" placeholder="새 비밀번호 (8자 이상)"></div>
              <div><label for="editConfirmNewPassword" class="form-label-dark">새 비밀번호 확인</label><input type="password" id="editConfirmNewPassword" v-model="editData.confirmNewPassword" class="form-input-dark" placeholder="새 비밀번호 다시 입력"></div>
            </div>
            <div class="mt-8 flex justify-end space-x-3">
              <button type="button" @click="cancelEdit" class="btn btn-secondary-dark">취소</button>
              <button type="submit" class="btn btn-primary">저장</button>
            </div>
          </form>
        </div>

        <div v-if="activeSection === 'savedProductsSection'" class="content-section animate-fadeIn">
          <h2 class="section-title-dark border-primary-dark">저장한 금융 상품</h2>
          <div class="space-y-4 mb-8 max-h-[350px] overflow-y-auto pr-3 custom-scrollbar-dark">
            <div v-if="savedProducts.length === 0" class="text-gray-400 p-6 text-center bg-gray-700 rounded-md">저장한 상품이 없습니다.</div>
            <div v-for="product in savedProducts" :key="product.id" class="list-item-card-dark">
              <h3 class="text-lg font-semibold text-primary-light mb-1">{{ product.name }}</h3>
              <div class="grid grid-cols-2 gap-x-4 gap-y-1 text-sm text-gray-300">
                <p><span class="font-medium text-gray-400">기본 금리:</span> <span class="text-gray-200">{{ product.baseRate }}%</span></p>
                <p><span class="font-medium text-gray-400">최고 금리:</span> <span class="text-gray-200">{{ product.maxRate }}% (우대)</span></p>
                <p><span class="font-medium text-gray-400">가입 기간:</span> <span class="text-gray-200">{{ product.term }}</span></p>
                <p><span class="font-medium text-gray-400">은행:</span> <span class="text-gray-200">{{ product.bank }}</span></p>
              </div>
            </div>
          </div>
          <h3 class="text-xl font-semibold mb-4 text-gray-200 mt-8">저장 상품 금리 비교</h3>
          <div class="w-full h-80 md:h-96 bg-gray-800 rounded-lg p-4 relative border border-gray-700 shadow-md">
            <canvas ref="savedProductsChartCanvas"></canvas>
            <p v-if="chartLoading" class="absolute inset-0 flex items-center justify-center text-gray-400 z-10 bg-gray-800 bg-opacity-75 rounded-lg">차트 로딩 중...</p>
          </div>
        </div>

        <div v-if="activeSection === 'myPostsSection'" class="content-section animate-fadeIn">
          <h2 class="section-title-dark border-primary-dark">내가 작성한 활동</h2>
          
          <div class="mb-10">
            <h3 class="sub-section-title-alt-dark">내가 작성한 게시글</h3>
            <div class="space-y-4 max-h-[300px] overflow-y-auto pr-3 custom-scrollbar-dark">
              <div v-if="!myBoardPosts || myBoardPosts.length === 0" class="text-gray-400 p-6 text-center bg-gray-700 rounded-md">작성한 게시글이 없습니다.</div>
              <div v-for="post in myBoardPosts" :key="post.id" class="list-item-card-dark">
                <h3 class="text-lg font-semibold text-primary-light hover:text-primary mb-1"><router-link :to="{ name: 'board-detail', params: { id: post.id } }">{{ post.title }}</router-link></h3>
                <p class="text-sm text-gray-300 mb-2 whitespace-pre-wrap leading-relaxed">{{ truncateText(post.content, 120) }}</p>
                <div class="flex justify-between items-center text-xs">
                  <p class="text-gray-400">작성일: <span class="font-medium">{{ formatDate(post.created_at) }}</span></p>
                  <router-link :to="{ name: 'board-detail', params: { id: post.id } }" class="text-primary-light hover:underline font-medium">자세히 보기 &rarr;</router-link>
                </div>
              </div>
            </div>
          </div>
          <div>
            <h3 class="sub-section-title-alt-dark">내가 작성한 댓글</h3>
            <div class="space-y-4 max-h-[300px] overflow-y-auto pr-3 custom-scrollbar-dark">
              <div v-if="!myComments || myComments.length === 0" class="text-gray-400 p-6 text-center bg-gray-700 rounded-md">작성한 댓글이 없습니다.</div>
              <div v-for="comment in myComments" :key="comment.id" class="list-item-card-dark">
                <h4 class="text-sm font-medium text-gray-300 mb-1">댓글 단 게시글: <router-link :to="{ name: 'board-detail', params: { id: comment.post } }" class="text-primary-light hover:text-primary hover:underline">{{ comment.post_title }}</router-link></h4>
                <p class="text-sm text-gray-300 mb-2 whitespace-pre-wrap leading-relaxed">{{ truncateText(comment.content, 120) }}</p>
                <div class="flex justify-between items-center text-xs">
                  <p class="text-gray-400">작성일: <span class="font-medium">{{ formatDate(comment.created_at) }}</span></p>
                  <router-link :to="{ name: 'board-detail', params: { id: comment.post } }" class="text-primary-light hover:underline font-medium">원문 보기 &rarr;</router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch, nextTick } from 'vue';
import Chart from 'chart.js/auto'; // Import Chart.js
import { useAuthStore } from '@/stores/user';
import { storeToRefs } from 'pinia';

const authStore = useAuthStore();
const { user: authUser, isLoggedIn } = storeToRefs(authStore);

// Reactive state for user data, will be populated from store
const userData = reactive({
  userId: '',
  email: '',
  nickname: '',
  age: null,
  assets: null,
  salary: null,
  savingsTendency: '',
});

// Reactive state for edit form data
const editData = reactive({
  userId: '', // Will be read-only
  email: '',
  nickname: '',
  age: null,
  assets: null,
  salary: null,
  savingsTendency: '',
  // Password fields are separate for editing
  currentPassword: '',
  newPassword: '',
  confirmNewPassword: '',
});

const userProfileName = computed(() => userData.nickname || userData.userId || '사용자');

const activeSection = ref('userInfoDisplaySection'); // Default section

// Placeholder data for lists - these will be fetched later
const savedProducts = ref([]);
const myBoardPosts = ref([]);
const myComments = ref([]);

const savedProductsChartCanvas = ref(null);
let savedProductsChartInstance = null;
const chartLoading = ref(false);

const showSection = (sectionId) => {
  activeSection.value = sectionId;
  if (sectionId === 'userInfoEditSection') {
    populateEditForm();
  }
};

const populateEditForm = () => {
  editData.userId = userData.userId;
  editData.email = userData.email;
  editData.nickname = userData.nickname;
  editData.age = userData.age;
  editData.assets = userData.assets;
  editData.salary = userData.salary;
  editData.savingsTendency = userData.savingsTendency;
  editData.currentPassword = '';
  editData.newPassword = '';
  editData.confirmNewPassword = '';
};

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

const cancelEdit = () => {
  showSection('userInfoDisplaySection');
};

const handleProfileEditSubmit = async () => { // Made this async
  // Password validation
  if (editData.newPassword || editData.confirmNewPassword || editData.currentPassword) {
    if (!editData.currentPassword) {
      alert("현재 비밀번호를 입력해주세요.");
      return;
    }
    if (editData.newPassword.length > 0 && editData.newPassword.length < 8) {
      alert("새 비밀번호는 8자 이상이어야 합니다.");
      return;
    }
    if (editData.newPassword !== editData.confirmNewPassword) {
      alert("새 비밀번호와 비밀번호 확인이 일치하지 않습니다.");
      return;
    }
    // Placeholder for actual password change logic
    if (editData.newPassword) {
        console.log("Password Change Attempt (Placeholder):", { currentPassword: editData.currentPassword, newPassword: editData.newPassword });
        alert("비밀번호가 성공적으로 변경되었습니다. (실제 변경은 백엔드 구현 필요)");
    }
  }

  // Update userData with editData
  userData.email = editData.email;
  userData.nickname = editData.nickname;
  userData.age = editData.age;
  userData.assets = editData.assets;
  userData.salary = editData.salary;
  userData.savingsTendency = editData.savingsTendency;

  console.log("Profile Updated (Placeholder):", { ...userData });
  alert("프로필 정보가 업데이트되었습니다. (실제 저장은 백엔드 연동 필요)");
  // Construct the data payload for the store action
  // Only include fields that are meant to be updated.
  // The store action will handle password fields separately.
  const profileUpdateData = {
    email: editData.email,
    nickname: editData.nickname,
    age: editData.age,
    assets: editData.assets,
    salary: editData.salary,
    savings_tendency: editData.savingsTendency, // Ensure field name matches serializer if different
    // Password fields if they are being changed:
    current_password: editData.currentPassword, // Ensure field names match what backend expects for password change
    new_password: editData.newPassword,
  };

  // Remove empty password fields so they are not sent if not being changed
  if (!profileUpdateData.current_password && !profileUpdateData.new_password) {
    delete profileUpdateData.current_password;
    delete profileUpdateData.new_password;
  } else {
    // If new password is provided, ensure current password is also there (backend might require it)
    if (profileUpdateData.new_password && !profileUpdateData.current_password) {
      alert("새 비밀번호를 변경하려면 현재 비밀번호를 입력해야 합니다.");
      return;
    }
  }


  const result = await authStore.updateUserProfile(profileUpdateData);

  if (result.success) {
    alert("프로필 정보가 성공적으로 업데이트되었습니다.");
    showSection('userInfoDisplaySection'); // Switch back to display mode
  } else {
    alert(result.message || "프로필 업데이트에 실패했습니다.");
  }
  // The local `userData` will be updated automatically by the watcher on `authUser`
};

const formatCurrency = (value) => {
  if (value === null || value === undefined || isNaN(Number(value))) return '0';
  return Number(value).toLocaleString('ko-KR');
};

const renderSavedProductsChart = async () => {
  if (!savedProductsChartCanvas.value) return;
  chartLoading.value = true;

  await nextTick(); // Ensure canvas is in the DOM

  if (savedProductsChartInstance) {
    savedProductsChartInstance.destroy();
  }

  // Simulate API call or data processing
  setTimeout(() => {
    try {
      const productNames = savedProducts.value.map(p => p.name.split(' - ')[1] || p.name); // Extract simpler names
      const baseRates = savedProducts.value.map(p => parseFloat(p.baseRate));
      const maxRates = savedProducts.value.map(p => parseFloat(p.maxRate));

      const chartTextColor = '#cbd5e1'; // slate-300 for dark theme text
      const chartGridColor = '#4b5563'; // gray-600 for dark theme grid lines

      if (productNames.length === 0) {
        chartLoading.value = false;
        const ctx = savedProductsChartCanvas.value.getContext('2d');
        ctx.clearRect(0, 0, savedProductsChartCanvas.value.width, savedProductsChartCanvas.value.height);
        ctx.textAlign = 'center';
        ctx.fillStyle = chartTextColor; // Use light text color for dark theme
        ctx.font = "16px 'Noto Sans KR', sans-serif";
        ctx.fillText('비교할 저장 상품 데이터가 없습니다.', savedProductsChartCanvas.value.width / 2, savedProductsChartCanvas.value.height / 2);
        return;
      }
      
      const ctx = savedProductsChartCanvas.value.getContext('2d');
      savedProductsChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: productNames,
          datasets: [
            {
              label: '기본 금리 (%)',
              data: baseRates,
              backgroundColor: 'rgba(59, 130, 246, 0.7)', // primary.light (blue-500) with opacity
              borderColor: 'rgba(29, 78, 216, 1)', // primary.dark (blue-700)
              borderWidth: 1,
              borderRadius: 4,
            },
            {
              label: '최고 금리 (%)',
              data: maxRates,
              backgroundColor: 'rgba(96, 165, 250, 0.7)', // lighter blue (blue-400) with opacity
              borderColor: 'rgba(59, 130, 246, 1)',    // primary.light (blue-500)
              borderWidth: 1,
              borderRadius: 4,
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: { 
              beginAtZero: true, 
              title: { display: true, text: '금리 (%)', font: {size: 14}, color: chartTextColor }, 
              grid: { color: chartGridColor },
              ticks: { color: chartTextColor }
            },
            x: { 
              grid: { display: false },
              ticks: { color: chartTextColor }
            }
          },
          plugins: {
            legend: { position: 'bottom', labels:{ font: {size: 12}, color: chartTextColor } },
            title: { display: true, text: '저장 상품 금리 비교', font: {size: 16, weight: 'bold'}, color: chartTextColor, padding: {top:10, bottom:20} },
            tooltip: { 
              backgroundColor: '#1f2937', // gray-800
              titleColor: '#e5e7eb', // gray-200
              bodyColor: '#d1d5db', // gray-300
              titleFont: {size: 14}, 
              bodyFont: {size: 12}, 
              padding: 10, 
              cornerRadius: 4, 
              displayColors: true 
            }
          },
          animation: { duration: 800, easing: 'easeInOutQuart' }
        }
      });
      chartLoading.value = false;
    } catch (error) {
      console.error("저장 상품 차트 초기화 오류:", error);
      chartLoading.value = false;
      const ctx = savedProductsChartCanvas.value.getContext('2d');
      ctx.clearRect(0, 0, savedProductsChartCanvas.value.width, savedProductsChartCanvas.value.height);
      ctx.textAlign = 'center';
      ctx.fillStyle = chartTextColor; // Use light text color for dark theme
      ctx.font = "16px 'Noto Sans KR', sans-serif";
      ctx.fillText('차트 로딩 중 오류 발생.', savedProductsChartCanvas.value.width / 2, savedProductsChartCanvas.value.height / 2);
    }
  }, 500);
};


watch(activeSection, (newSection) => {
  if (newSection === 'savedProductsSection') {
    renderSavedProductsChart();
  }
});

// Watch for changes in the authenticated user data from the store
watch(authUser, (newUser) => {
  if (newUser) {
    userData.userId = newUser.username || newUser.userId || ''; // Django User model has username, not userId typically for PK unless custom
    userData.email = newUser.email || '';
    userData.nickname = newUser.nickname || '';
    userData.age = newUser.age || null;
    userData.assets = newUser.assets || null; // These fields might be named differently or not exist on your User model
    userData.salary = newUser.salary || null; // Adjust according to your UserSerializer in Django
    userData.savingsTendency = newUser.savings_tendency || newUser.savingsTendency || ''; // Check field name from serializer
    
    // Populate authored posts and comments
    myBoardPosts.value = newUser.authored_posts || [];
    myComments.value = newUser.authored_comments || [];
    
    populateEditForm(); // Update edit form as well
  } else {
    // Clear local data if user logs out or data becomes unavailable
    Object.keys(userData).forEach(key => {
      const type = typeof userData[key];
      if (type === 'string') userData[key] = '';
      else if (type === 'number') userData[key] = null;
      else userData[key] = null; // default for others
    });
    populateEditForm();
  }
}, { immediate: true }); // immediate: true to run the watcher once on component mount with current authUser value

onMounted(async () => {
  if (isLoggedIn.value && !authUser.value) {
    // If logged in but user data isn't in store, try to load it
    await authStore.loadUser();
  } else if (authUser.value) {
    // If user data is already in store, populate local state
    // This might be redundant due to the immediate watcher, but can be a fallback
    const user = authUser.value;
    userData.userId = user.username || user.userId || '';
    userData.email = user.email || '';
    userData.nickname = user.nickname || '';
    userData.age = user.age || null;
    userData.assets = user.assets || null;
    userData.salary = user.salary || null;
    userData.savingsTendency = user.savings_tendency || user.savingsTendency || '';
  }
  populateEditForm(); // Initialize edit form
  
  if (activeSection.value === 'savedProductsSection') {
     renderSavedProductsChart(); // Initial chart render if this section is active
  }
  // TODO: Fetch savedProducts, myBoardPosts, myComments data here
  console.log("MyPage mounted. User:", authUser.value);
});

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

body { /* This is a general body style, MyPage itself is within a main tag */
    font-family: 'Noto Sans KR', sans-serif;
    /* background-color for the entire app is likely in App.vue or index.css */
}

.hidden { display: none !important; }

/* Sidebar Button Styling - Dark Theme */
.sidebar-button {
  @apply w-full flex items-center py-3 px-4 rounded-md text-sm font-medium transition-all duration-150 ease-in-out;
}
.sidebar-button-active-primary { /* Changed from -sky to -primary */
  @apply bg-primary text-white shadow-md; /* Uses primary color from Tailwind config */
}
.sidebar-button-inactive-dark { /* New class for dark theme inactive state */
  @apply text-gray-300 hover:bg-gray-700 hover:text-primary-light;
}
.sidebar-button svg {
  transition: transform 0.2s ease-in-out;
}
.sidebar-button:hover svg {
  transform: scale(1.1);
}

/* Content Section Styling - Dark Theme */
.section-title-dark { /* New class for dark theme section titles */
  @apply text-2xl font-bold text-primary-light mb-6 pb-3 border-b-2;
  /* border color (e.g., border-primary-dark) is applied via Tailwind class in template */
}

.info-label-dark { /* New class */
  @apply block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1;
}
.info-value-dark { /* New class */
  @apply text-gray-100 text-base;
}

/* Form Styling - Dark Theme */
.form-label-dark { /* New class */
  @apply block text-sm font-medium text-gray-300 mb-1;
}
.form-input-dark, .form-select-dark { /* New classes */
  @apply w-full px-3 py-2 border border-gray-600 rounded-md shadow-sm 
         bg-gray-700 text-gray-100 placeholder-gray-400
         focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary 
         transition duration-150 ease-in-out text-sm;
}
.form-input-dark.bg-gray-700.cursor-not-allowed { /* Specific for readonly */
  @apply bg-gray-600 cursor-not-allowed text-gray-400;
}
.form-select-dark {
  @apply appearance-none; 
}

/* Button Styling - Dark Theme (btn-primary uses Tailwind's definition) */
.btn { /* General button class remains */
  @apply px-5 py-2.5 rounded-md text-sm font-medium shadow-sm
         focus:outline-none focus:ring-2 focus:ring-offset-2 
         transition-all duration-150 ease-in-out;
}
/* .btn-primary is defined by Tailwind config: bg-primary hover:bg-primary-dark text-white focus:ring-primary */

.btn-secondary-dark { /* New class for dark theme secondary button */
  @apply bg-gray-600 text-gray-200 hover:bg-gray-500 focus:ring-gray-500 border border-gray-500;
}

/* List Item Card Styling - Dark Theme */
.list-item-card-dark { /* New class */
  @apply bg-gray-900 p-4 rounded-lg border border-gray-700 shadow-md hover:shadow-lg transition-shadow duration-200;
}

.sub-section-title-alt-dark { /* New class */
  @apply text-lg font-semibold text-gray-200 mb-3 pb-2 border-b border-gray-700;
}

/* Custom Scrollbar - Dark Theme */
.custom-scrollbar-dark::-webkit-scrollbar { /* New class */
  width: 8px;
}
.custom-scrollbar-dark::-webkit-scrollbar-track {
  background: #2d3748; /* gray-800 */
  border-radius: 10px;
}
.custom-scrollbar-dark::-webkit-scrollbar-thumb {
  background: #4a5568; /* gray-600 */
  border-radius: 10px;
}
.custom-scrollbar-dark::-webkit-scrollbar-thumb:hover {
  background: #718096; /* gray-500 */
}

/* Animation */
.animate-fadeIn { /* Remains the same */
  animation: fadeIn 0.5s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Responsive adjustments if needed */
@media (max-width: 768px) {
  .section-title-dark {
    font-size: 1.25rem; /* text-xl */
  }
  .info-value-dark {
    font-size: 0.95rem;
  }
}
</style>
<environment_details>
# VSCode Visible Files
design/BoardForm.vue

# VSCode Open Tabs
FinScope_Django/.env
FinScope_vue/src/main.js
FinScope_vue/src/views/CommoditiesPrice.vue
FinScope_vue/src/components/commoditiesChart.vue
FinScope_vue/src/components/exchangeRateChart.vue
FinScope_vue/src/views/BankMap.vue
FinScope_vue/src/views/Board.vue
FinScope_vue/src/components/PostDetail.vue
FinScope_vue/src/views/BoardDetail.vue
FinScope_vue/src/views/BoardForm.vue
FinScope_vue/src/views/BoardList.vue
FinScope_vue/src/views/Login.vue
FinScope_vue/src/views/Board.css
design/Board.css
design/BoardForm.vue
FinScope_vue/src/views/Signup.vue
FinScope_vue/tailwind.config.js
FinScope_vue/src/components/footer.vue
FinScope_vue/src/views/MyPage.vue
FinScope_vue/src/views/MyPageLayout.vue
FinScope_vue/src/views/NaverLoginCallback.vue
FinScope_vue/src/views/NewsDetail.vue
FinScope_vue/src/views/RecommendDeposit.vue
FinScope_vue/src/views/StockInfo.vue
FinScope_vue/src/api/depositSavingsApi.js
FinScope_vue/src/components/NavigationBar.vue
FinScope_vue/src/views/MainPage.vue
FinScope_vue/src/views/DepositPage.vue
FinScope_Django/stocks/views.py
FinScope_vue/src/App.vue
FinScope_vue/src/router/index.js
FinScope_vue/.env

# Current Time
5/28/2025, 5:06:29 AM (Asia/Seoul, UTC+9:00)

# Context Window Usage
408,370 / 1,048.576K tokens used (39%)

# Current Mode
ACT MODE
</environment_details>
