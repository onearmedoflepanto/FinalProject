<style scoped>
canvas {
  max-width: 100%;
  /* height: 100%; Ensure canvas can take full height of its container */
}

/* Removed body, main, hidden, menu-bar styles as they should be global or in App.vue */

.control-button {
  padding: 0.5rem 1rem;
  border-radius: 0.375rem; /* rounded-md */
  font-weight: 500; /* font-medium */
  transition: background-color 0.2s ease-in-out, color 0.2s ease-in-out, border-color 0.2s ease-in-out;
  border-width: 1px;
  border-style: solid;
}

.control-button.active {
  background-color: var(--color-primary); /* Use CSS variable for primary color */
  color: white;
  border-color: var(--color-primary);
}

.control-button:not(.active) {
  background-color: #4B5563; /* bg-gray-600 */
  color: #D1D5DB; /* text-gray-300 */
  border-color: #6B7280; /* border-gray-500 */
}

.control-button:not(.active):hover {
  background-color: #374151; /* bg-gray-700 */
  color: white;
}

.date-input {
  padding: 0.5rem 0.75rem;
  border: 1px solid #4B5563; /* border-gray-600 */
  border-radius: 0.375rem; /* rounded-md */
  font-size: 0.875rem; /* text-sm */
  background-color: #374151; /* bg-gray-700 */
  color: #F3F4F6; /* text-gray-100 */
}
/* Style for the date picker indicator */
.date-input::-webkit-calendar-picker-indicator {
  filter: invert(1); /* Makes the icon white for dark backgrounds */
}

.chart-container {
  position: relative;
  /* height: 600px; Let chart.js handle height or set via aspect ratio */
  width: 100%;
  background-color: #1F2937; /* bg-gray-800 */
  border-radius: 0.5rem; /* rounded-lg */
  padding: 1rem; /* p-4 */
  border: 1px solid #374151; /* border-gray-700 */
}

/* Define primary color as CSS variable for chart.js if not already global */
:root {
  --color-primary: #2563eb; /* Example primary color from your tailwind config */
}
</style>

<template>
  <main class="flex-grow container mx-auto px-4 sm:px-6 py-8 md:py-12 text-gray-100">
    <div class="bg-gray-800 p-6 md:p-8 rounded-xl shadow-xl border border-gray-700">
      <h1 class="text-2xl md:text-3xl font-bold text-primary-light mb-2 text-center">현물 상품 비교</h1>
      <p class="text-center text-gray-400 mb-8 text-lg">금/은/유가 가격 변동</p>

      <div class="flex flex-col sm:flex-row justify-center items-center gap-4 mb-8 p-4 bg-gray-700 rounded-lg">
        <div class="flex items-center gap-2">
          <label for="startDate" class="text-sm font-medium text-gray-300">시작일:</label>
          <input type="date" v-model="startDate" name="startDate" class="date-input">
        </div>
        <div class="flex items-center gap-2">
          <label for="endDate" class="text-sm font-medium text-gray-300">종료일:</label>
          <input type="date" v-model="endDate" name="endDate" class="date-input">
        </div>
        <div class="flex items-center gap-2 mt-4 sm:mt-0">
          <button @click="selectCommodity('gold')" 
                  :class="['control-button', currentCommodity === 'gold' ? 'active bg-primary text-white border-primary' : 'bg-gray-600 text-gray-300 border-gray-500 hover:bg-gray-500 hover:text-white']">금 (Gold)</button>
          <button @click="selectCommodity('silver')" 
                  :class="['control-button', currentCommodity === 'silver' ? 'active bg-primary text-white border-primary' : 'bg-gray-600 text-gray-300 border-gray-500 hover:bg-gray-500 hover:text-white']">은 (Silver)</button>
          <button @click="selectCommodity('oil')" 
                  :class="['control-button', currentCommodity === 'oil' ? 'active bg-primary text-white border-primary' : 'bg-gray-600 text-gray-300 border-gray-500 hover:bg-gray-500 hover:text-white']">유가 (Oil)</button>
        </div>
      </div>

      <div class="chart-container flex justify-center items-center min-h-[400px] sm:min-h-[500px] md:min-h-[600px]">
        <canvas v-show="!loading && chartData.length" ref="chartCanvas"></canvas>
        <p v-if="loading" class="text-gray-400">{{ loadingMessage }}</p>
         <p v-if="!loading && !chartData.length" class="text-gray-500">선택된 기간에 대한 데이터가 없습니다.</p>
      </div>
    </div>
  </main>
</template>

<script setup>
// Removed NavigationBar import, assuming it's globally available or in App.vue
import { ref, watch, onMounted, computed } from 'vue'; // Added computed
import { fetchCommodityData } from '@/api/stockfetch.js';
import { parseISO, isAfter, isBefore, isSameDay, isValid } from 'date-fns';
import { Chart, registerables } from 'chart.js';
import 'chartjs-adapter-date-fns';
Chart.register(...registerables);

const chartCanvas = ref(null);
const chartInstance = ref(null);

const currentCommodity = ref('gold');
const startDate = ref('');
const endDate = ref('');
const loading = ref(false);
const loadingMessage = ref('');
const chartData = ref([]);

// Helper to get Tailwind's primary color for the chart
const primaryColor = computed(() => getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim() || '#2563eb');


async function loadData() {
  loading.value = true;
  loadingMessage.value = `${commodityName(currentCommodity.value)} 가격 데이터를 불러오는 중...`;
  chartData.value = []; // Clear previous data

  try {
    const fetchedData = await fetchCommodityData(currentCommodity.value);
    const processedData = fetchedData.map(item => ({
      Date: parseISO(item.Date),
      Price: item.Price
    }));
    chartData.value = filterData(processedData);
  } catch (error) {
    console.error("Error loading commodity data:", error);
    // Optionally, set an error message to display to the user
  } finally {
    renderChart();
    loading.value = false;
  }
}
function selectCommodity(commodity) {
  currentCommodity.value = commodity;
  // loadData will be triggered by the watcher on currentCommodity
}

function commodityName(type) {
  return type === 'gold' ? '금' : type === 'silver' ? '은' : '유가';
}

function filterData(data) {
  const s = startDate.value ? parseISO(startDate.value) : null;
  const e = endDate.value ? parseISO(endDate.value) : null;

  return data.filter(({ Date: dateObj }) => {
    const d = dateObj;
    if (!isValid(d)) return false;
    const after = s ? isSameDay(d, s) || isAfter(d, s) : true;
    const before = e ? isSameDay(d, e) || isBefore(d, e) : true;
    return after && before;
  });
}

function renderChart() {
  if (chartInstance.value) {
    chartInstance.value.destroy();
  }

  if (!chartCanvas.value || !chartData.value.length) {
    return;
  }

  const ctx = chartCanvas.value.getContext('2d');
  const commodityType = currentCommodity.value;
  let borderColorVal = primaryColor.value; // Default to primary blue

  if (commodityType === 'gold') {
    borderColorVal = '#FBBF24'; // Tailwind yellow-400
  } else if (commodityType === 'silver') {
    borderColorVal = '#9CA3AF'; // Tailwind gray-400
  } else if (commodityType === 'oil') {
    borderColorVal = '#8B5CF6'; // Tailwind violet-500 (example, adjust as needed)
  }
  
  const backgroundColorVal = borderColorVal.startsWith('#') 
    ? `${borderColorVal}33` // Add 33 for ~20% opacity for hex
    : borderColorVal.replace('rgb', 'rgba').replace(')', ', 0.2)');


  chartInstance.value = new Chart(ctx, {
    type: 'line',
    data: {
      datasets: [{
        label: `${commodityName(commodityType)} 가격 (USD)`,
        data: chartData.value.map(item => ({ x: item.Date, y: item.Price })),
        borderColor: borderColorVal,
        backgroundColor: backgroundColorVal,
        pointRadius: 2,
        pointBackgroundColor: borderColorVal,
        borderWidth: 2,
        tension: 0.1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          type: 'time',
          time: {
            unit: 'day', // Adjust based on data granularity
            tooltipFormat: 'yyyy-MM-dd HH:mm',
            displayFormats: {
              day: 'MMM d',
              hour: 'HH:mm'
            }
          },
          title: { display: true, text: '날짜 / 시간', color: '#9CA3AF' }, // text-gray-400
          ticks: { color: '#9CA3AF' }, // text-gray-400
          grid: { color: '#374151' } // border-gray-700
        },
        y: {
          title: { display: true, text: '가격 (USD)', color: '#9CA3AF' }, // text-gray-400
          beginAtZero: false,
          ticks: { color: '#9CA3AF', callback: function(value) { return '$' + value; } }, // text-gray-400
          grid: { color: '#374151' } // border-gray-700
        }
      },
      plugins: {
        legend: { 
          display: true,
          labels: { color: '#D1D5DB' } // text-gray-300
        },
        tooltip: {
          backgroundColor: '#1F2937', // bg-gray-800
          titleColor: '#F3F4F6', // text-gray-100
          bodyColor: '#D1D5DB', // text-gray-300
          borderColor: '#374151', // border-gray-700
          borderWidth: 1
        }
      }
    }
  });
}

watch([startDate, endDate, currentCommodity], () => { // Watch currentCommodity as well
  loadData();
}, { immediate: false }); // Set immediate to false if loadData is called in onMounted

onMounted(() => {
  // Set default date range if needed, e.g., last 30 days
  const today = new Date();
  const thirtyDaysAgo = new Date(new Date().setDate(today.getDate() - 30));
  startDate.value = thirtyDaysAgo.toISOString().split('T')[0];
  endDate.value = today.toISOString().split('T')[0];
  
  loadData(); // Initial load
});

// btnClass is no longer needed as Tailwind classes are directly applied in the template
</script>
