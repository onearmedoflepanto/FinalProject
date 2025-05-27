<template>
  <div class="container mx-auto h-screen flex justify-center items-center">
    <div class="carousel-content-overlay">
      <h1 class="text-4xl md:text-5xl font-bold mb-4">주식 검색</h1>
      <div class="flex">
        <input type="text" v-model="searchQuery" placeholder="종목명 또는 티커를 입력하세요"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" />
        <button @click="searchStock"
          class="ml-2 bg-teal-600 text-white px-8 py-2 rounded-lg hover:bg-teal-700 text-sm focus:outline-none focus:shadow-outline min-w-[100px]">
          검색
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: '',
    };
  },
  methods: {
    searchStock() {
      if (this.searchQuery) {
        this.$router.push({ path: '/stock-info', query: { search: this.searchQuery } });
      }
    },
  },
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
  top: -10%;
  height: 30vh;
}
</style>
