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
        plugins: {
          legend: {
            display: true,
          },
          title: {
            display: false,
          },
        },
      },
    }
  },
  mounted() {
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
}
</style>
