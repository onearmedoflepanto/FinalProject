<template>
  <div class="content-section">
    <h2 class="text-2xl font-semibold mb-6 text-gray-800 border-b-2 border-emerald-500 pb-3">기본 정보 수정</h2>
    <form @submit.prevent="handleProfileEditSubmit">
      <div class="space-y-5">
        <div><label for="editUserId" class="block text-sm font-medium text-gray-700 mb-1">아이디</label><input type="text" id="editUserId" :value="editData.userId" class="form-input bg-gray-100 cursor-not-allowed" readonly></div>
        <div><label for="editUserEmail" class="block text-sm font-medium text-gray-700 mb-1">이메일</label><input type="email" id="editUserEmail" v-model="editData.email" class="form-input" required></div>
        <div><label for="editUserNickname" class="block text-sm font-medium text-gray-700 mb-1">닉네임</label><input type="text" id="editUserNickname" v-model="editData.nickname" class="form-input" required></div>
        <div><label for="editUserAge" class="block text-sm font-medium text-gray-700 mb-1">나이</label><input type="number" id="editUserAge" v-model.number="editData.age" class="form-input" placeholder="숫자만 입력"></div>
        <div><label for="editUserAssets" class="block text-sm font-medium text-gray-700 mb-1">현재 가진 금액 (원)</label><input type="number" id="editUserAssets" v-model.number="editData.assets" class="form-input" placeholder="숫자만 입력"></div>
        <div><label for="editUserSalary" class="block text-sm font-medium text-gray-700 mb-1">연봉 (원)</label><input type="number" id="editUserSalary" v-model.number="editData.salary" class="form-input" placeholder="숫자만 입력"></div>
        <div><label for="editUserSavingsTendency" class="block text-sm font-medium text-gray-700 mb-1">저축 성향</label>
          <select id="editUserSavingsTendency" v-model="editData.savingsTendency" class="form-select">
            <option value="" disabled>선택하세요</option>
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
        <button type="submit" class="px-6 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700">저장</button>
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
    border-color: #059669; /* emerald-600 */
    box-shadow: 0 0 0 0.2rem rgba(5, 150, 105, 0.25); /* emerald-600 with 25% opacity */
}
.form-input.bg-gray-100 {
  background-color: #f3f4f6; /* Tailwind gray-100 */
}
</style>
