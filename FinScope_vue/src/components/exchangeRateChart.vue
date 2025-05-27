<template>
  <div class="h-full w-full">
    <div class="chart-wrapper w-full h-full">
      <Bar :data="chartData" :options="chartOptions" v-if="chartData.labels.length" />
      <div v-else-if="loading" class="text-center text-gray-700">Loading chart data...</div>
      <div v-else-if="error" class="text-center text-red-600">Error loading chart data.</div>
      <div v-else class="text-center text-gray-700">No chart data available.</div>
    </div>
  </div>
</template>

<script>
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'vue-chartjs';
import axios from 'axios';

ChartJS.register(
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
);

export default {
  name: 'exchangeRateChart',
  components: {
    Bar,
  },
  data() {
    return {
      chartData: {
        labels: [],
        datasets: [],
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            labels: {
              color: '#D1D5DB' // text-gray-300
            }
          },
          title: {
            display: false, // No title needed as per current setup
            // text: '환율 정보',
            // color: '#F3F4F6' // text-gray-100
          },
          tooltip: {
            backgroundColor: '#111827', // bg-gray-900
            titleColor: '#F3F4F6', // text-gray-100
            bodyColor: '#D1D5DB', // text-gray-300
            borderColor: '#374151', // border-gray-700
            borderWidth: 1
          }
        },
        scales: {
          x: {
            ticks: {
              color: '#9CA3AF' // text-gray-400
            },
            grid: {
              color: '#374151' // border-gray-700
            },
            stacked: true, // Stack bars on x-axis
            barPercentage: 0.3 // Reduced further to make bars thinner
          },
          y: {
            ticks: {
              color: '#9CA3AF' // text-gray-400
            },
            grid: {
              color: '#374151' // border-gray-700
            },
            stacked: true // Stack bars on y-axis
          }
        }
      },
      loading: true,
      error: null,
    }
  },
  mounted() {
    this.loading = true;
    axios
      .get('http://127.0.0.1:8000/api/stocks/exchange-summary/')
      .then((response) => {
        const { USD, JPY, CNY } = response.data;

        this.chartData = {
          labels: ['USD', 'JPY', 'CNY'],
          datasets: [
            {
              label: 'USD',
              data: [USD, null, null],
              backgroundColor: '#FFD700',
            },
            {
              label: 'JPY',
              data: [null, JPY, null],
              backgroundColor: '#C0C0C0',
            },
            {
              label: 'CNY',
              data: [null, null, CNY],
              backgroundColor: '#808000',
            },
          ],
        };
        this.loading = false;
      })
      .catch((error) => {
        console.error('API fetch error:', error);
        this.error = error;
        this.loading = false;
      });
  },
};
</script>

<style scoped>
.chart-wrapper {
  height: 100%;
  min-height: 0;
  background-color: #1F2937; /* bg-gray-800, consistent with commoditiesChart */
  padding: 1rem; /* p-4, consistent with commoditiesChart */
  border-radius: 0.5rem; /* rounded-lg, consistent */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Add a subtle shadow */
}
</style>
