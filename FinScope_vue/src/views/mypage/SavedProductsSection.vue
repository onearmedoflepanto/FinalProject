<template>
  <div class="content-section">
    <h2 class="text-2xl font-semibold mb-6 text-gray-800 border-b-2 border-emerald-500 pb-3">저장한 금융 상품</h2>
    <div v-if="loading" class="text-center text-gray-500 py-4">정보를 불러오는 중...</div>
    <div v-else>
      <div class="space-y-4 mb-8 max-h-[400px] overflow-y-auto pr-2">
        <div v-if="!savedProductsList || savedProductsList.length === 0" class="text-gray-500 p-4 text-center">저장한 상품이 없습니다.</div>
        <div v-for="product in savedProductsList" :key="product.id" class="list-item">
          <div class="flex justify-between items-start">
            <div>
              <h3 class="text-emerald-600">{{ product.product_name }}</h3>
              <p class="text-sm text-gray-500">{{ product.bank_name }} - {{ product.product_type === 'deposit' ? '정기예금' : '정기적금' }}</p>
            </div>
            <button @click="handleUnsaveProduct(product.id)" class="text-sm text-red-500 hover:text-red-700 font-medium">삭제</button>
          </div>
          <p class="text-xs text-gray-400 mt-1">저장일: {{ formatDate(product.saved_at) }}</p>
          <p v-if="product.interest_rate_12m !== null && product.interest_rate_12m !== undefined" class="text-xs text-gray-500 mt-1">저장된 12개월 금리: <span class="font-semibold">{{ product.interest_rate_12m }}%</span></p>
        </div>
      </div>
      <h3 class="text-xl font-semibold mb-4 text-gray-700 mt-8">저장 상품 12개월 금리 비교</h3>
      <div class="w-full h-72 md:h-80 bg-gray-50 rounded-lg flex items-center justify-center text-gray-500 p-4 relative border border-gray-200">
        <canvas ref="savedProductsChartCanvas"></canvas>
        <p v-if="chartLoading" class="absolute inset-0 flex items-center justify-center text-gray-500 z-10">차트 로딩 중...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick, computed } from 'vue';
import Chart from 'chart.js/auto';
import { useAuthStore } from '@/stores/user';
import { storeToRefs } from 'pinia';
import { unsaveFinancialProduct } from '@/api/depositSavingsApi';

const authStore = useAuthStore();
const { user: authUser, isLoggedIn } = storeToRefs(authStore);

const loading = ref(false);
const savedProductsList = computed(() => authUser.value?.saved_financial_products || []);

const savedProductsChartCanvas = ref(null);
let savedProductsChartInstance = null;
const chartLoading = ref(false);

const formatDate = (dateString) => {
  if (!dateString) return '';
  const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
  return new Date(dateString).toLocaleDateString('ko-KR', options);
};

const handleUnsaveProduct = async (savedProductId) => {
  if (!confirm('이 상품을 저장 목록에서 삭제하시겠습니까?')) return;
  try {
    await unsaveFinancialProduct(savedProductId);
    alert('상품이 저장 목록에서 삭제되었습니다.');
    await authStore.loadUser(); 
  } catch (error) {
    alert('상품 삭제에 실패했습니다.');
    console.error("Failed to unsave product:", error);
  }
};

const renderSavedProductsChart = async () => {
  if (!savedProductsChartCanvas.value) return;
  chartLoading.value = true;
  await nextTick();

  if (savedProductsChartInstance) {
    savedProductsChartInstance.destroy();
  }

  const productsForChart = savedProductsList.value.map(p => ({
    name: p.product_name,
    // If interest_rate_12m is null or undefined, plot it as 0 for the chart.
    // The list view will still show if it's actually null.
    rate: (p.interest_rate_12m !== null && p.interest_rate_12m !== undefined) ? parseFloat(p.interest_rate_12m) : 0
  }));

  // Sort by rate descending for better visualization
  productsForChart.sort((a, b) => b.rate - a.rate);

  setTimeout(() => { // Simulating data processing
    try {
      const productNames = productsForChart.map(p => p.name);
      const rates = productsForChart.map(p => p.rate);
      
      if (productNames.length === 0) {
        chartLoading.value = false;
        const ctx = savedProductsChartCanvas.value.getContext('2d');
        ctx.clearRect(0, 0, savedProductsChartCanvas.value.width, savedProductsChartCanvas.value.height);
        ctx.font = "16px Arial";
        ctx.textAlign = 'center';
        ctx.fillText('차트에 표시할 금리 정보가 없습니다.', savedProductsChartCanvas.value.width / 2, savedProductsChartCanvas.value.height / 2); // Updated message
        return;
      }
      
      const greenShades = [
        'rgba(5, 150, 105, 0.7)',   // emerald-600
        'rgba(16, 185, 129, 0.7)',  // emerald-500
        'rgba(52, 211, 153, 0.7)',  // emerald-400
        'rgba(22, 163, 74, 0.7)',   // green-600
        'rgba(34, 197, 94, 0.7)',   // green-500
      ];
      const borderGreenShades = [
        'rgba(5, 150, 105, 1)',    // emerald-600
        'rgba(16, 185, 129, 1)',   // emerald-500
        'rgba(52, 211, 153, 1)',   // emerald-400
        'rgba(22, 163, 74, 1)',    // green-600
        'rgba(34, 197, 94, 1)',    // green-500
      ];

      const ctx = savedProductsChartCanvas.value.getContext('2d');
      savedProductsChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: productNames,
          datasets: [
            {
              label: '12개월 금리 (%)',
              data: rates,
              backgroundColor: productNames.map((_, i) => greenShades[i % greenShades.length]),
              borderColor: productNames.map((_, i) => borderGreenShades[i % borderGreenShades.length]),
              borderWidth: 1,
              borderRadius: 4,
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: 'y', 
          scales: {
            x: { 
              beginAtZero: true, 
              title: { display: true, text: '금리 (%)' }
            },
            y: { 
              grid: { display: false } 
            }
          },
          plugins: {
            legend: { 
              display: true,
              position: 'top',
            },
            title: { 
              display: true, 
              text: '저장된 상품 12개월 금리 비교', 
              font: {size: 16, weight: 'bold'}, 
              padding: {top:10, bottom:20} 
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  let label = context.dataset.label || '';
                  if (label) {
                    label += ': ';
                  }
                  if (context.parsed.x !== null) {
                    label += context.parsed.x.toFixed(2) + '%';
                  }
                  return label;
                }
              }
            }
          },
        }
      });
      chartLoading.value = false;
    } catch (error) {
      console.error("저장 상품 차트 초기화 오류:", error);
      chartLoading.value = false;
       const ctx = savedProductsChartCanvas.value.getContext('2d');
        ctx.clearRect(0, 0, savedProductsChartCanvas.value.width, savedProductsChartCanvas.value.height);
        ctx.font = "16px Arial";
        ctx.textAlign = 'center';
        ctx.fillText('차트 로딩 중 오류 발생.', savedProductsChartCanvas.value.width / 2, savedProductsChartCanvas.value.height / 2);
    }
  }, 200);
};

watch(savedProductsList, () => {
  renderSavedProductsChart();
}, { deep: true });

onMounted(async () => {
  loading.value = true;
  if (isLoggedIn.value && (!authUser.value || !authUser.value.saved_financial_products)) { 
    await authStore.loadUser(); 
  }
  renderSavedProductsChart(); // Call directly as watcher might not fire if authUser was already populated
  loading.value = false;
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
    margin-bottom: 1rem;
}
.list-item:hover {
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06); /* shadow-md */
}
.list-item h3 {
    font-size: 1.125rem; /* text-lg */
    font-weight: 600; /* font-semibold */
    /* color: #10b981; emerald-600 applied via Tailwind */
    margin-bottom: 0.25rem;
}
</style>
