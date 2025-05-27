<style scoped>
/* Keep existing styles for controls, inputs, and general layout */
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
.date-input::-webkit-calendar-picker-indicator {
  filter: invert(1);
}

.chart-wrapper { /* Renamed from chart-container for clarity with ApexCharts */
  position: relative;
  width: 100%;
  background-color: #1F2937; /* bg-gray-800 */
  border-radius: 0.5rem; /* rounded-lg */
  padding: 1rem; /* p-4 */
  border: 1px solid #374151; /* border-gray-700 */
}

/* Define primary color as CSS variable if not already global */
:root {
  --color-primary: #0ea5e9; /* Example: sky-500 */
}
</style>

<template>
  <div class="bg-gray-900 text-gray-100 min-h-screen">
    <main class="flex-grow container mx-auto px-4 sm:px-6 py-8 md:py-12">
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
                    :class="['control-button', currentCommodity === 'gold' ? 'active' : '']">금 (Gold)</button>
            <button @click="selectCommodity('silver')" 
                    :class="['control-button', currentCommodity === 'silver' ? 'active' : '']">은 (Silver)</button>
            <button @click="selectCommodity('oil')" 
                    :class="['control-button', currentCommodity === 'oil' ? 'active' : '']">유가 (Oil)</button>
          </div>
        </div>

        <div class="chart-wrapper min-h-[400px] sm:min-h-[500px] md:min-h-[600px]">
          <apexchart v-if="!loading && series[0] && series[0].data.length > 0" type="line" height="100%" width="100%" :options="chartOptions" :series="series"></apexchart>
          <p v-if="loading" class="text-gray-400 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">{{ loadingMessage }}</p>
          <p v-if="!loading && series[0] && series[0].data.length === 0" class="text-gray-500 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">선택된 기간에 대한 데이터가 없습니다.</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, computed } from 'vue';
import VueApexCharts from 'vue3-apexcharts';
import { fetchCommodityData } from '@/api/stockfetch.js';
import { parseISO, format, isAfter, isBefore, isSameDay, isValid } from 'date-fns';

const currentCommodity = ref('gold');
const startDate = ref('');
const endDate = ref('');
const loading = ref(false);
const loadingMessage = ref('');

// ApexCharts series format: [{ name: 'Series Name', data: [[timestamp, value], ...] }]
const series = ref([{ name: '', data: [] }]);

// ApexCharts options
const chartOptions = ref({
  chart: {
    type: 'line',
    height: '100%', // Ensure chart takes full height of its container
    background: '#1F2937', // bg-gray-800
    foreColor: '#D1D5DB', // text-gray-300 for general text
    toolbar: {
      show: true,
      tools: {
        download: true,
        selection: true,
        zoom: true,
        zoomin: true,
        zoomout: true,
        pan: true,
        reset: true
      },
      autoSelected: 'zoom'
    },
    animations: {
      enabled: true,
      easing: 'easeinout',
      speed: 800,
      animateGradually: {
        enabled: true,
        delay: 150
      },
      dynamicAnimation: {
        enabled: true,
        speed: 350
      }
    }
  },
  theme: {
    mode: 'dark',
    palette: 'palette1' // You can choose different palettes
  },
  stroke: {
    curve: 'smooth',
    width: 2,
  },
  markers: {
    size: 0, // No markers by default, or set a small size
    hover: {
      size: 5
    }
  },
  xaxis: {
    type: 'datetime',
    labels: {
      datetimeUTC: false, // Important if your timestamps are local
      format: 'MMM dd', // Format for x-axis labels
      style: {
        colors: '#9CA3AF' // text-gray-400
      }
    },
    title: {
      text: '날짜 / 시간',
      style: {
        color: '#9CA3AF' // text-gray-400
      }
    },
    tooltip: {
      enabled: true,
      x: {
        format: 'yyyy-MM-dd HH:mm' // Format for x-axis tooltip
      }
    }
  },
  yaxis: {
    title: {
      text: '가격 (USD)',
      style: {
        color: '#9CA3AF' // text-gray-400
      }
    },
    labels: {
      formatter: function (value) {
        return '$' + value.toFixed(2);
      },
      style: {
        colors: '#9CA3AF' // text-gray-400
      }
    }
  },
  tooltip: {
    theme: 'dark',
    x: {
      format: 'dd MMM yyyy HH:mm' // More detailed tooltip date format
    },
  },
  grid: {
    borderColor: '#374151', // border-gray-700
  },
  dataLabels: {
    enabled: false
  },
  noData: {
    text: '데이터를 불러오는 중이거나 데이터가 없습니다...',
    align: 'center',
    verticalAlign: 'middle',
    offsetX: 0,
    offsetY: 0,
    style: {
      color: '#9CA3AF',
      fontSize: '14px',
    }
  }
});

const commodityColors = {
  gold: '#FBBF24',   // Tailwind yellow-400
  silver: '#9CA3AF', // Tailwind gray-400
  oil: '#8B5CF6',    // Tailwind violet-500
};

function commodityName(type) {
  if (type === 'gold') return '금';
  if (type === 'silver') return '은';
  if (type === 'oil') return '유가';
  return '';
}

function filterData(data) {
  const s = startDate.value ? parseISO(startDate.value) : null;
  const e = endDate.value ? parseISO(endDate.value) : null;

  return data.filter(({ Date: dateObj }) => {
    const d = dateObj; // Already a Date object from parseISO
    if (!isValid(d)) return false;
    const after = s ? isSameDay(d, s) || isAfter(d, s) : true;
    const before = e ? isSameDay(d, e) || isBefore(d, e) : true;
    return after && before;
  });
}

async function loadAndProcessData() {
  loading.value = true;
  loadingMessage.value = `${commodityName(currentCommodity.value)} 가격 데이터를 불러오는 중...`;
  
  try {
    const fetchedData = await fetchCommodityData(currentCommodity.value);
    const processedData = fetchedData.map(item => ({
      x: item.Date, // Keep as string for ApexCharts, it handles ISO strings
      y: item.Price
    }));

    const filtered = filterData(fetchedData.map(item => ({ // filterData expects { Date: DateObject, Price: number }
        Date: parseISO(item.Date), 
        Price: item.Price
    })));

    // Update series
    series.value = [{
      name: `${commodityName(currentCommodity.value)} 가격 (USD)`,
      data: filtered.map(item => [new Date(item.Date).getTime(), item.Price]) // ApexCharts expects [timestamp, value]
    }];

    // Update chart options (e.g., color)
    chartOptions.value = {
      ...chartOptions.value,
      colors: [commodityColors[currentCommodity.value] || '#0ea5e9'],
      xaxis: { // Ensure xaxis is updated if its properties depend on data range, though usually not needed for datetime
        ...chartOptions.value.xaxis,
        // min: filtered.length ? new Date(filtered[0].Date).getTime() : undefined,
        // max: filtered.length ? new Date(filtered[filtered.length - 1].Date).getTime() : undefined,
      },
      title: {
        text: `${commodityName(currentCommodity.value)} 가격 변동`,
        align: 'center',
        style: {
          color: '#F3F4F6' // text-gray-100
        }
      }
    };

  } catch (error) {
    console.error("Error loading commodity data:", error);
    series.value = [{ name: commodityName(currentCommodity.value), data: [] }]; // Clear data on error
  } finally {
    loading.value = false;
  }
}

function selectCommodity(commodity) {
  currentCommodity.value = commodity;
  // Data will be reloaded by the watcher
}

watch([currentCommodity, startDate, endDate], () => {
  loadAndProcessData();
}, { immediate: false }); // Will be called by onMounted initially

onMounted(() => {
  const today = new Date();
  const thirtyDaysAgo = new Date(new Date().setDate(today.getDate() - 30));
  startDate.value = format(thirtyDaysAgo, 'yyyy-MM-dd');
  endDate.value = format(today, 'yyyy-MM-dd');
  
  loadAndProcessData(); // Initial data load
});

</script>
