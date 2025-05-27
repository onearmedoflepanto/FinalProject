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
  name: 'CommoditiesChart',
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
            display: false, // No main title needed as per current setup
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
          x: { // Added x-axis styling for consistency
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
            type: 'linear',
            position: 'left',
            title: {
              display: true,
              text: 'Gold Price (USD)',
              color: '#9CA3AF' // text-gray-400
            },
            ticks: {
              color: '#9CA3AF' // text-gray-400
            },
            grid: {
              color: '#374151' // border-gray-700
            },
            stacked: true // Stack bars on y-axis (for each category)
          },
          y1: {
            type: 'linear',
            position: 'right',
            grid: {
              drawOnChartArea: false, // Only show grid for the first y-axis
            },
            title: {
              display: true,
              text: 'Silver & Oil Price (USD)',
              color: '#9CA3AF' // text-gray-400
            },
            ticks: {
              color: '#9CA3AF' // text-gray-400
            },
            stacked: true // Stack bars on y1-axis (for each category)
          },
        },
      },
      loading: true,
      error: null,
    };
  },
  mounted() {
    this.loading = true;
    axios
      .get('http://127.0.0.1:8000/api/stocks/commodities-summary/?mode=latest')
      .then((response) => {
        const { gold, silver, oil } = response.data;

        this.chartData = {
          labels: ['Gold', 'Silver', 'Oil'],
          datasets: [
            {
              label: 'Gold',
              data: [gold, null, null],
              backgroundColor: '#FFD700',
              yAxisID: 'y',
              // barPercentage: 0.7, // Removed from dataset
              // categoryPercentage: 0.7, // Removed from dataset
            },
            {
              label: 'Silver',
              data: [null, silver, null],
              backgroundColor: '#C0C0C0',
              yAxisID: 'y1',
              // barPercentage: 0.7, // Removed from dataset
              // categoryPercentage: 0.7, // Removed from dataset
            },
            {
              label: 'Oil',
              data: [null, null, oil],
              backgroundColor: '#808000',
              yAxisID: 'y1',
              // barPercentage: 0.7, // Removed from dataset
              // categoryPercentage: 0.7, // Removed from dataset
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
  background-color: #1F2937; /* bg-gray-800 */
  padding: 1rem; /* p-4, consistent */
  border-radius: 0.5rem; /* rounded-lg, consistent */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Add a subtle shadow */
}
</style>
