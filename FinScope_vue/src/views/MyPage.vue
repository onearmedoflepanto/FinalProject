<template>
  <main class="flex-grow container mx-auto px-4 sm:px-6 py-8 md:py-12">
    <h1 class="text-3xl md:text-4xl font-bold mb-8 md:mb-10 text-center text-teal-700">
      <span class="text-sky-600">{{ userProfileName }}</span>님의 프로필
    </h1>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 md:gap-8">
      <div class="lg:col-span-1 bg-white p-6 rounded-xl shadow-xl border border-gray-200 flex flex-col justify-start">
        <h2 class="text-2xl font-semibold mb-6 text-gray-800 border-b-2 border-teal-500 pb-3">계정 관리</h2>
        <div class="space-y-3">
          <button @click="showSection('userInfoDisplaySection')" :class="['w-full py-3 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-opacity-50 transition duration-150 ease-in-out text-base font-medium action-button-secondary', { hidden: activeSection !== 'userInfoEditSection' }]">
            기본 정보 보기
          </button>
          <button @click="showSection('userInfoEditSection')" :class="['w-full bg-teal-600 text-white py-3 px-4 rounded-lg hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-opacity-50 transition duration-150 ease-in-out text-base font-medium border border-transparent', { hidden: activeSection === 'userInfoEditSection' }]">
            기본 정보 수정
          </button>
          <button @click="showSection('savedProductsSection')" class="w-full bg-sky-500 text-white py-3 px-4 rounded-lg hover:bg-sky-600 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:ring-opacity-50 transition duration-150 ease-in-out text-base font-medium border border-transparent">
            저장한 상품
          </button>
          <button @click="showSection('myPostsSection')" class="w-full bg-indigo-500 text-white py-3 px-4 rounded-lg hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50 transition duration-150 ease-in-out text-base font-medium border border-transparent">
            내가 작성한 글
          </button>
        </div>
      </div>

      <div class="lg:col-span-2 bg-white p-6 rounded-xl shadow-xl border border-gray-200">
        <div v-if="activeSection === 'userInfoDisplaySection'" class="content-section">
          <h2 class="text-2xl font-semibold mb-6 text-gray-800 border-b-2 border-teal-500 pb-3">기본 정보</h2>
          <div class="space-y-5">
            <div><label class="block text-xs font-medium text-gray-500 uppercase tracking-wider">아이디</label><p class="text-gray-900 text-lg">{{ userData.userId }}</p></div>
            <div><label class="block text-xs font-medium text-gray-500 uppercase tracking-wider">이메일</label><p class="text-gray-900 text-lg">{{ userData.email }}</p></div>
            <div><label class="block text-xs font-medium text-gray-500 uppercase tracking-wider">닉네임</label><p class="text-gray-900 text-lg">{{ userData.nickname }}</p></div>
            <div><label class="block text-xs font-medium text-gray-500 uppercase tracking-wider">나이</label><p class="text-gray-900 text-lg">{{ userData.age || '정보 없음' }}</p></div>
            <div><label class="block text-xs font-medium text-gray-500 uppercase tracking-wider">현재 가진 금액 (원)</label><p class="text-gray-900 text-lg">{{ formatCurrency(userData.assets) }}</p></div>
            <div><label class="block text-xs font-medium text-gray-500 uppercase tracking-wider">연봉 (원)</label><p class="text-gray-900 text-lg">{{ formatCurrency(userData.salary) }}</p></div>
            <div><label class="block text-xs font-medium text-gray-500 uppercase tracking-wider">저축 성향</label><p class="text-gray-900 text-lg">{{ userData.savingsTendency }}</p></div>
          </div>
        </div>

        <div v-if="activeSection === 'userInfoEditSection'" class="content-section">
          <h2 class="text-2xl font-semibold mb-6 text-gray-800 border-b-2 border-teal-500 pb-3">기본 정보 수정</h2>
          <form @submit.prevent="handleProfileEditSubmit">
            <div class="space-y-5">
              <div><label for="editUserId" class="block text-sm font-medium text-gray-700 mb-1">아이디</label><input type="text" id="editUserId" :value="editData.userId" class="form-input bg-gray-100 cursor-not-allowed" readonly></div>
              <div><label for="editUserEmail" class="block text-sm font-medium text-gray-700 mb-1">이메일</label><input type="email" id="editUserEmail" v-model="editData.email" class="form-input" required></div>
              <div><label for="editUserNickname" class="block text-sm font-medium text-gray-700 mb-1">닉네임</label><input type="text" id="editUserNickname" v-model="editData.nickname" class="form-input" required></div>
              <div><label for="editUserAge" class="block text-sm font-medium text-gray-700 mb-1">나이</label><input type="number" id="editUserAge" v-model.number="editData.age" class="form-input" placeholder="숫자만 입력"></div>
              <div><label for="editUserAssets" class="block text-sm font-medium text-gray-700 mb-1">현재 가진 금액 (원)</label><input type="number" id="editUserAssets" v-model.number="editData.assets" class="form-input" placeholder="숫자만 입력" required></div>
              <div><label for="editUserSalary" class="block text-sm font-medium text-gray-700 mb-1">연봉 (원)</label><input type="number" id="editUserSalary" v-model.number="editData.salary" class="form-input" placeholder="숫자만 입력"></div>
              <div><label for="editUserSavingsTendency" class="block text-sm font-medium text-gray-700 mb-1">저축 성향</label>
                <select id="editUserSavingsTendency" v-model="editData.savingsTendency" class="form-select">
                  <option value="알뜰형">알뜰형</option>
                  <option value="균형형">균형형</option>
                  <option value="도전형">도전형</option>
                </select>
              </div>
            </div>
            <hr class="my-8 border-gray-300">
            <h3 class="text-xl font-semibold mb-4 text-gray-700">비밀번호 변경</h3>
            <div class="space-y-5">
              <div><label for="editCurrentPassword" class="block text-sm font-medium text-gray-700 mb-1">현재 비밀번호</label><input type="password" id="editCurrentPassword" v-model="editData.currentPassword" class="form-input" placeholder="현재 비밀번호 입력"></div>
              <div><label for="editNewPassword" class="block text-sm font-medium text-gray-700 mb-1">새 비밀번호</label><input type="password" id="editNewPassword" v-model="editData.newPassword" class="form-input" placeholder="새 비밀번호 (8자 이상)"></div>
              <div><label for="editConfirmNewPassword" class="block text-sm font-medium text-gray-700 mb-1">새 비밀번호 확인</label><input type="password" id="editConfirmNewPassword" v-model="editData.confirmNewPassword" class="form-input" placeholder="새 비밀번호 다시 입력"></div>
            </div>
            <div class="mt-8 flex justify-end space-x-3">
              <button type="button" @click="cancelEdit" class="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-100">취소</button>
              <button type="submit" class="px-6 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700">저장</button>
            </div>
          </form>
        </div>

        <div v-if="activeSection === 'savedProductsSection'" class="content-section">
          <h2 class="text-2xl font-semibold mb-6 text-gray-800 border-b-2 border-sky-500 pb-3">저장한 금융 상품</h2>
          <div class="space-y-4 mb-8 max-h-[300px] overflow-y-auto pr-2">
            <!-- Placeholder for saved products list -->
            <div v-if="savedProducts.length === 0" class="text-gray-500 p-4 text-center">저장한 상품이 없습니다.</div>
            <div v-for="product in savedProducts" :key="product.id" class="list-item">
              <h3>{{ product.name }}</h3>
              <div class="details grid grid-cols-2 gap-x-4">
                <p>기본 금리: <span>{{ product.baseRate }}%</span></p>
                <p>최고 금리: <span>{{ product.maxRate }}%</span> (우대)</p>
                <p>가입 기간: <span>{{ product.term }}</span></p>
                <p>은행: <span>{{ product.bank }}</span></p>
              </div>
            </div>
          </div>
          <h3 class="text-xl font-semibold mb-4 text-gray-700 mt-8">저장 상품 금리 비교</h3>
          <div class="w-full h-72 md:h-80 bg-gray-50 rounded-lg flex items-center justify-center text-gray-500 p-4 relative border border-gray-200">
            <canvas ref="savedProductsChartCanvas"></canvas>
            <p v-if="chartLoading" class="absolute inset-0 flex items-center justify-center text-gray-500 z-10">차트 로딩 중...</p>
          </div>
        </div>

        <div v-if="activeSection === 'myPostsSection'" class="content-section">
          <h2 class="text-2xl font-semibold mb-6 text-gray-800 border-b-2 border-indigo-500 pb-3">내가 작성한 활동</h2>
          <div class="mb-8">
            <h3 class="sub-section-title">내가 작성한 게시글</h3>
            <div class="space-y-4 max-h-[250px] overflow-y-auto pr-2">
              <!-- Placeholder for user's board posts -->
              <div v-if="myBoardPosts.length === 0" class="text-gray-500 p-4 text-center">작성한 게시글이 없습니다.</div>
              <div v-for="post in myBoardPosts" :key="post.id" class="list-item">
                <h3>{{ post.title }}</h3>
                <p class="content-preview truncate">{{ post.contentPreview }}</p>
                <div class="details mt-1 flex justify-between items-center">
                  <p class="text-xs text-gray-500">게시판: <span>{{ post.boardName }}</span></p>
                  <p class="text-xs text-gray-500">작성일: <span>{{ post.date }}</span></p>
                  <router-link :to="`/board/${post.id}`" class="text-xs text-teal-600 hover:underline">자세히 보기 &rarr;</router-link>
                </div>
              </div>
            </div>
          </div>
          <div>
            <h3 class="sub-section-title">내가 작성한 댓글</h3>
            <div class="space-y-4 max-h-[250px] overflow-y-auto pr-2">
              <!-- Placeholder for user's comments -->
              <div v-if="myComments.length === 0" class="text-gray-500 p-4 text-center">작성한 댓글이 없습니다.</div>
              <div v-for="comment in myComments" :key="comment.id" class="list-item">
                <h4>댓글 단 게시글: <span>{{ comment.postTitle }}</span></h4>
                <p class="content-preview truncate">{{ comment.contentPreview }}</p>
                <div class="details mt-1 flex justify-between items-center">
                  <p class="text-xs text-gray-500">게시판: <span>{{ comment.boardName }}</span></p>
                  <p class="text-xs text-gray-500">작성일: <span>{{ comment.date }}</span></p>
                  <router-link :to="`/board/${comment.postId}`" class="text-xs text-teal-600 hover:underline">원문 보기 &rarr;</router-link>
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

      if (productNames.length === 0) {
        chartLoading.value = false;
        // Optionally display a message in the canvas area
        const ctx = savedProductsChartCanvas.value.getContext('2d');
        ctx.clearRect(0, 0, savedProductsChartCanvas.value.width, savedProductsChartCanvas.value.height);
        ctx.textAlign = 'center';
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
              backgroundColor: 'rgba(20, 184, 166, 0.7)', // teal-500
              borderColor: 'rgba(15, 118, 110, 1)', // teal-600
              borderWidth: 1,
              borderRadius: 4,
            },
            {
              label: '최고 금리 (%)',
              data: maxRates,
              backgroundColor: 'rgba(14, 165, 233, 0.7)', // sky-500
              borderColor: 'rgba(2, 132, 199, 1)', // sky-600
              borderWidth: 1,
              borderRadius: 4,
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: { beginAtZero: true, title: { display: true, text: '금리 (%)', font: {size: 14}}, grid: { color: '#e5e7eb' } },
            x: { grid: { display: false } }
          },
          plugins: {
            legend: { position: 'bottom', labels:{ font: {size: 12}} },
            title: { display: true, text: '저장 상품 금리 비교', font: {size: 16, weight: 'bold'}, padding: {top:10, bottom:20} },
            tooltip: { backgroundColor: '#1f2937', titleFont: {size: 14}, bodyFont: {size: 12}, padding: 10, cornerRadius: 4, displayColors: true }
          },
          animation: { duration: 800, easing: 'easeInOutQuart' }
        }
      });
      chartLoading.value = false;
    } catch (error) {
      console.error("저장 상품 차트 초기화 오류:", error);
      chartLoading.value = false;
      // Display error on canvas
       const ctx = savedProductsChartCanvas.value.getContext('2d');
        ctx.clearRect(0, 0, savedProductsChartCanvas.value.width, savedProductsChartCanvas.value.height);
        ctx.textAlign = 'center';
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
/* Styles from mypage.html, adapted for Vue component */
body { /* This will likely be handled by a global style or App.vue */
    font-family: 'Inter', sans-serif;
    background-color: #f8fafc;
}
main {
    flex-grow: 1;
}
.hidden { display: none !important; }

.form-input, .form-select {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #d1d5db; /* border-gray-300 */
    border-radius: 0.375rem; /* rounded-md */
    box-shadow: inset 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}
.form-input:focus, .form-select:focus {
    outline: none;
    border-color: #0d9488; /* teal-600 */
    box-shadow: 0 0 0 0.2rem rgba(13, 148, 136, 0.25); /* ring-teal-500 opacity-25 */
}
.action-button-secondary {
    border: 1px solid #0d9488; /* teal-600 border */
    color: #0d9488; /* teal-600 text */
    background-color: white;
}
.action-button-secondary:hover {
    background-color: #f0fdfa; /* teal-50 background */
}
.list-item {
    background-color: #f9fafb; /* gray-50 */
    padding: 1rem; /* p-4 */
    border: 1px solid #e5e7eb; /* border-gray-200 */
    border-radius: 0.5rem; /* rounded-lg */
    transition: box-shadow 0.2s ease-in-out;
}
.list-item:hover {
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06); /* shadow-md */
}
.list-item h3 {
    font-size: 1.125rem; /* text-lg */
    font-weight: 600; /* font-semibold */
    color: #14b8a6; /* text-teal-500 */
    margin-bottom: 0.25rem;
}
.list-item h4 {
    font-size: 0.95rem;
    font-weight: 500;
    color: #374151; /* text-gray-700 */
    margin-bottom: 0.25rem;
}
.list-item p.content-preview {
    font-size: 0.875rem; /* text-sm */
    color: #4b5563; /* text-gray-600 */
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
</style>
