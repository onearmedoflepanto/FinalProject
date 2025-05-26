<template>
  <main class="flex-grow container mx-auto px-4 sm:px-6 py-8 md:py-12">
    <div id="productListSection" class="page-section bg-white p-6 md:p-8 rounded-xl shadow-xl border border-gray-200">
      <h1 class="text-2xl md:text-3xl font-bold text-teal-700 mb-6 text-center">예금 및 적금 금리 비교</h1>

      <div class="mb-6 space-y-4">
        <div class="flex flex-col sm:flex-row justify-between items-center gap-4">
          <div class="flex space-x-2">
            <button id="depositTabBtn" class="tab-button" :class="{ active: currentProductType === 'deposit' }"
              @click="selectProductType('deposit')">
              정기예금
            </button>
            <button id="savingsTabBtn" class="tab-button" :class="{ active: currentProductType === 'savings' }"
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
          <span class="text-sm font-medium text-gray-700 mr-2">정렬:</span>
          <button id="sortHighToLowBtn" class="sort-button" :class="{ active: currentSortOrder === 'highToLow' }"
            @click="sortProducts('highToLow')">
            높은 금리순
          </button>
          <button id="sortLowToHighBtn" class="sort-button" :class="{ active: currentSortOrder === 'lowToHigh' }"
            @click="sortProducts('lowToHigh')">
            낮은 금리순
          </button>
          <button id="resetSortBtn" class="sort-button" :class="{ active: currentSortOrder === 'default' }"
            @click="sortProducts('default')">
            정렬 초기화
          </button>
        </div>
      </div>

      <div class="table-container">
        <table class="w-full product-table">
          <thead>
            <tr>
              <th>금융회사명</th>
              <th>상품명</th>
              <th>6개월</th>
              <th>12개월</th>
              <th>24개월</th>
              <th>36개월</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="product in filteredAndSortedProducts" :key="product.id">
              <tr :class="{ 'bg-teal-50': expandedProductId === product.id }">
                <td>{{ product.bank }}</td>
                <td>
                  <a href="#" class="product-name-link" @click.prevent="toggleProductDetail(product.id)">
                    {{ product.name }}
                  </a>
                </td>
                <td>{{ formatRate(product.rates['6']) }}</td>
                <td>{{ formatRate(product.rates['12']) }}</td>
                <td>{{ formatRate(product.rates['24']) }}</td>
                <td>{{ formatRate(product.rates['36']) }}</td>
              </tr>
              <tr v-if="expandedProductId === product.id" class="product-detail-row">
                <td colspan="6">
                  <div class="p-4 bg-gray-50 rounded-lg border border-gray-200">
                    <div class="flex justify-between items-center mb-4">
                      <h2 class="text-xl font-bold text-teal-700">{{ product.name }} 상세 정보</h2>
                      <button class="bg-gray-500 text-white py-1.5 px-3 rounded-lg hover:bg-gray-600 text-sm"
                        @click="toggleProductDetail(null)">
                        닫기
                      </button>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4 detail-section">
                      <div>
                        <dt>공시 제출월</dt>
                        <dd>{{ product.submitMonth }}</dd>
                      </div>
                      <div>
                        <dt>금융회사명</dt>
                        <dd>{{ product.bank }}</dd>
                      </div>
                      <div>
                        <dt>가입제한</dt>
                        <dd>{{ product.restriction }}</dd>
                      </div>
                      <div>
                        <dt>가입방법</dt>
                        <dd>{{ product.way }}</dd>
                      </div>
                      <div class="md:col-span-2">
                        <dt>우대조건</dt>
                        <dd class="whitespace-pre-line">{{ product.special || '특별 우대 조건 없음' }}</dd>
                      </div>
                    </div>
                    <h3 class="text-lg font-semibold text-gray-800 mb-2">금리 정보 (세전)</h3>
                    <div class="space-y-1 detail-section">
                      <p v-if="!hasInterestRatesForProduct(product)">금리 정보 없음</p>
                      <p v-else v-for="(rate, term) in product.rates" :key="term">
                        <span class="font-medium">{{ term }}개월:</span> {{ formatRate(rate) }}
                      </p>
                    </div>
                    <div
                      class="mt-6 flex flex-col sm:flex-row justify-center items-center space-y-2 sm:space-y-0 sm:space-x-3">
                      <button v-if="isLoggedIn" @click="handleSaveProduct(product)" :disabled="isProductSaved(product)"
                        :class="[
                          'py-2.5 px-6 rounded-lg font-medium transition-colors',
                          isProductSaved(product) ? 'bg-green-500 text-white cursor-not-allowed' : 'bg-sky-500 text-white hover:bg-sky-600'
                        ]">
                        {{ isProductSaved(product) ? '저장됨' : 'MyPage에 저장' }}
                      </button>
                      <p v-if="!isLoggedIn" class="text-sm text-red-500">상품을 저장하려면 로그인이 필요합니다.</p>
                      <!-- "가입하기" button removed -->
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
import { fetchDepositProducts, fetchSavingsProducts, saveFinancialProduct } from '@/api/depositSavingsApi';
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
  const banks = new Set(allProducts.value.map(p => p.bank));
  return Array.from(banks).sort();
});

const filteredAndSortedProducts = computed(() => {
  let productsToDisplay = allProducts.value.filter(product =>
    selectedBank.value === 'all' || product.bank === selectedBank.value
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
    const [fin_co_no, fin_prdt_cd] = productToCheck.id.split('_');
    return authUser.value.saved_financial_products.some(savedProd =>
      savedProd.fin_co_no === fin_co_no &&
      savedProd.fin_prdt_cd === fin_prdt_cd &&
      savedProd.product_type === currentProductType.value
    );
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

    const baseList = data && data.result && data.result.baseList ? data.result.baseList : [];
    const optionList = data && data.result && data.result.optionList ? data.result.optionList : [];

    const combinedProducts = baseList.map(base => {
      const options = optionList.filter(opt => opt.fin_prdt_cd === base.fin_prdt_cd && opt.fin_co_no === base.fin_co_no);
      const rates = {};
      options.forEach(opt => {
        rates[opt.save_trm] = opt.intr_rate;
      });

      return {
        id: `${base.fin_co_no}_${base.fin_prdt_cd}`,
        fin_co_no: base.fin_co_no, // Store separately for saving
        fin_prdt_cd: base.fin_prdt_cd, // Store separately for saving
        bank: base.kor_co_nm,
        name: base.fin_prdt_nm,
        rates: rates,
        submitMonth: base.dcls_month,
        restriction: base.join_deny === '1' ? '제한없음' : (base.join_deny === '2' ? '서민전용' : '일부제한'),
        way: base.join_way,
        special: base.spcl_cnd,
      };
    });
    allProducts.value = combinedProducts;
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
  // Triggered by bank filter change
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
    // Optionally, redirect to login: router.push({ name: 'login' });
    return;
  }
  if (isProductSaved.value(product)) {
    alert('이미 저장된 상품입니다.');
    return;
  }

  const productData = {
    product_type: currentProductType.value,
    fin_co_no: product.fin_co_no,
    fin_prdt_cd: product.fin_prdt_cd,
    product_name: product.name,
    bank_name: product.bank,
    interest_rate_12m: product.rates && product.rates['12'] ? parseFloat(product.rates['12']) : null,
  };

  try {
    await saveFinancialProduct(productData);
    alert('상품이 My Page에 저장되었습니다.');
    // Refresh user data to update the saved products list in the store
    await authStore.loadUser();
  } catch (error) {
    alert('상품 저장에 실패했습니다. 이미 저장된 상품일 수 있습니다.');
    console.error("Failed to save product:", error);
  }
};

// joinProduct function removed as the button is removed

onMounted(() => {
  if (isLoggedIn.value && !authUser.value) { // Ensure authUser is loaded if logged in
    authStore.loadUser();
  }
  fetchData();
});
</script>

<style scoped>
/* Tailwind CSS is typically handled by postcss/tailwind.config.js */
/* Custom styles from deposit_savings.html that are not pure Tailwind classes */
.hidden {
  display: none !important;
}


/* Override for Vue's v-if/v-show if needed, but v-if is preferred */

.menu-bar a {
  padding: 0.5rem 0.75rem;
  border-radius: 0.375rem;
  transition: background-color 0.2s ease-in-out, color 0.2s ease-in-out;
  white-space: nowrap;
}

.menu-bar a:hover {
  background-color: #f0fdfa;
  color: #0d9488;
}

.menu-bar a.active {
  color: #0d9488;
  font-weight: 600;
  border-bottom: 2px solid #0d9488;
  padding-bottom: calc(0.5rem - 2px);
}

.tab-button,
.sort-button {
  padding: 0.625rem 1.25rem;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s, border-color 0.2s;
  border: 1px solid transparent;
  text-align: center;
}

.tab-button.active,
.sort-button.active {
  background-color: #0d9488;
  color: white;
  border-color: #0d9488;
}

.tab-button:not(.active),
.sort-button:not(.active) {
  background-color: #e5e7eb;
  color: #374151;
  border-color: #d1d5db;
}

.tab-button:not(.active):hover,
.sort-button:not(.active):hover {
  background-color: #d1d5db;

  =======.tab-button,
  .sort-button {
    padding: 0.625rem 1.25rem;
    border-radius: 0.375rem;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s, color 0.2s, border-color 0.2s;
    border: 1px solid transparent;
    text-align: center;
  }

  .tab-button.active,
  .sort-button.active {
    background-color: #0d9488;
    /* teal-600 */
    color: white;
    border-color: #0d9488;
    /* teal-600 */
  }

  .tab-button:not(.active),
  .sort-button:not(.active) {
    background-color: #e5e7eb;
    /* gray-200 */
    color: #374151;
    /* gray-700 */
    border-color: #d1d5db;
    /* gray-300 */
  }

  .tab-button:not(.active):hover,
  .sort-button:not(.active):hover {
    background-color: #d1d5db;
    /* gray-300 */
  }

  .form-select {
    padding: 0.625rem 2.5rem 0.625rem 0.75rem;
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
    background-color: white;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20' fill='currentColor'%3E%3Cpath fill-rule='evenodd' d='M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z' clip-rule='evenodd'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 0.5rem center;
    background-size: 1.5em 1.5em;
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
  }

  .form-select:focus {
    outline: none;
    border-color: #0d9488;
    box-shadow: 0 0 0 0.2rem rgba(13, 148, 136, 0.25);
    border-color: #0d9488;
    /* teal-600 */
    box-shadow: 0 0 0 0.2rem rgba(13, 148, 136, 0.25);
    /* ring-teal-500 opacity-25 */
  }

  .table-container {
    overflow-x: auto;
  }

  .product-table th,
  .product-table td {
    padding: 0.75rem 1rem;
    text-align: left;
    font-size: 0.875rem;
    border-bottom: 1px solid #e5e7eb;
  }

  .product-table thead th {
    background-color: #f3f4f6;
    color: #374151;
    font-weight: 600;
  }

  .product-table tbody tr:hover {
    background-color: #f0fdfa;
  }

  .product-table .product-name-link {
    color: #0d9488;
    background-color: #f0fdfa;
    /* teal-50 */
  }

  .product-table .product-name-link {
    color: #0d9488;
    /* teal-600 */
    cursor: pointer;
    font-weight: 500;
  }

  .product-table .product-name-link:hover {
    text-decoration: underline;
  }

  .detail-section dt {
    font-weight: 500;
    color: #4b5563;
  }

  .detail-section dd {
    color: #1f2937;
    =======color: #4b5563;
    /* gray-600 */
  }

  .detail-section dd {
    color: #1f2937;
    /* gray-800 */
  }</style>
