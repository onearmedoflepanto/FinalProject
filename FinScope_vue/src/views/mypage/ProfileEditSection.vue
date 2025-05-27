<template>
  <div class="content-section p-6 sm:p-8">
    <h2 class="text-2xl font-bold text-primary-light mb-6 pb-3 border-b-2 border-primary-dark">기본 정보 수정</h2>
    <form @submit.prevent="handleProfileEditSubmit" class="space-y-6">
      <div class="grid grid-cols-1 gap-y-4"> 
        <div><label for="editUserId" class="form-label-dark-local">아이디</label><input type="text" id="editUserId" :value="editData.userId" class="form-input-dark-local bg-gray-600 cursor-not-allowed" readonly></div>
        <div><label for="editUserEmail" class="form-label-dark-local">이메일</label><input type="email" id="editUserEmail" v-model="editData.email" class="form-input-dark-local" required></div>
        <div><label for="editUserNickname" class="form-label-dark-local">닉네임</label><input type="text" id="editUserNickname" v-model="editData.nickname" class="form-input-dark-local" required></div>
        <div><label for="editUserAge" class="form-label-dark-local">나이</label><input type="number" id="editUserAge" v-model.number="editData.age" class="form-input-dark-local" placeholder="숫자만 입력"></div>
        <div><label for="editUserAssets" class="form-label-dark-local">현재 가진 금액 (원)</label><input type="number" id="editUserAssets" v-model.number="editData.assets" class="form-input-dark-local" placeholder="숫자만 입력"></div>
        <div><label for="editUserSalary" class="form-label-dark-local">연봉 (원)</label><input type="number" id="editUserSalary" v-model.number="editData.salary" class="form-input-dark-local" placeholder="숫자만 입력"></div>
        <div><label for="editUserSavingsTendency" class="form-label-dark-local">저축 성향</label>
          <select id="editUserSavingsTendency" v-model="editData.savingsTendency" class="form-select-dark-local">
            <option value="" disabled>선택하세요</option>
            <option value="알뜰형">알뜰형</option>
            <option value="균형형">균형형</option>
            <option value="도전형">도전형</option>
          </select>
        </div>
      </div>
            <hr class="my-6 border-gray-700">
            <h3 class="text-xl font-semibold mb-4 text-gray-300">비밀번호 변경</h3>
            <div class="grid grid-cols-1 gap-y-4"> 
              <div><label for="editCurrentPassword" class="form-label-dark-local">현재 비밀번호</label><input type="password" id="editCurrentPassword" v-model="editData.currentPassword" class="form-input-dark-local" placeholder="현재 비밀번호 입력"></div>
              <div><label for="editNewPassword" class="form-label-dark-local">새 비밀번호</label><input type="password" id="editNewPassword" v-model="editData.newPassword" class="form-input-dark-local" placeholder="새 비밀번호 (8자 이상)"></div>
        <div><label for="editConfirmNewPassword" class="form-label-dark-local">새 비밀번호 확인</label><input type="password" id="editConfirmNewPassword" v-model="editData.confirmNewPassword" class="form-input-dark-local" placeholder="새 비밀번호 다시 입력"></div>
      </div>
      <div class="mt-8 flex justify-end space-x-3">
        <button type="button" @click="cancelEdit" class="btn-secondary-dark-local">취소</button>
        <button type="submit" class="btn-primary-local">저장</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, watch, onMounted } from 'vue';
import { useAuthStore } from '@/stores/user';
import { storeToRefs } from 'pinia';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const { user: authUser, isLoggedIn } = storeToRefs(authStore);
const router = useRouter();

const editData = reactive({
  userId: '', // Will be read-only, from username
  email: '',
  nickname: '',
  age: null,
  assets: null,
  salary: null,
  savingsTendency: '',
  currentPassword: '',
  newPassword: '',
  confirmNewPassword: '',
});

const populateEditForm = (currentUser) => {
  if (currentUser) {
    editData.userId = currentUser.username || ''; // Assuming userId is username
    editData.email = currentUser.email || '';
    editData.nickname = currentUser.nickname || '';
    editData.age = currentUser.age || null;
    editData.assets = currentUser.assets || null;
    editData.salary = currentUser.salary || null;
    editData.savingsTendency = currentUser.savings_tendency || currentUser.savingsTendency || '';
  }
  editData.currentPassword = '';
  editData.newPassword = '';
  editData.confirmNewPassword = '';
};

watch(authUser, (newUser) => {
  populateEditForm(newUser);
}, { immediate: true, deep: true });

onMounted(async () => {
  if (isLoggedIn.value && !authUser.value) {
    await authStore.loadUser(); // Watcher will populate editData
  } else {
    populateEditForm(authUser.value); // Populate if already loaded
  }
});

const cancelEdit = () => {
  router.push({ name: 'my-page-profile' }); // Navigate to display section
};

const handleProfileEditSubmit = async () => {
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
  }

  const profileUpdateData = {
    email: editData.email,
    nickname: editData.nickname,
    age: editData.age,
    assets: editData.assets,
    salary: editData.salary,
    savings_tendency: editData.savingsTendency,
    current_password: editData.currentPassword,
    new_password: editData.newPassword,
  };

  if (!profileUpdateData.current_password && !profileUpdateData.new_password) {
    delete profileUpdateData.current_password;
    delete profileUpdateData.new_password;
  } else if (profileUpdateData.new_password && !profileUpdateData.current_password) {
    alert("새 비밀번호를 변경하려면 현재 비밀번호를 입력해야 합니다.");
    return;
  }
  
  // Filter out null or empty password fields if not changing password
  if (!editData.newPassword) {
    delete profileUpdateData.new_password;
    delete profileUpdateData.current_password; // No need to send current_password if new_password is not set
  }


  const result = await authStore.updateUserProfile(profileUpdateData);

  if (result.success) {
    alert("프로필 정보가 성공적으로 업데이트되었습니다.");
    router.push({ name: 'my-page-profile' }); // Navigate to display section
  } else {
    alert(result.message || "프로필 업데이트에 실패했습니다.");
  }
};
</script>

<style scoped>
.content-section {
  animation: fadeIn 0.5s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
/* Removed old light-theme form input styles */

/* Dark Theme Form Styling specific to this component if needed, or rely on MyPageLayout's if structure allows */
.form-label-dark-local {
  @apply block text-sm font-medium text-gray-300 mb-1;
}
.form-input-dark-local, .form-select-dark-local {
  @apply w-full px-3 py-2 border border-gray-600 rounded-md shadow-sm 
         bg-gray-700 text-gray-100 placeholder-gray-400
         focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary 
         transition duration-150 ease-in-out text-sm;
}
/* The readonly input style is handled by adding bg-gray-600 directly in the template, so this specific CSS rule is not needed and causes circular dependency. */
.form-select-dark-local {
  @apply appearance-none; 
}

/* Dark Theme Button Styling specific to this component */
.btn-primary-local {
  @apply px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 focus:ring-offset-gray-800 transition-colors;
}
.btn-secondary-dark-local {
  @apply px-6 py-2 border border-gray-500 rounded-lg text-gray-300 hover:bg-gray-700 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 focus:ring-offset-gray-800 transition-colors;
}
</style>
