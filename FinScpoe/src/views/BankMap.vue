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
      min-height: 600px; /* Adjusted height for larger map */
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
        <div class="md:col-span-3 bg-gray-50 p-4 rounded-lg border border-gray-200">
          <h4 class="text-lg font-semibold text-gray-700 mb-3 text-center">은행 위치 및 경로</h4>
          <div ref="map1El" class="map-container-custom"></div>
          
          <div class="mt-4 flex justify-center space-x-4">
            <label class="inline-flex items-center">
              <input type="radio" class="form-radio text-teal-600" name="transport" value="car" v-model="selectedTransportType">
              <span class="ml-2 text-gray-700">자동차</span>
            </label>
          </div>

          <div id="routeInfo" class="mt-4 text-center text-gray-700 font-medium"></div>
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

const map1El = ref(null); // Only one map element needed
const routeInfoEl = ref(null); // To display route information

const globalData = ref({ mapInfo: [], bankInfo: [] });
const map1 = ref(null); // Only one map instance
const currentMarker = ref(null); // Marker for the selected bank
const currentPolyline = ref(null); // Polyline for the route
const currentLocationMarker = ref(null); // Marker for current location

const currentPosition = ref(null); // Make currentPosition reactive
const selectedTransportType = ref('car'); // Default to car
const destinationCoords = ref(null); // Store destination for re-requesting directions
const destinationName = ref(''); // Store destination name

function initializeMaps() {
  const defaultCenter = new kakao.maps.LatLng(37.566826, 126.9786567);
  map1.value = new kakao.maps.Map(map1El.value, { center: defaultCenter, level: 5 });

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        currentPosition.value = new kakao.maps.LatLng(lat, lon);

        // Add current location marker to map1
        currentLocationMarker.value = new kakao.maps.Marker({
          map: map1.value,
          position: currentPosition.value,
          title: '현재 위치',
          image: new kakao.maps.MarkerImage(
            'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png',
            new kakao.maps.Size(31, 35),
            { offset: new kakao.maps.Point(13, 34) }
          )
        });
        map1.value.setCenter(currentPosition.value); // Center map on current location
      },
      (error) => {
        console.error('Error getting current location:', error);
        alert('현재 위치를 가져올 수 없습니다. 기본 위치로 설정합니다.');
        currentPosition.value = new kakao.maps.LatLng(37.5012743, 127.039585); // Fallback
        currentLocationMarker.value = new kakao.maps.Marker({
          map: map1.value,
          position: currentPosition.value,
          title: '현재 위치 (기본값)',
          image: new kakao.maps.MarkerImage(
            'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png',
            new kakao.maps.Size(31, 35),
            { offset: new kakao.maps.Point(13, 34) }
          )
        });
        map1.value.setCenter(currentPosition.value); // Center map on fallback location
      }
    );
  } else {
    alert('이 브라우저에서는 Geolocation이 지원되지 않습니다. 기본 위치로 설정합니다.');
    currentPosition.value = new kakao.maps.LatLng(37.5012743, 127.039585); // Fallback
    currentLocationMarker.value = new kakao.maps.Marker({
      map: map1.value,
      position: currentPosition.value,
      title: '현재 위치 (기본값)',
      image: new kakao.maps.MarkerImage(
        'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png',
        new kakao.maps.Size(31, 35),
        { offset: new kakao.maps.Point(13, 34) }
      )
    });
    map1.value.setCenter(currentPosition.value); // Center map on fallback location
  }
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

      map1.value.setCenter(coords);
      map1.value.setLevel(4);
      currentMarker.value = new kakao.maps.Marker({ map: map1.value, position: coords });

      const infowindow = new kakao.maps.InfoWindow({
        content: `<div style="padding:5px;font-size:12px;min-width:150px;">${place.place_name}</div>`,
      });
      infowindow.open(map1.value, currentMarker.value);

      // Store destination for re-requesting directions
      destinationCoords.value = coords;
      destinationName.value = place.place_name;

      // Request directions immediately after finding the bank
      requestDirections(coords, place.place_name, selectedTransportType.value);
    } else {
      alert("검색 결과가 없습니다.");
      if (currentPolyline.value) currentPolyline.value.setMap(null); // Clear previous route
      if (routeInfoEl.value) routeInfoEl.value.innerText = ''; // Clear route info
      destinationCoords.value = null;
      destinationName.value = '';
    }
  });
}

// No need for reRequestDirections if only one transport type is supported
// function reRequestDirections() {
//   if (destinationCoords.value && destinationName.value) {
//     requestDirections(destinationCoords.value, destinationName.value, selectedTransportType.value);
//   }
// }

async function requestDirections(destinationLatLng, destinationName, transportType) {
  if (!currentPosition.value) {
    alert("현재 위치를 가져오는 중입니다. 잠시 후 다시 시도해주세요.");
    return;
  }

  const REST_API_KEY = import.meta.env.VITE_KAKAO_MOBILITY_REST_API_KEY;
  if (!REST_API_KEY) {
    alert("Kakao Mobility REST API 키가 .env 파일에 설정되지 않았습니다.");
    return;
  }

  const origin = `${currentPosition.value.getLng()},${currentPosition.value.getLat()}`;
  const destination = `${destinationLatLng.getLng()},${destinationLatLng.getLat()}`;
  let url = '';
  let headers = { Authorization: `KakaoAK ${REST_API_KEY}` };

  if (transportType === 'car') {
    url = `https://apis-navi.kakaomobility.com/v1/directions?origin=${origin}&destination=${destination}&priority=RECOMMEND`;
  } else {
    // Fallback for unsupported transport types, or if 'walking' was removed
    alert("지원하지 않는 이동 수단입니다. 자동차 경로를 표시합니다.");
    url = `https://apis-navi.kakaomobility.com/v1/directions?origin=${origin}&destination=${destination}&priority=RECOMMEND`;
    transportType = 'car'; // Ensure the display text is correct
  }

  console.log('Requesting directions with URL:', url);
  console.log('Origin:', origin, 'Destination:', destination, 'Transport Type:', transportType);

  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: headers,
    });
    const data = await response.json();
    console.log('Kakao Mobility API response:', JSON.stringify(data, null, 2));

    const routes = data.routes;
    if (!routes || routes.length === 0 || !routes[0].sections || routes[0].sections.length === 0) {
      alert("경로 정보를 찾을 수 없습니다. (API 응답에 경로 정보 없음)");
      console.error("No routes found in API response:", data);
      if (currentPolyline.value) currentPolyline.value.setMap(null);
      if (routeInfoEl.value) routeInfoEl.value.innerText = '';
      return;
    }

    const linePath = [];
    routes[0].sections.forEach(section => {
      section.roads.forEach(road => {
        for (let i = 0; i < road.vertexes.length; i += 2) {
          linePath.push(new kakao.maps.LatLng(road.vertexes[i + 1], road.vertexes[i]));
        }
      });
    });

    if (currentPolyline.value) currentPolyline.value.setMap(null);

    currentPolyline.value = new kakao.maps.Polyline({
      map: map1.value, // Draw on map1
      path: linePath,
      strokeWeight: 5,
      strokeColor: '#007aff',
      strokeOpacity: 0.9,
    });

    const bounds = new kakao.maps.LatLngBounds();
    bounds.extend(currentPosition.value);
    linePath.forEach(latlng => bounds.extend(latlng));
    map1.value.setBounds(bounds); // Adjust map1 bounds

    // Display estimated time
    const duration = routes[0].summary.duration; // Duration in seconds
    const minutes = Math.floor(duration / 60);
    const seconds = duration % 60;
    if (routeInfoEl.value) {
      routeInfoEl.value.innerText = `예상 소요 시간 (${transportType === 'car' ? '자동차' : '도보'}): ${minutes}분 ${seconds}초`;
    }
  } catch (error) {
    console.error("Error requesting directions:", error);
    alert("경로 요청 실패. 네트워크 또는 API 키를 확인하세요. 자세한 내용은 콘솔을 확인하세요.");
    if (currentPolyline.value) currentPolyline.value.setMap(null);
    if (routeInfoEl.value) routeInfoEl.value.innerText = '';
  }
}

onMounted(() => {
  initializeMaps()
  loadDropdownData()
})
</script>
