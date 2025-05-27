<template>
  <main class="flex-grow container mx-auto px-4 sm:px-6 py-8 md:py-12 text-gray-100">
    <div id="productListSection" class="page-section bg-gray-800 p-6 md:p-8 rounded-xl shadow-xl border border-gray-700">
      <h1 class="text-2xl md:text-3xl font-bold text-primary-light mb-6 text-center">예금 및 적금 금리 비교</h1>

      <div class="mb-6 space-y-4">
        <div class="flex flex-col sm:flex-row justify-between items-center gap-4">
          <div class="flex space-x-2">
            <button id="depositTabBtn" 
                    :class="['tab-button', currentProductType === 'deposit' ? 'active' : 'inactive']"
                    @click="selectProductType('deposit')">
              정기예금
            </button>
            <button id="savingsTabBtn" 
                    :class="['tab-button', currentProductType === 'savings' ? 'active' : 'inactive']"
                    @click="selectProductType('savings')">
              정기적금
            </button>
          </div>
          <div class="w-full sm:w-auto">
            <label for="bankFilter" class="sr-only">은행 선택</label>
            <select id="bankFilter" class="form-select w-full sm:w-64" v-model="selectedBank"
              @change="filterAndSortProducts">
              <option value="all">전체 은행</option>
              <option v-for="bankName in sortedBanks" :key="bankName" :value="bankName">{{ bankName }}</option>
            </select>
          </div>
        </div>
        <div class="flex flex-wrap justify-center sm:justify-start items-center gap-2 pt-2">
          <span class="text-sm font-medium text-gray-300 mr-2">정렬:</span>
          <button id="sortHighToLowBtn" 
                  :class="['sort-button', currentSortOrder === 'highToLow' ? 'active' : 'inactive']"
                  @click="sortProducts('highToLow')">
            높은 금리순
          </button>
          <button id="sortLowToHighBtn" 
                  :class="['sort-button', currentSortOrder === 'lowToHigh' ? 'active' : 'inactive']"
                  @click="sortProducts('lowToHigh')">
            낮은 금리순
          </button>
          <button id="resetSortBtn" 
                  :class="['sort-button', currentSortOrder === 'default' ? 'active' : 'inactive']"
                  @click="sortProducts('default')">
            정렬 초기화
          </button>
        </div>
      </div>

      <div class="table-container overflow-x-auto rounded-lg shadow">
        <table class="w-full product-table min-w-[640px]">
          <thead class="bg-gray-700">
            <tr>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">금융회사명</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">상품명</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">6개월</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">12개월</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">24개월</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">36개월</th>
            </tr>
          </thead>
          <tbody class="bg-gray-800 divide-y divide-gray-700">
            <template v-for="product in filteredAndSortedProducts" :key="product.id">
              <tr :class="expandedProductId === product.id ? 'bg-gray-700/70' : ''" class="hover:bg-gray-700/50 transition-colors duration-150">
                <td class="px-4 py-3 text-sm text-gray-300 border-b border-gray-700">{{ product.bank }}</td>
                <td class="px-4 py-3 text-sm border-b border-gray-700">
                  <a href="#" class="product-name-link" @click.prevent="toggleProductDetail(product.id)">
                    {{ product.name }}
                  </a>
                </td>
                <td class="px-4 py-3 text-sm text-gray-300 border-b border-gray-700">{{ formatRate(product.rates['6']) }}</td>
                <td class="px-4 py-3 text-sm text-gray-300 border-b border-gray-700">{{ formatRate(product.rates['12']) }}</td>
                <td class="px-4 py-3 text-sm text-gray-300 border-b border-gray-700">{{ formatRate(product.rates['24']) }}</td>
                <td class="px-4 py-3 text-sm text-gray-300 border-b border-gray-700">{{ formatRate(product.rates['36']) }}</td>
              </tr>
              <tr v-if="expandedProductId === product.id" class="product-detail-row bg-gray-700/30">
                <td colspan="6" class="p-0 border-b border-gray-600">
                  <div class="p-4 bg-gray-900 rounded-b-lg">
                    <div class="flex justify-between items-center mb-4">
                      <h2 class="text-xl font-bold text-primary-light">{{ product.name }} 상세 정보</h2>
                      <button class="bg-gray-600 text-white py-1.5 px-3 rounded-lg hover:bg-gray-500 text-sm"
                        @click="toggleProductDetail(null)">
                        닫기
                      </button>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4 detail-section">
                      <div>
                        <dt class="text-gray-400">공시 제출월</dt>
                        <dd class="text-gray-200">{{ product.submitMonth }}</dd>
                      </div>
                      <div>
                        <dt class="text-gray-400">금융회사명</dt>
                        <dd class="text-gray-200">{{ product.bank }}</dd>
                      </div>
                      <div>
                        <dt class="text-gray-400">가입제한</dt>
                        <dd class="text-gray-200">{{ product.restriction }}</dd>
                      </div>
                      <div>
                        <dt class="text-gray-400">가입방법</dt>
                        <dd class="text-gray-200">{{ product.way }}</dd>
                      </div>
                      <div class="md:col-span-2">
                        <dt class="text-gray-400">우대조건</dt>
                        <dd class="whitespace-pre-line text-gray-200">{{ product.special || '특별 우대 조건 없음' }}</dd>
                      </div>
                    </div>
                    <h3 class="text-lg font-semibold text-gray-100 mb-2">금리 정보 (세전)</h3>
                    <div class="space-y-1 detail-section">
                      <p v-if="!hasInterestRatesForProduct(product)" class="text-gray-400">금리 정보 없음</p>
                      <p v-else v-for="(rate, term) in product.rates" :key="term" class="text-gray-200">
                        <span class="font-medium">{{ term }}개월:</span> {{ formatRate(rate) }}
                      </p>
                    </div>
                    <div
                      class="mt-6 flex flex-col sm:flex-row justify-center items-center space-y-2 sm:space-y-0 sm:space-x-3">
                      <button v-if="isLoggedIn" @click="handleSaveProduct(product)" :disabled="isProductSaved(product)"
                        :class="[
                          'py-2.5 px-6 rounded-lg font-medium transition-colors',
                          isProductSaved(product) ? 'bg-green-600 text-white cursor-not-allowed' : 'bg-primary hover:bg-primary-dark text-white'
                        ]">
                        {{ isProductSaved(product) ? '저장됨' : 'MyPage에 저장' }}
                      </button>
                      <button v-if="isLoggedIn && isProductSaved(product)"
                              @click="handleToggleNotification(product)"
                              :class="[
                                'py-2.5 px-6 rounded-lg font-medium transition-colors ml-2',
                                isSubscribedToNotifications(product) ? 'bg-red-600 hover:bg-red-700 text-white' : 'bg-yellow-500 hover:bg-yellow-600 text-white'
                              ]">
                        {{ isSubscribedToNotifications(product) ? '알림 해제' : '금리변동 알림받기' }}
                      </button>
                      <p v-if="!isLoggedIn" class="text-sm text-red-400">상품을 저장하고 알림을 받으려면 로그인이 필요합니다.</p>
                    </div>
                  </div>
                </td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
      <p v-if="filteredAndSortedProducts.length === 0" class="text-center text-gray-500 py-8">
        선택하신 조건에 맞는 상품이 없습니다.
      </p>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue';
import { fetchDepositProducts, fetchSavingsProducts, saveFinancialProduct, toggleNotificationSubscription } from '@/api/depositSavingsApi';
import { useAuthStore } from '@/stores/user';
import { storeToRefs } from 'pinia';

const authStore = useAuthStore();
const { user: authUser, isLoggedIn } = storeToRefs(authStore);

const currentProductType = ref('deposit');
const currentSortOrder = ref('default');
const allProducts = ref([]);
const selectedBank = ref('all');
const expandedProductId = ref(null);

const sortedBanks = computed(() => {
  const banks = new Set(allProducts.value.map(p => p.kor_co_nm));
  return Array.from(banks).sort();
});

const filteredAndSortedProducts = computed(() => {
  let productsToDisplay = allProducts.value.filter(product =>
    selectedBank.value === 'all' || product.kor_co_nm === selectedBank.value
  );

  if (currentSortOrder.value !== 'default') {
    productsToDisplay.sort((a, b) => {
      const rateA = a.rates['12'] !== null && a.rates['12'] !== undefined ? parseFloat(a.rates['12']) : (currentSortOrder.value === 'highToLow' ? -Infinity : Infinity);
      const rateB = b.rates['12'] !== null && b.rates['12'] !== undefined ? parseFloat(b.rates['12']) : (currentSortOrder.value === 'highToLow' ? -Infinity : Infinity);

      if (currentSortOrder.value === 'highToLow') {
        return rateB - rateA;
      } else {
        return rateA - rateB;
      }
    });
  }
  return productsToDisplay;
});

const isProductSaved = computed(() => {
  return (productToCheck) => {
    if (!authUser.value || !authUser.value.saved_financial_products) {
      return false;
    }
    return authUser.value.saved_financial_products.some(savedProd =>
      savedProd.fin_co_no === productToCheck.fin_co_no &&
      savedProd.fin_prdt_cd === productToCheck.fin_prdt_cd &&
      savedProd.product_type === productToCheck.product_type
    );
  };
});

const isSubscribedToNotifications = computed(() => {
  return (productToCheck) => {
    if (!isLoggedIn.value || !authUser.value || !authUser.value.saved_financial_products) {
      return false;
    }
    const savedProductInstance = authUser.value.saved_financial_products.find(savedProd =>
      savedProd.fin_co_no === productToCheck.fin_co_no &&
      savedProd.fin_prdt_cd === productToCheck.fin_prdt_cd &&
      savedProd.product_type === productToCheck.product_type
    );
    return savedProductInstance ? savedProductInstance.notify_on_rate_change : false;
  };
});

const hasInterestRatesForProduct = (product) => {
  if (!product || !product.rates) return false;
  return Object.values(product.rates).some(rate => rate !== null && rate !== undefined);
};

const fetchData = async () => {
  try {
    let data;
    if (currentProductType.value === 'deposit') {
      data = await fetchDepositProducts();
    } else {
      data = await fetchSavingsProducts();
    }
    const processedProducts = data.map(product => {
      const rates = {};
      if (product.options && Array.isArray(product.options)) {
        product.options.forEach(opt => {
          if (opt.save_trm) {
            rates[opt.save_trm] = opt.intr_rate;
          }
        });
      }
      return {
        ...product,
        id: product.id, 
        bank: product.kor_co_nm,
        name: product.fin_prdt_nm,
        rates: rates,
        submitMonth: product.dcls_month,
      };
    });

    allProducts.value = processedProducts;
    selectedBank.value = 'all';
    currentSortOrder.value = 'default';
  } catch (error) {
    console.error('Failed to fetch products:', error);
    allProducts.value = [];
  }
};

const selectProductType = (type) => {
  currentProductType.value = type;
  fetchData();
};

const sortProducts = (order) => {
  currentSortOrder.value = order;
};

const filterAndSortProducts = () => {
  // This computed property already handles filtering and sorting.
};

const toggleProductDetail = (productId) => {
  expandedProductId.value = expandedProductId.value === productId ? null : productId;
};

const formatRate = (rate) => {
  return rate !== null && rate !== undefined ? parseFloat(rate).toFixed(2) + '%' : '-';
};

const handleSaveProduct = async (product) => {
  if (!isLoggedIn.value) {
    alert('상품을 저장하려면 로그인이 필요합니다.');
    return;
  }
  if (isProductSaved.value(product)) {
    alert('이미 저장된 상품입니다.');
    return;
  }

  const productData = {
    product_type: product.product_type,
    fin_co_no: product.fin_co_no,
    fin_prdt_cd: product.fin_prdt_cd,
    product_name: product.name,
    bank_name: product.bank,
    interest_rate_12m: product.rates && product.rates['12'] ? parseFloat(product.rates['12']) : null,
  };

  try {
    await saveFinancialProduct(productData);
    alert('상품이 My Page에 저장되었습니다.');
    await authStore.loadUser();
  } catch (error) {
    alert('상품 저장에 실패했습니다. 이미 저장된 상품일 수 있습니다.');
    console.error("Failed to save product:", error);
  }
};

const handleToggleNotification = async (product) => {
  if (!isLoggedIn.value) {
    alert('알림 설정을 변경하려면 로그인이 필요합니다.');
    return;
  }
  const savedProductInstance = authUser.value.saved_financial_products.find(savedProd =>
    savedProd.fin_co_no === product.fin_co_no &&
    savedProd.fin_prdt_cd === product.fin_prdt_cd &&
    savedProd.product_type === product.product_type
  );

  if (!savedProductInstance) {
    alert('알림을 설정하려면 먼저 상품을 MyPage에 저장해야 합니다.');
    return;
  }

  const currentStatus = savedProductInstance.notify_on_rate_change;
  const newStatus = !currentStatus;

  try {
    const updatedSubscription = await toggleNotificationSubscription(savedProductInstance.id, newStatus);
    const productIndex = authUser.value.saved_financial_products.findIndex(p => p.id === savedProductInstance.id);
    if (productIndex !== -1) {
      authUser.value.saved_financial_products[productIndex].notify_on_rate_change = updatedSubscription.notify_on_rate_change;
    }
    alert(`금리 변동 알림이 ${newStatus ? '설정' : '해제'}되었습니다.`);
  } catch (error) {
    alert('알림 설정 변경에 실패했습니다.');
    console.error("Failed to toggle notification:", error);
  }
};

onMounted(() => {
  if (isLoggedIn.value && !authUser.value) {
    authStore.loadUser();
  }
  fetchData();
});
</script>

<style scoped>
.tab-button,
.sort-button {
  padding: 0.5rem 1rem; 
  border-radius: 0.375rem; /* rounded-md */
  font-weight: 500; /* font-medium */
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s, border-color 0.2s;
  border-width: 1px;
  border-style: solid;
  font-size: 0.875rem; /* text-sm */
}

.tab-button.active,
.sort-button.active {
  @apply bg-primary text-white border-primary;
}

.tab-button.inactive,
.sort-button.inactive {
  @apply bg-gray-600 text-gray-300 border-gray-500 hover:bg-gray-500 hover:text-white;
}

.form-select {
  @apply bg-gray-700 border-gray-600 text-gray-100 focus:ring-primary-light focus:border-primary-light;
  /* Basic select styling from Tailwind is in the template, this ensures dark mode compatibility */
  appearance: none; /* Remove default system appearance */
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20' fill='%239CA3AF'%3E%3Cpath fill-rule='evenodd' d='M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z' clip-rule='evenodd'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.5rem center;
  background-size: 1.5em 1.5em;
}
.form-select option { 
    background-color: #374151; /* bg-gray-700 */
    color: #F3F4F6; /* text-gray-100 */
}

.table-container {
  overflow-x: auto;
}

.product-table th,
.product-table td {
  padding: 0.75rem 1rem;
  text-align: left;
  font-size: 0.875rem; 
}

.product-table thead th {
  font-weight: 600; /* font-semibold */
}

.product-name-link {
  @apply text-primary-light hover:text-primary font-medium; /* Ensure visibility */
  cursor: pointer;
}

.product-name-link:hover {
  text-decoration: underline;
}

.detail-section dt {
  font-weight: 500; /* font-medium */
}
</style>
