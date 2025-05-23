    <style scoped>
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

    /* Navbar styles from other pages */
    .menu-bar a {
      padding: 0.5rem 0.75rem;
      border-radius: 0.375rem;
      transition: background-color 0.2s ease-in-out, color 0.2s ease-in-out;
      white-space: nowrap;
    }

    .menu-bar a:hover {
      background-color: #f0fdfa;
      /* teal-50 */
      color: #0d9488;
      /* teal-600 */
    }

    .menu-bar a.active {
      color: #0d9488;
      /* teal-600 */
      font-weight: 600;
      /* semibold */
      border-bottom: 2px solid #0d9488;
      padding-bottom: calc(0.5rem - 2px);
    }

    /* Form element styling consistent with other pages */
    .form-label {
      display: block;
      margin-bottom: 0.25rem;
      /* mb-1 */
      font-size: 0.875rem;
      /* text-sm */
      font-weight: 500;
      /* font-medium */
      color: #374151;
      /* text-gray-700 */
    }

    .form-select {
      width: 100%;
      padding: 0.625rem 0.75rem;
      /* Adjusted padding for select */
      border: 1px solid #d1d5db;
      /* gray-300 */
      border-radius: 0.375rem;
      /* rounded-md */
      background-color: white;
      box-shadow: inset 0 1px 2px 0 rgba(0, 0, 0, 0.05);
      transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
      -webkit-appearance: none;
      /* For custom arrow, if added */
      -moz-appearance: none;
      appearance: none;
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20' fill='currentColor'%3E%3Cpath fill-rule='evenodd' d='M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z' clip-rule='evenodd'/%3E%3C/svg%3E");
      background-repeat: no-repeat;
      background-position: right 0.5rem center;
      background-size: 1.5em 1.5em;
      padding-right: 2.5rem;
      /* Make space for arrow */
    }

    .form-select:focus {
      outline: none;
      border-color: #0d9488;
      /* teal-600 */
      box-shadow: 0 0 0 0.2rem rgba(13, 148, 136, 0.25);
      /* teal-600 focus ring */
    }

    .map-container-custom {
      /* Renamed to avoid conflict with potential Tailwind class */
      min-height: 400px;
      /* Adjusted height */
      width: 100%;
      border: 1px solid #e5e7eb;
      /* gray-200 */
      border-radius: 0.5rem;
      /* rounded-lg */
    }
  </style>

<template>
  <navbar />
  <main class="flex-grow container mx-auto px-4 sm:px-6 py-8 md:py-12">
    <div class="bg-white p-6 md:p-8 rounded-xl shadow-xl border border-gray-200">
      <h1 class="text-2xl md:text-3xl font-bold text-teal-700 mb-8 text-center">은행 지도 검색</h1>

      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <!-- 검색 조건 -->
        <div class="md:col-span-1 bg-gray-50 p-6 rounded-lg border border-gray-200">
          <h2 class="text-xl font-semibold text-gray-800 mb-4">검색 조건</h2>
          <div class="space-y-4">
            <div>
              <label class="form-label">광역시 / 도</label>
              <select class="form-select" v-model="selectedRegion" @change="updateCities">
                <option v-for="region in globalData.mapInfo" :key="region.name" :value="region.name">
                  {{ region.name }}
                </option>
              </select>
            </div>
            <div>
              <label class="form-label">시 / 군 / 구</label>
              <select class="form-select" v-model="selectedCity">
                <option v-for="city in cityList" :key="city" :value="city">
                  {{ city }}
                </option>
              </select>
            </div>
            <div>
              <label class="form-label">은행</label>
              <select class="form-select" v-model="selectedBank">
                <option v-for="bank in globalData.bankInfo" :key="bank" :value="bank">
                  {{ bank }}
                </option>
              </select>
            </div>
            <button @click="searchBank" class="w-full bg-teal-600 text-white py-2.5 px-4 rounded-lg hover:bg-teal-700">
              찾기
            </button>
          </div>
        </div>

        <!-- 지도 영역 -->
        <div class="md:col-span-3 grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
            <h4 class="text-lg font-semibold text-gray-700 mb-3 text-center">선택 은행 위치</h4>
            <div ref="map1El" class="map-container-custom"></div>
          </div>
          <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
            <h4 class="text-lg font-semibold text-gray-700 mb-3 text-center">현재 위치에서 경로</h4>
            <div ref="map2El" class="map-container-custom"></div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import res from '@/assets/data.json'
import navbar from '@/components/navbar.vue'

const selectedRegion = ref('')
const selectedCity = ref('')
const selectedBank = ref('')
const cityList = ref([])

const map1El = ref(null)
const map2El = ref(null)

const globalData = ref({ mapInfo: [], bankInfo: [] })
const map1 = ref(null)
const map2 = ref(null)
const currentMarker = ref(null)
const currentPolyline = ref(null)

const currentPosition = new kakao.maps.LatLng(37.5012743, 127.039585)

function initializeMaps() {
  const defaultCenter = new kakao.maps.LatLng(37.566826, 126.9786567)
  map1.value = new kakao.maps.Map(map1El.value, { center: defaultCenter, level: 5 })
  map2.value = new kakao.maps.Map(map2El.value, { center: defaultCenter, level: 5 })

  new kakao.maps.Marker({
    map: map2.value,
    position: currentPosition,
    title: '현재 위치 (예시)',
  })
}

function updateCities() {
  const region = globalData.value.mapInfo.find(r => r.name === selectedRegion.value)
  cityList.value = region ? region.countries : []
  selectedCity.value = cityList.value[0] || ''
}

async function loadDropdownData() {
  try {
    const data = res
    globalData.value = data

    if (data.mapInfo.length > 0) {
      selectedRegion.value = data.mapInfo[0].name
      updateCities()
    }
    selectedBank.value = data.bankInfo[0] || ''
  } catch (err) {
    alert("데이터 로드 실패: data.json을 확인하세요.")
  }
}

function searchBank() {
  const places = new kakao.maps.services.Places()
  const keyword = `${selectedRegion.value} ${selectedCity.value} ${selectedBank.value}`

  places.keywordSearch(keyword, (result, status) => {
    if (status === kakao.maps.services.Status.OK && result.length > 0) {
      const place = result[0]
      const coords = new kakao.maps.LatLng(place.y, place.x)

      if (currentMarker.value) {
        currentMarker.value.setMap(null)
      }

      map1.value.setCenter(coords)
      map1.value.setLevel(4)
      currentMarker.value = new kakao.maps.Marker({ map: map1.value, position: coords })

      const infowindow = new kakao.maps.InfoWindow({
        content: `<div style="padding:5px;font-size:12px;min-width:150px;">${place.place_name}</div>`,
      })
      infowindow.open(map1.value, currentMarker.value)

      kakao.maps.event.addListener(currentMarker.value, 'click', () => {
        requestDirections(coords, place.place_name)
      })
    } else {
      alert("검색 결과가 없습니다.")
    }
  })
}

function requestDirections(destinationLatLng, destinationName) {
  const REST_API_KEY = 'YOUR_KAKAO_MOBILITY_REST_API_KEY'
  if (!REST_API_KEY || REST_API_KEY === 'YOUR_KAKAO_MOBILITY_REST_API_KEY') {
    alert("REST API 키가 필요합니다.")
    return
  }

  const origin = `${currentPosition.getLng()},${currentPosition.getLat()}`
  const destination = `${destinationLatLng.getLng()},${destinationLatLng.getLat()}`
  const url = `https://apis-navi.kakaomobility.com/v1/directions?origin=${origin}&destination=${destination}&priority=RECOMMEND`

  fetch(url, {
    method: 'GET',
    headers: { Authorization: `KakaoAK ${REST_API_KEY}` },
  })
    .then(res => res.json())
    .then(data => {
      const roads = data.routes?.[0]?.sections?.[0]?.roads
      if (!roads) {
        alert("경로 정보를 찾을 수 없습니다.")
        return
      }

      const linePath = []
      roads.forEach(road => {
        for (let i = 0; i < road.vertexes.length; i += 2) {
          linePath.push(new kakao.maps.LatLng(road.vertexes[i + 1], road.vertexes[i]))
        }
      })

      if (currentPolyline.value) currentPolyline.value.setMap(null)

      currentPolyline.value = new kakao.maps.Polyline({
        map: map2.value,
        path: linePath,
        strokeWeight: 5,
        strokeColor: '#007aff',
        strokeOpacity: 0.9,
      })

      const bounds = new kakao.maps.LatLngBounds()
      bounds.extend(currentPosition)
      linePath.forEach(latlng => bounds.extend(latlng))
      map2.value.setBounds(bounds)
    })
    .catch(() => {
      alert("경로 요청 실패. 네트워크 또는 API 키를 확인하세요.")
    })
}

onMounted(() => {
  initializeMaps()
  loadDropdownData()
})
</script>