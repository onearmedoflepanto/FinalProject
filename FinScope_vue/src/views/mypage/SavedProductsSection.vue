<template>
  <div class="content-section p-6 sm:p-8">
    <h2 class="text-2xl font-bold text-primary-light mb-6 pb-3 border-b-2 border-primary-dark">저장한 금융 상품</h2>
    <div v-if="loading" class="text-center text-gray-400 py-4">정보를 불러오는 중...</div>
    <div v-else>
      <div class="space-y-4 mb-8 max-h-[400px] overflow-y-auto pr-3 custom-scrollbar-dark-local">
        <div v-if="!savedProductsList || savedProductsList.length === 0" class="text-gray-400 p-6 text-center bg-gray-700 rounded-md">저장한 상품이 없습니다.</div>
        <div v-for="product in savedProductsList" :key="product.id" class="list-item-card-dark-local">
          <div class="flex justify-between items-start">
            <div>
              <h3 class="text-lg font-semibold text-primary-light mb-1">{{ product.product_name }}</h3>
              <p class="text-sm text-gray-400">{{ product.bank_name }} - {{ product.product_type === 'deposit' ? '정기예금' : '정기적금' }}</p>
            </div>
            <div class="flex space-x-2">
              <button 
                @click="handleToggleProductNotification(product)"
                :class="[
                  'text-xs font-medium py-1 px-3 rounded-md transition-colors duration-150',
                  isSubscribedToProductNotifications(product) 
                    ? 'bg-red-600 hover:bg-red-700 text-white' 
                    : 'bg-primary hover:bg-primary-dark text-white'
                ]">
                {{ isSubscribedToProductNotifications(product) ? '알림 해제' : '알림 설정' }}
              </button>
              <button @click="handleUnsaveProduct(product.id)" class="text-xs text-gray-300 hover:text-white font-medium py-1 px-3 rounded-md bg-gray-600 hover:bg-gray-500 transition-colors">삭제</button>
            </div>
          </div>
          <p class="text-xs text-gray-500 mt-1">저장일: {{ formatDate(product.saved_at) }}</p>
          <p v-if="product.interest_rate_12m !== null && product.interest_rate_12m !== undefined" class="text-xs text-gray-400 mt-1">저장된 12개월 금리: <span class="font-semibold text-gray-200">{{ product.interest_rate_12m }}%</span></p>
          <p class="text-xs text-gray-400 mt-1">금리변동 알림: <span :class="product.notify_on_rate_change ? 'text-green-400 font-semibold' : 'text-red-400 font-semibold'">{{ product.notify_on_rate_change ? '설정됨' : '해제됨' }}</span></p>
        </div>
      </div>
      <h3 class="text-xl font-semibold mb-4 text-gray-200 mt-8">저장 상품 12개월 금리 비교</h3>
      <div class="w-full h-80 md:h-96 bg-gray-800 rounded-lg p-4 relative border border-gray-700 shadow-md">
        <canvas ref="savedProductsChartCanvas"></canvas>
        <p v-if="chartLoading" class="absolute inset-0 flex items-center justify-center text-gray-400 z-10 bg-gray-800 bg-opacity-75 rounded-lg">차트 로딩 중...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick, computed } from 'vue';
import Chart from 'chart.js/auto';
import { useAuthStore } from '@/stores/user';
import { storeToRefs } from 'pinia';
import { unsaveFinancialProduct, toggleNotificationSubscription } from '@/api/depositSavingsApi'; // Import toggleNotificationSubscription

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

const isSubscribedToProductNotifications = computed(() => {
  return (productToCheck) => {
    // productToCheck is an item from savedProductsList, which directly has notify_on_rate_change
    return productToCheck.notify_on_rate_change;
  };
});

const handleToggleProductNotification = async (product) => {
  if (!isLoggedIn.value) {
    alert('알림 설정을 변경하려면 로그인이 필요합니다.');
    return;
  }

  // 'product' here is an item from the savedProductsList
  // It already contains 'id' (PK of SavedFinancialProduct) and 'notify_on_rate_change'
  const savedProductId = product.id;
  const currentStatus = product.notify_on_rate_change;
  const newStatus = !currentStatus;

  try {
    const updatedSubscription = await toggleNotificationSubscription(savedProductId, newStatus);
    // Update the local state in the authStore to reflect the change immediately
    const productIndex = authUser.value.saved_financial_products.findIndex(p => p.id === savedProductId);
    if (productIndex !== -1) {
      authUser.value.saved_financial_products[productIndex].notify_on_rate_change = updatedSubscription.notify_on_rate_change;
    }
    alert(`금리 변동 알림이 ${newStatus ? '설정' : '해제'}되었습니다.`);
  } catch (error) {
    alert('알림 설정 변경에 실패했습니다.');
    console.error("Failed to toggle notification for saved product:", error);
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
    rate: (p.interest_rate_12m !== null && p.interest_rate_12m !== undefined) ? parseFloat(p.interest_rate_12m) : 0
  }));

  productsForChart.sort((a, b) => b.rate - a.rate);

  const chartTextColor = '#cbd5e1'; // slate-300 for dark theme text
  const chartGridColor = '#4b5563'; // gray-600 for dark theme grid lines

  setTimeout(() => { 
    try {
      const productNames = productsForChart.map(p => p.name);
      const rates = productsForChart.map(p => p.rate);
      
      if (productNames.length === 0) {
        chartLoading.value = false;
        const ctx = savedProductsChartCanvas.value.getContext('2d');
        ctx.clearRect(0, 0, savedProductsChartCanvas.value.width, savedProductsChartCanvas.value.height);
        ctx.font = "16px 'Noto Sans KR', sans-serif";
        ctx.fillStyle = chartTextColor;
        ctx.textAlign = 'center';
        ctx.fillText('차트에 표시할 금리 정보가 없습니다.', savedProductsChartCanvas.value.width / 2, savedProductsChartCanvas.value.height / 2);
        return;
      }
      
      // Using shades of blue (primary color) for the chart
      const blueShades = [
        'rgba(59, 130, 246, 0.7)',   // primary.light (blue-500)
        'rgba(37, 99, 235, 0.7)',    // primary.DEFAULT (blue-600)
        'rgba(29, 78, 216, 0.7)',    // primary.dark (blue-700)
        'rgba(96, 165, 250, 0.7)',   // blue-400
        'rgba(147, 197, 253, 0.7)',  // blue-300
      ];
      const borderBlueShades = [
        'rgba(59, 130, 246, 1)',
        'rgba(37, 99, 235, 1)',
        'rgba(29, 78, 216, 1)',
        'rgba(96, 165, 250, 1)',
        'rgba(147, 197, 253, 1)',
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
              backgroundColor: productNames.map((_, i) => blueShades[i % blueShades.length]),
              borderColor: productNames.map((_, i) => borderBlueShades[i % borderBlueShades.length]),
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
              title: { display: true, text: '금리 (%)', color: chartTextColor },
              grid: { color: chartGridColor },
              ticks: { color: chartTextColor }
            },
            y: { 
              grid: { display: false }, // Keep y-axis grid lines off for horizontal bar chart
              ticks: { color: chartTextColor }
            }
          },
          plugins: {
            legend: { 
              display: true,
              position: 'top',
              labels: { color: chartTextColor }
            },
            title: { 
              display: true, 
              text: '저장된 상품 12개월 금리 비교', 
              font: {size: 16, weight: 'bold'}, 
              color: chartTextColor,
              padding: {top:10, bottom:20} 
            },
            tooltip: {
              backgroundColor: '#1f2937', // gray-800
              titleColor: '#e5e7eb', // gray-200
              bodyColor: '#d1d5db', // gray-300
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
        ctx.font = "16px 'Noto Sans KR', sans-serif";
        ctx.fillStyle = chartTextColor;
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

/* Dark Theme List Item Card Styling specific to this component */
.list-item-card-dark-local {
  @apply bg-gray-900 p-4 rounded-lg border border-gray-700 shadow-md hover:shadow-lg transition-shadow duration-200;
  margin-bottom: 1rem; /* Retain margin from original .list-item */
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
</style>
