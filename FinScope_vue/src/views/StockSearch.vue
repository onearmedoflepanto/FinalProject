<template>
  <div class="container mx-auto max-w-4xl">
    <div class="carousel-content-overlay">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-center">
        <div class="md:col-span-1">
          <h1 class="text-2xl font-bold whitespace-nowrap">종목 검색</h1>
        </div>
        <div class="md:col-span-2 flex">
          <input type="text" v-model="searchQuery" placeholder="종목명 또는 티커를 입력하세요"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" />
          <button @click="searchStock"
            class="ml-2 bg-teal-600 text-white px-8 py-2 rounded-lg hover:bg-teal-700 text-sm focus:outline-none focus:shadow-outline min-w-[100px]">
            검색
          </button>
        </div>
      </div>
    </div>

    <div class="mt-2">
      <div class="grid grid-cols-3 gap-4">
        <div class="col-span-1">
          <div class="p-2 rounded-md flex justify-start items-center space-x-2">
            <button
              class="inline-flex items-center justify-center border align-middle select-none font-sans font-medium text-center transition-all ease-in disabled:opacity-50 disabled:shadow-none disabled:cursor-not-allowed focus:shadow-none text-sm py-2 px-4 shadow-sm bg-transparent relative text-stone-700 hover:text-stone-700 border-stone-500 hover:bg-transparent duration-150 hover:border-stone-600 rounded-lg hover:opacity-60 hover:shadow-none"
              :class="{ 'hover:shadow-md bg-stone-800 hover:bg-stone-700 relative bg-gradient-to-b from-stone-700 to-stone-800 border-stone-900 text-stone-50 rounded-lg hover:bg-gradient-to-b hover:from-stone-800 hover:to-stone-800 hover:border-stone-900 after:absolute after:inset-0 after:rounded-[inherit] after:box-shadow after:shadow-[inset_0_1px_0px_rgba(255,255,255,0.25),inset_0_-2px_0px_rgba(0,0,0,0.35)] after:pointer-events-none transition-all antialiased': isDomestic }"
              @click="isDomestic = true">국내</button>
            <button
              class="inline-flex items-center justify-center border align-middle select-none font-sans font-medium text-center transition-all ease-in disabled:opacity-50 disabled:shadow-none disabled:cursor-not-allowed focus:shadow-none text-sm py-2 px-4 shadow-sm bg-transparent relative text-stone-700 hover:text-stone-700 border-stone-500 hover:bg-transparent duration-150 hover:border-stone-600 rounded-lg hover:opacity-60 hover:shadow-none"
              :class="{ 'hover:shadow-md bg-stone-800 hover:bg-stone-700 relative bg-gradient-to-b from-stone-700 to-stone-800 border-stone-900 text-stone-50 rounded-lg hover:bg-gradient-to-b hover:from-stone-800 hover:to-stone-800 hover:border-stone-900 after:absolute after:inset-0 after:rounded-[inherit] after:box-shadow after:shadow-[inset_0_1px_0px_rgba(255,255,255,0.25),inset_0_-2px_0px_rgba(0,0,0,0.35)] after:pointer-events-none transition-all antialiased': !isDomestic }"
              @click="isDomestic = false">해외</button>
          </div>
        </div>
        <div class="col-span-2">
          <div class="p-2 rounded-md flex justify-end items-center space-x-2">
            <button
              class="inline-flex items-center justify-center border align-middle select-none font-sans font-medium text-center transition-all ease-in disabled:opacity-50 disabled:shadow-none disabled:cursor-not-allowed focus:shadow-none text-sm py-2 px-4 shadow-sm bg-transparent relative text-stone-700 hover:text-stone-700 border-stone-500 hover:bg-transparent duration-150 hover:border-stone-600 rounded-lg hover:opacity-60 hover:shadow-none"
              :class="{ 'hover:shadow-md bg-stone-800 hover:bg-stone-700 relative bg-gradient-to-b from-stone-700 to-stone-800 border-stone-900 text-stone-50 rounded-lg hover:bg-gradient-to-b hover:from-stone-800 hover:to-stone-800 hover:border-stone-900 after:absolute after:inset-0 after:rounded-[inherit] after:box-shadow after:shadow-[inset_0_1px_0px_rgba(255,255,255,0.25),inset_0_-2px_0px_rgba(0,0,0,0.35)] after:pointer-events-none transition-all antialiased': listQuery === '거래량 급증' }"
              @click="listQuery = '거래량 급증'">거래량
              급증</button>
            <button
              class="inline-flex items-center justify-center border align-middle select-none font-sans font-medium text-center transition-all ease-in disabled:opacity-50 disabled:shadow-none disabled:cursor-not-allowed focus:shadow-none text-sm py-2 px-4 shadow-sm bg-transparent relative text-stone-700 hover:text-stone-700 border-stone-500 hover:bg-transparent duration-150 hover:border-stone-600 rounded-lg hover:opacity-60 hover:shadow-none"
              :class="{ 'hover:shadow-md bg-stone-800 hover:bg-stone-700 relative bg-gradient-to-b from-stone-700 to-stone-800 border-stone-900 text-stone-50 rounded-lg hover:bg-gradient-to-b hover:from-stone-800 hover:to-stone-800 hover:border-stone-900 after:absolute after:inset-0 after:rounded-[inherit] after:box-shadow after:shadow-[inset_0_1px_0px_rgba(255,255,255,0.25),inset_0_-2px_0px_rgba(0,0,0,0.35)] after:pointer-events-none transition-all antialiased': listQuery === '등락률 상위' }"
              @click="listQuery = '등락률 상위'">등락률
              상위</button>
            <button
              class="inline-flex items-center justify-center border align-middle select-none font-sans font-medium text-center transition-all ease-in disabled:opacity-50 disabled:shadow-none disabled:cursor-not-allowed focus:shadow-none text-sm py-2 px-4 shadow-sm bg-transparent relative text-stone-700 hover:text-stone-700 border-stone-500 hover:bg-transparent duration-150 hover:border-stone-600 rounded-lg hover:opacity-60 hover:shadow-none"
              :class="{ 'hover:shadow-md bg-stone-800 hover:bg-stone-700 relative bg-gradient-to-b from-stone-700 to-stone-800 border-stone-900 text-stone-50 rounded-lg hover:bg-gradient-to-b hover:from-stone-800 hover:to-stone-800 hover:border-stone-900 after:absolute after:inset-0 after:rounded-[inherit] after:box-shadow after:shadow-[inset_0_1px_0px_rgba(255,255,255,0.25),inset_0_-2px_0px_rgba(0,0,0,0.35)] after:pointer-events-none transition-all antialiased': listQuery === '시가총액 상위' }"
              @click="listQuery = '시가총액 상위'">시가총액
              상위</button>
          </div>
        </div>
      </div>
      <div>
        <p>isDomestic: {{ isDomestic }}</p>
        <p>listQuery: {{ listQuery }}</p>
      </div>
      <div class="mt-2">
        <table class="stock-table">
          <thead>
            <tr>
              <th>종목</th>
              <th>현재가</th>
              <th>등락률</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>소룩스</td>
              <td>3600원</td>
              <td>
                <span class="progress negative">-2.4%</span>
              </td>
            </tr>
            <tr>
              <td>큐로셀</td>
              <td>30350원</td>
              <td>
                <span class="progress positive">+2.5%</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
.stock-table {
  width: 100%;
  border-collapse: collapse;
}

.stock-table thead {
  background-color: #f0f5f9;
  /* Use Tailwind's gray-200 equivalent */
}

.stock-table th,
.stock-table td {
  padding: 0.75rem;
  text-align: center;
}

.stock-table tbody tr:hover {
  background-color: #f7fafc;
  /* Use Tailwind's gray-100 equivalent */
}

.stock-table tbody tr:nth-child(even) {
  background-color: #ffffff;
  /* White background for even rows */
}

.positive {
  color: #22c55e;
  /* Tailwind's green-500 equivalent */
}

.negative {
  color: #ef4444;
  /* Tailwind's red-500 equivalent */
}

.progress {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.5rem;
  border-radius: 0.375rem;
  font-weight: 600;
}

.progress.positive {
  background-color: #ecfdf5;
  /* Tailwind's green-50 equivalent */
}

.progress.negative {
  background-color: #fef2f2;
  /* Tailwind's red-50 equivalent */
}
</style>

<script setup>
import { ref } from 'vue';

const isDomestic = ref(false);
const listQuery = ref('');

const searchQuery = ref('');

const searchStock = () => {
  if (searchQuery.value) {
    this.$router.push({ path: '/stock-info', query: { search: searchQuery.value } });
  }
};
</script>

<style scoped>
.carousel-content-overlay {
  position: relative;
  z-index: 10;
  color: black;
  text-align: center;
  width: 90%;
  max-width: 800px;
  padding: 2rem;
  height: 10vh;
}
</style>
