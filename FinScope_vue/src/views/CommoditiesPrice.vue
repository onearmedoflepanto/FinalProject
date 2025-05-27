<style scoped>
canvas {
  max-width: 100%;
  height: 100%;
}

body {
  font-family: 'Inter', sans-serif;
  background-color: #f8fafc;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex-grow: 1;
}

.hidden {
  display: none !important;
}

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

.control-button {
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;
  transition: background-color 0.2s ease-in-out, color 0.2s ease-in-out, border-color 0.2s ease-in-out;
  border: 1px solid transparent;
}

.control-button.active {
  background-color: #0d9488;
  color: white;
  border-color: #0d9488;
}

.control-button:not(.active) {
  background-color: #e5e7eb;
  color: #374151;
}

.control-button:not(.active):hover {
  background-color: #d1d5db;
}

.date-input {
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.chart-container {
  position: relative;
  height: 600px;
  width: 100%;
  background-color: #f9fafb;
  border-radius: 0.5rem;
  padding: 1rem;
  border: 1px solid #e5e7eb;
}
</style>

<template>
  <main class="flex-grow container mx-auto px-4 sm:px-6 py-8 md:py-12">
    <div class="bg-white p-6 md:p-8 rounded-xl shadow-xl border border-gray-200">
      <h1 class="text-2xl md:text-3xl font-bold text-teal-700 mb-2 text-center">현물 상품 비교</h1>
      <p class="text-center text-gray-600 mb-8 text-lg">금/은/유가 가격 변동</p>

      <div class="flex flex-col sm:flex-row justify-center items-center gap-4 mb-8 p-4 bg-gray-100 rounded-lg">
        <div class="flex items-center gap-2">
          <label for="startDate" class="text-sm font-medium text-gray-700">시작일:</label>
          <input type="date" v-model="startDate" name="startDate" class="date-input">
        </div>
        <div class="flex items-center gap-2">
          <label for="endDate" class="text-sm font-medium text-gray-700">종료일:</label>
          <input type="date" v-model="endDate" name="endDate" class="date-input">
        </div>
        <div class="flex items-center gap-2 mt-4 sm:mt-0">
          <button @click="selectCommodity('gold')" class="control-button" :class="btnClass('gold')"
            :disabled="isButtonDisabled">금 (Gold)</button>
          <button @click="selectCommodity('silver')" class="control-button" :class="btnClass('silver')"
            :disabled="isButtonDisabled">은
            (Silver)</button>
          <button @click="selectCommodity('oil')" id="oilBtn" class="control-button" :class="btnClass('oil')"
            :disabled="isButtonDisabled">유가
            (Oil)</button>
        </div>
      </div>

      <div class="chart-container flex justify-center items-center min-h-[300px]">
        <canvas v-show="!loading && chartData.length" ref="chartCanvas"></canvas>
        <p v-if="loading">{{ loadingMessage }}</p>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { fetchCommodityData } from '@/api/stockfetch.js'
import { parseISO, isAfter, isBefore, isSameDay, isValid } from 'date-fns' // Removed formatISO
import { Chart, registerables } from 'chart.js'
import 'chartjs-adapter-date-fns'
Chart.register(...registerables)

const chartCanvas = ref(null)
const chartInstance = ref(null)

const currentCommodity = ref('gold')
const startDate = ref('')
const endDate = ref('')
const loading = ref(false)
const loadingMessage = ref('')
const chartData = ref([])
const isButtonDisabled = ref(false)


async function loadData() {
  loading.value = true
  isButtonDisabled.value = true
  loadingMessage.value = `${commodityName(currentCommodity.value)} 가격 데이터를 불러오는 중...`

  try {
    const fetchedData = await fetchCommodityData(currentCommodity.value) // fetchCommodityData now returns an array

    const processedData = fetchedData.map(item => ({
      Date: parseISO(item.Date), // item.Date is the full timestamp string
      Price: item.Price
    }));

    chartData.value = filterData(processedData);
    renderChart()
  } catch (error) {
    console.error("Error loading data:", error);
    // Optionally, display an error message to the user
  } finally {
    loading.value = false
    setTimeout(() => {
      isButtonDisabled.value = false
    }, 2000) // Disable buttons for 2 seconds after loading
  }
}
function selectCommodity(commodity) {
  currentCommodity.value = commodity
  loadData()
}

function commodityName(type) {
  return type === 'gold' ? '금' : type === 'silver' ? '은' : '유가'
}

function filterData(data) {
  const s = startDate.value ? parseISO(startDate.value) : null
  const e = endDate.value ? parseISO(endDate.value) : null

  return data.filter(({ Date: dateObj }) => {
    const d = dateObj
    if (!isValid(d)) return false
    const after = s ? isSameDay(d, s) || isAfter(d, s) : true
    const before = e ? isSameDay(d, e) || isBefore(d, e) : true
    return after && before
  })
}

function renderChart() {
  if (chartInstance.value) chartInstance.value.destroy()

  if (!chartCanvas.value || !chartData.value.length) {
    return
  }

  const ctx = chartCanvas.value.getContext('2d')
  const borderColor = currentCommodity.value === 'gold' ? '#FBBF24' :
    currentCommodity.value === 'silver' ? '#A0AEC0' : '#8B5CF6'
  const backgroundColor = borderColor.replace(')', ', 0.2)').replace('rgb', 'rgba')

  // const formattedLabels = ... // Removed this line
  chartInstance.value = new Chart(ctx, {
    type: 'line',
    data: {
      // labels: formattedLabels, // Removed this line, Chart.js generates labels for time scale
      datasets: [{
        label: `${commodityName(currentCommodity.value)} 가격`,
        data: chartData.value.map(item => ({ x: item.Date, y: item.Price })), // Use {x,y} data structure
        borderColor: borderColor,
        backgroundColor: backgroundColor,
        pointRadius: 0,
        borderWidth: 2,
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      scales: {
        x: {
          type: 'time', // Set x-axis to time scale
          time: {
            unit: 'hour', // Display units in hours
            tooltipFormat: 'yyyy-MM-dd HH:mm', // Format for tooltips
            displayFormats: { // Format for axis labels
              hour: 'HH:mm', // e.g., 10:00, 11:00
              minute: 'HH:mm' // In case data is more granular
            }
          },
          title: { display: true, text: '시간' }
        },
        y: {
          title: { display: true, text: '가격' },
          beginAtZero: false
        }
      },
      plugins: {
        legend: { display: true }
      }
    }
  })
}

watch([startDate, endDate], () => {
  loadData()
})

onMounted(() => {
  loadData()
})

function btnClass(type) {
  return currentCommodity.value === type ? 'bg-blue-500 text-white px-4 py-2 rounded' : 'bg-gray-200 text-black px-4 py-2 rounded'
}
</script>
