<template>
  <div class="bg-white text-gray-800">
    <main class="container mx-auto px-4 sm:px-6 py-8">
      <h1 class="text-3xl font-bold mb-4 text-center">AI 추천 금융상품</h1>
      <div class="bg-white p-6 rounded-lg shadow-lg overflow-x-auto">
        <table class="table-auto w-full">
          <thead>
            <tr>
              <th class="px-4 py-2 text-left">이름</th>
              <th class="px-4 py-2 text-left">종류</th>
              <th class="px-4 py-2 text-left">상품 소개</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="border px-4 py-2">삼성전자</td>
              <td class="border px-4 py-2">주식</td>
              <td class="border px-4 py-2"><a href="#">바로가기</a></td>
            </tr>
            <tr>
              <td class="border px-4 py-2">더큰플러스적금</td>
              <td class="border px-4 py-2">예/적금</td>
              <td class="border px-4 py-2"><a href="#">바로가기</a></td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'RecommendDeposit'
}
</script>

<style scoped>
/* 필요에 따라 스타일 추가 */
</style>
