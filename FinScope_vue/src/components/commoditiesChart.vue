<template>
  <div>
    <div class="chart-wrapper">
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
        plugins: {
          legend: {
            display: true,
          },
          title: {
            display: false,
          },
        },
        scales: {
          y: {
            type: 'linear',
            position: 'left',
            title: {
              display: true,
              text: 'Gold',
            },
          },
          y1: {
            type: 'linear',
            position: 'right',
            grid: {
              drawOnChartArea: false,
            },
            title: {
              display: true,
              text: 'Silver & Oil',
            },
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
            },
            {
              label: 'Silver',
              data: [null, silver, null],
              backgroundColor: '#C0C0C0',
              yAxisID: 'y1',
            },
            {
              label: 'Oil',
              data: [null, null, oil],
              backgroundColor: '#808000',
              yAxisID: 'y1',
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
  background-color: white; /* Add white background */
  padding: 10px; /* Add some padding */
  border-radius: 8px; /* Optional: add rounded corners */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Add a subtle shadow */
}
</style>
