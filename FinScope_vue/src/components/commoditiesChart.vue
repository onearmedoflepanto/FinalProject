<template>
  <div>
    <div class="chart-wrapper">
      <Bar :data="chartData" :options="chartOptions" v-if="chartData.labels.length" />
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
    };
  },
  mounted() {
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
      })
      .catch((error) => {
        console.error('API fetch error:', error);
      });
  },
};
</script>

<style scoped>
.chart-wrapper {
  height: 100%;
  min-height: 0;
  color: white;
}
</style>
