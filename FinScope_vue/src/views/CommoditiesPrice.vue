<style scoped>
canvas {
  max-width: 100%;
  height: 400px;
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
  height: 400px;
  width: 100%;
  background-color: #f9fafb;
  border-radius: 0.5rem;
  padding: 1rem;
  border: 1px solid #e5e7eb;
}
</style>

<template>
  <div class="p-4">
    <div class="flex space-x-4 mb-4">
      <button @click="selectCommodity('gold')" :class="btnClass('gold')">금</button>
      <button @click="selectCommodity('silver')" :class="btnClass('silver')">은</button>
      <button @click="selectCommodity('oil')" :class="btnClass('oil')">유가</button>
    </div>

    <div class="mb-4">
      <label>시작일: <input type="date" v-model="startDate" /></label>
      <label class="ml-4">종료일: <input type="date" v-model="endDate" /></label>
    </div>

    <p v-if="loading">{{ loadingMessage }}</p>
    <canvas v-show="!loading && chartData.length" ref="chartCanvas" class="w-full h-96"></canvas>
    <p v-if="!loading && !chartData.length">데이터가 없습니다.</p>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { fetchCommodityData } from '@/api/stockfetch.js'
import { parseISO, isAfter, isBefore, isSameDay, isValid, formatISO } from 'date-fns'
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


async function loadData() {
  loading.value = true
  loadingMessage.value = `${commodityName(currentCommodity.value)} 가격 데이터를 불러오는 중...`
  const raw = await fetchCommodityData(currentCommodity.value)
  chartData.value = filterData(raw)
  renderChart()
  loading.value = false
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

  return data.filter(({ Date }) => {
    const d = parseISO(Date)
    if (!isValid(d)) return false
    const after = s ? isSameDay(d, s) || isAfter(d, s) : true
    const before = e ? isSameDay(d, e) || isBefore(d, e) : true
    return after && before
  })
}

function renderChart() {
  if (chartInstance.value) chartInstance.value.destroy()

  if (!chartCanvas.value || !chartData.value.length) return

  const ctx = chartCanvas.value.getContext('2d')
  const borderColor = currentCommodity.value === 'gold' ? '#FBBF24' :
    currentCommodity.value === 'silver' ? '#A0AEC0' : '#8B5CF6'
  const backgroundColor = borderColor.replace(')', ', 0.2)').replace('rgb', 'rgba')

  chartInstance.value = new Chart(ctx, {
    type: 'line',
    data: {
      labels: chartData.value.map(d => d.Date),
      datasets: [{
        label: `${commodityName(currentCommodity.value)} 가격 (USD)`,
        data: chartData.value.map(d => d.Price),
        borderColor,
        backgroundColor,
        tension: 0.1,
        borderWidth: 2,
        pointRadius: chartData.value.length < 50 ? 3 : 1,
        pointHoverRadius: 5
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          type: 'time',
          time: {
            unit: 'month',
            tooltipFormat: 'yyyy-MM-dd',
            displayFormats: { month: 'yyyy-MM' }
          },
          title: { display: true, text: '날짜' },
          ticks: { autoSkip: true, maxTicksLimit: 12 }
        },
        y: {
          title: { display: true, text: '가격 (USD)' },
          beginAtZero: false
        }
      },
      plugins: {
        tooltip: {
          mode: 'index',
          intersect: false,
          callbacks: {
            label: ctx => `${ctx.dataset.label || ''}: ${new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(ctx.parsed.y)}`
          }
        }
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
