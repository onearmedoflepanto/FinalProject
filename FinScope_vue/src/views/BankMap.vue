<style scoped>
/* Removed scoped body, #app, main styles */

.form-input-custom {
  @apply w-full px-4 py-2.5 border border-gray-600 bg-gray-700 text-gray-100 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-light focus:border-primary-light transition duration-150 ease-in-out;
  font-size: 0.95rem;
}

.form-select-custom {
  @apply w-full pl-4 pr-10 py-2.5 border border-gray-600 bg-gray-700 text-gray-100 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-light focus:border-primary-light transition duration-150 ease-in-out;
  font-size: 0.95rem;
  appearance: none;
  /* Ensure the SVG is visible on dark backgrounds, consider using a white or light-colored SVG or filter: invert(1) */
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3E%3Cpath stroke='%239CA3AF' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3E%3C/svg%3E"); /* gray-400 stroke */
  background-repeat: no-repeat;
  background-position: right 0.7rem center;
  background-size: 1.25em 1.25em;
}
.form-select-custom option {
  background-color: #374151; /* bg-gray-700 for dropdown options */
  color: #F3F4F6; /* text-gray-100 */
}


.btn-primary {
  @apply w-full bg-primary hover:bg-primary-dark text-white font-semibold py-3 px-4 rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-primary-light focus:ring-offset-2 focus:ring-offset-gray-800 transition duration-150 ease-in-out;
}

.btn-secondary {
  @apply w-full bg-sky-600 hover:bg-sky-700 text-white font-semibold py-2.5 px-4 rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-sky-500 focus:ring-offset-2 focus:ring-offset-gray-800 transition duration-150 ease-in-out;
  font-size: 0.9rem;
}

.radio-label-custom {
  @apply flex items-center text-gray-300 hover:text-primary-light cursor-pointer;
}

.radio-custom {
  @apply appearance-none h-5 w-5 border-2 border-gray-500 rounded-full checked:bg-primary checked:border-primary-dark focus:outline-none focus:ring-2 focus:ring-primary-light focus:ring-offset-1 focus:ring-offset-gray-800 transition duration-150 ease-in-out mr-2;
}

.map-container-custom {
  min-height: 550px;
  width: 100%;
  border: 1px solid #374151; /* border-gray-700 */
  border-radius: 0.75rem; /* rounded-xl */
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); /* shadow-lg */
  /* Kakao map might need specific styling for its own elements if they don't inherit well */
}
</style>

<template>
  <main class="flex-grow container mx-auto px-4 sm:px-6 pb-2 md:pb-4 text-gray-100">
    <h1 class="text-3xl md:text-4xl font-bold text-primary-light mb-6 text-center tracking-tight">
      은행 지도 및 경로 검색
    </h1>
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
      <!-- Controls Panel -->
      <div class="lg:col-span-4 bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-xl">
        <!-- Start Location Settings -->
        <section class="mb-8">
          <h2 class="text-xl font-semibold text-gray-200 mb-5 border-b border-gray-700 pb-3">출발지 설정</h2>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-1.5">출발지 유형</label>
              <div class="flex items-center space-x-6 bg-gray-700 p-3 rounded-lg border border-gray-600">
                <label class="radio-label-custom">
                  <input type="radio" class="radio-custom" name="startLocationType" value="current"
                    v-model="startLocationType">
                  현재 위치
                </label>
                <label class="radio-label-custom">
                  <input type="radio" class="radio-custom" name="startLocationType" value="custom"
                    v-model="startLocationType">
                  직접 입력
                </label>
              </div>
            </div>
            <div v-if="startLocationType === 'custom'" class="space-y-3">
              <label class="block text-sm font-medium text-gray-300">출발 주소</label>
              <input type="text" class="form-input-custom" v-model="customStartAddress" placeholder="예: 서울특별시 강남구 테헤란로">
              <button @click="geocodeCustomStartAddress" class="btn-secondary">
                주소로 출발지 설정
              </button>
            </div>
          </div>
        </section>

        <!-- Destination Bank Search -->
        <section>
          <h2 class="text-xl font-semibold text-gray-200 mb-5 border-b border-gray-700 pb-3">도착 은행 검색</h2>
          <div class="space-y-5">
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-1.5">광역시 / 도</label>
              <select class="form-select-custom" v-model="selectedRegion" @change="updateCities">
                <option disabled value="" class="text-gray-400">선택하세요</option>
                <option v-for="region in globalData.mapInfo" :key="region.name" :value="region.name">
                  {{ region.name }}
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-1.5">시 / 군 / 구</label>
              <select class="form-select-custom" v-model="selectedCity">
                <option disabled value="" class="text-gray-400">선택하세요</option>
                <option v-for="city in cityList" :key="city" :value="city">
                  {{ city }}
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-1.5">은행</label>
              <select class="form-select-custom" v-model="selectedBank">
                <option disabled value="" class="text-gray-400">선택하세요</option>
                <option v-for="bank in globalData.bankInfo" :key="bank" :value="bank">
                  {{ bank }}
                </option>
              </select>
            </div>
            <button @click="searchBank" class="btn-primary !mt-6">
              은행 찾기 및 경로 검색
            </button>
          </div>
        </section>
      </div>

      <!-- Map Area -->
      <div class="lg:col-span-8 bg-gray-800 p-4 sm:p-6 rounded-xl border border-gray-700 shadow-xl">
        <h3 class="text-xl font-semibold text-gray-200 mb-4 text-center">지도 및 경로 정보</h3>
        <div ref="map1El" class="map-container-custom"></div>

        <div
          class="mt-6 flex flex-col sm:flex-row justify-center items-center space-y-3 sm:space-y-0 sm:space-x-6 bg-gray-700 p-3 rounded-lg border border-gray-600 shadow-sm">
          <label class="radio-label-custom">
            <input type="radio" class="radio-custom" name="transport" value="car" v-model="selectedTransportType"
              @change="handleTransportChange">
            자동차 경로
          </label>
          <!-- Add other transport types if needed in the future -->
        </div>

        <div ref="routeInfoEl" id="routeInfo"
          class="mt-5 text-center text-primary-light font-semibold text-lg bg-gray-700 p-3 rounded-md">
          경로 정보를 보려면 은행을 검색하세요.
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import res from '@/assets/data.json'
// import NavigationBar from '@/components/NavigationBar.vue' // Assuming NavigationBar is globally registered or not used here

const selectedRegion = ref('')
const selectedCity = ref('')
const selectedBank = ref('')
const cityList = ref([])

const map1El = ref(null);
const routeInfoEl = ref(null);

const globalData = ref({ mapInfo: [], bankInfo: [] });
const map1 = ref(null);
const destinationBankMarker = ref(null); // Renamed from currentMarker for clarity
const routePolyline = ref(null); // Renamed from currentPolyline
const currentLocationMarker = ref(null);
const customStartMarker = ref(null);

const currentPosition = ref(null); // GPS current position
const customStartCoords = ref(null);
const customStartAddress = ref('');
const startLocationType = ref('current'); // 'current' or 'custom'

const selectedTransportType = ref('car');
const destinationCoords = ref(null);
const destinationName = ref('');

// Initialize Kakao Maps
function initializeKakaoMap() {
  const defaultCenter = new window.kakao.maps.LatLng(37.566826, 126.9786567); // Seoul City Hall
  const mapOptions = {
    center: defaultCenter,
    level: 5,
  };
  map1.value = new window.kakao.maps.Map(map1El.value, mapOptions);

  // Relayout map on tiles loaded to prevent rendering issues
  window.kakao.maps.event.addListener(map1.value, 'tilesloaded', () => map1.value.relayout());

  // Attempt to get current location
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        currentPosition.value = new window.kakao.maps.LatLng(lat, lon);

        if (currentLocationMarker.value) currentLocationMarker.value.setMap(null);
        currentLocationMarker.value = new window.kakao.maps.Marker({
          map: map1.value,
          position: currentPosition.value,
          title: '현재 위치',
          image: new window.kakao.maps.MarkerImage(
            'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png',
            new window.kakao.maps.Size(31, 35), { offset: new window.kakao.maps.Point(13, 34) }
          )
        });
        if (startLocationType.value === 'current') {
          map1.value.setCenter(currentPosition.value);
        }
      },
      () => handleLocationError() // Error callback
    );
  } else {
    handleLocationError("Geolocation is not supported by this browser.");
  }
}

function handleLocationError(message = '현재 위치를 가져올 수 없습니다. 기본 위치로 설정합니다.') {
  alert(message);
  currentPosition.value = new window.kakao.maps.LatLng(37.5012743, 127.039585); // Gangnam as fallback
  if (currentLocationMarker.value) currentLocationMarker.value.setMap(null);
  currentLocationMarker.value = new window.kakao.maps.Marker({
    map: map1.value,
    position: currentPosition.value,
    title: '현재 위치 (기본값)',
    image: new window.kakao.maps.MarkerImage(
      'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png',
      new window.kakao.maps.Size(31, 35), { offset: new window.kakao.maps.Point(13, 34) }
    )
  });
  if (startLocationType.value === 'current') {
    map1.value.setCenter(currentPosition.value);
  }
}

// Geocode custom start address
function geocodeCustomStartAddress() {
  if (!customStartAddress.value) {
    alert('출발 주소를 입력해주세요.');
    return;
  }
  const geocoder = new window.kakao.maps.services.Geocoder();
  geocoder.addressSearch(customStartAddress.value, (result, status) => {
    if (status === window.kakao.maps.services.Status.OK) {
      const coords = new window.kakao.maps.LatLng(result[0].y, result[0].x);
      customStartCoords.value = coords;

      if (customStartMarker.value) customStartMarker.value.setMap(null);
      customStartMarker.value = new window.kakao.maps.Marker({
        // map: map1.value, // Set below
        position: coords,
        title: `설정된 출발지: ${customStartAddress.value}`,
        image: new window.kakao.maps.MarkerImage( // Using red marker for now to ensure it's not a color-specific CDN issue
          'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png',
          new window.kakao.maps.Size(31, 35), { offset: new window.kakao.maps.Point(13, 34) }
        ),
        zIndex: 10 // Ensure custom start marker is on top if coordinates overlap initially
      });
      customStartMarker.value.setMap(map1.value); // Explicitly set map for the marker
      map1.value.setCenter(coords);

      // Hide current location marker if custom start is set
      if (currentLocationMarker.value) {
        currentLocationMarker.value.setMap(null);
      }

      // alert('출발지가 설정되었습니다.'); // Removed alert
      if (destinationCoords.value) {
        requestDirections(destinationCoords.value, destinationName.value, selectedTransportType.value);
      }
    } else {
      alert(`주소 검색 실패: ${status}. 정확한 주소를 입력해주세요.`);
      customStartCoords.value = null;
    }
  });
}

// Update city list based on selected region
function updateCities() {
  const region = globalData.value.mapInfo.find(r => r.name === selectedRegion.value);
  cityList.value = region ? region.countries : [];
  selectedCity.value = cityList.value.length > 0 ? cityList.value[0] : '';
}

// Load dropdown data from JSON
async function loadDropdownData() {
  try {
    globalData.value = res; // Assuming res is already imported JSON data
    if (globalData.value.mapInfo.length > 0) {
      selectedRegion.value = globalData.value.mapInfo[0].name;
      updateCities();
    }
    if (globalData.value.bankInfo.length > 0) {
      selectedBank.value = globalData.value.bankInfo[0];
    }
  } catch (error) {
    console.error("Error loading dropdown data:", error);
    alert("은행 및 지역 정보를 불러오는데 실패했습니다.");
  }
}

// Search for the bank and display it on the map
function searchBank() {
  if (!selectedRegion.value || !selectedCity.value || !selectedBank.value) {
    alert("모든 검색 조건을 선택해주세요.");
    return;
  }
  const places = new window.kakao.maps.services.Places();
  const keyword = `${selectedRegion.value} ${selectedCity.value} ${selectedBank.value}`;

  places.keywordSearch(keyword, (result, status) => {
    if (status === window.kakao.maps.services.Status.OK && result.length > 0) {
      const place = result[0];
      const coords = new window.kakao.maps.LatLng(place.y, place.x);

      if (destinationBankMarker.value) destinationBankMarker.value.setMap(null);
      destinationBankMarker.value = new window.kakao.maps.Marker({ map: map1.value, position: coords });

      map1.value.setCenter(coords);
      map1.value.setLevel(4);

      const infowindow = new window.kakao.maps.InfoWindow({
        content: `<div style="padding:8px;font-size:0.85rem;min-width:180px;text-align:center;font-weight:bold;">${place.place_name}</div>`,
      });
      infowindow.open(map1.value, destinationBankMarker.value);

      destinationCoords.value = coords;
      destinationName.value = place.place_name;
      requestDirections(coords, place.place_name, selectedTransportType.value);
    } else {
      alert("검색된 은행이 없습니다. 다른 조건을 시도해보세요.");
      if (routePolyline.value) routePolyline.value.setMap(null);
      if (routeInfoEl.value) routeInfoEl.value.innerText = '경로 정보를 보려면 은행을 검색하세요.';
      destinationCoords.value = null;
      destinationName.value = '';
    }
  });
}

// Request directions from Kakao Mobility API
async function requestDirections(destLatLng, destName, transportType) {
  let startCoords;
  if (startLocationType.value === 'custom') {
    if (!customStartCoords.value) {
      alert("직접 입력한 출발지가 설정되지 않았습니다. 주소로 출발지를 먼저 설정해주세요.");
      return;
    }
    startCoords = customStartCoords.value;
  } else {
    if (!currentPosition.value) {
      alert("현재 위치를 가져오는 중입니다. 잠시 후 다시 시도해주세요.");
      return;
    }
    startCoords = currentPosition.value;
  }

  const REST_API_KEY = import.meta.env.VITE_KAKAO_MOBILITY_REST_API_KEY;
  if (!REST_API_KEY) {
    alert("Kakao Mobility API 키가 .env 파일에 설정되지 않았습니다. (VITE_KAKAO_MOBILITY_REST_API_KEY)");
    return;
  }

  const origin = `${startCoords.getLng()},${startCoords.getLat()}`;
  const destination = `${destLatLng.getLng()},${destLatLng.getLat()}`;
  const url = `https://apis-navi.kakaomobility.com/v1/directions?origin=${origin}&destination=${destination}&priority=RECOMMEND&car_fuel=GASOLINE`; // Assuming car for now

  try {
    const response = await fetch(url, { headers: { Authorization: `KakaoAK ${REST_API_KEY}` } });
    const data = await response.json();

    if (!response.ok || !data.routes || data.routes.length === 0) {
      console.error("Kakao Mobility API Error:", data);
      alert(`경로 정보를 찾을 수 없습니다. (API 응답: ${data.msg || '오류 발생'})`);
      if (routePolyline.value) routePolyline.value.setMap(null);
      if (routeInfoEl.value) routeInfoEl.value.innerText = '경로를 찾을 수 없습니다.';
      return;
    }

    const route = data.routes[0];
    const linePath = [];
    route.sections.forEach(section => {
      section.roads.forEach(road => {
        for (let i = 0; i < road.vertexes.length; i += 2) {
          linePath.push(new window.kakao.maps.LatLng(road.vertexes[i + 1], road.vertexes[i]));
        }
      });
    });

    if (routePolyline.value) routePolyline.value.setMap(null);
    routePolyline.value = new window.kakao.maps.Polyline({
      map: map1.value,
      path: linePath,
      strokeWeight: 6,
      strokeColor: '#0891b2', // cyan-600
      strokeOpacity: 0.85,
    });

    const bounds = new window.kakao.maps.LatLngBounds();
    bounds.extend(startCoords);
    linePath.forEach(latlng => bounds.extend(latlng));
    map1.value.setBounds(bounds);

    const duration = route.summary.duration; // seconds
    const minutes = Math.floor(duration / 60);
    const seconds = duration % 60;
    if (routeInfoEl.value) {
      routeInfoEl.value.innerText = `예상 소요 시간 (자동차): ${minutes}분 ${seconds}초 (목적지: ${destName})`;
    }

  } catch (error) {
    console.error("Error requesting directions:", error);
    alert("경로 요청 중 오류가 발생했습니다. 네트워크 연결 또는 API 키를 확인하세요.");
    if (routePolyline.value) routePolyline.value.setMap(null);
    if (routeInfoEl.value) routeInfoEl.value.innerText = '경로 요청 중 오류 발생.';
  }
}

// Handle transport type change (if more types are added later)
function handleTransportChange() {
  if (destinationCoords.value && destinationName.value) {
    requestDirections(destinationCoords.value, destinationName.value, selectedTransportType.value);
  }
}

// Watch for changes in startLocationType to update map center or clear custom start
watch(startLocationType, (newType) => {
  if (newType === 'current' && currentPosition.value) {
    map1.value.setCenter(currentPosition.value);
    if (customStartMarker.value) {
      customStartMarker.value.setMap(null); // Hide custom start marker
    }
    if (currentLocationMarker.value) {
      currentLocationMarker.value.setMap(map1.value); // Show current location marker
    }
    customStartCoords.value = null;
    // customStartAddress.value = '';
  } else if (newType === 'custom') {
    if (customStartCoords.value) {
      map1.value.setCenter(customStartCoords.value);
      if (customStartMarker.value) {
        customStartMarker.value.setMap(map1.value); // Ensure custom start marker is visible
      }
      if (currentLocationMarker.value) {
        currentLocationMarker.value.setMap(null); // Hide current location marker
      }
    } else {
      // If switching to custom but no custom address is set yet, prompt or show current location
      if (currentLocationMarker.value) currentLocationMarker.value.setMap(map1.value);
      if (currentPosition.value) map1.value.setCenter(currentPosition.value);
    }
  }

  // If a route is displayed, re-calculate
  if (destinationCoords.value && routePolyline.value && map1.value) { // Added map1.value check
    requestDirections(destinationCoords.value, destinationName.value, selectedTransportType.value);
  }
});


// Kakao Maps SDK loader
function loadKakaoSdk() {
  return new Promise((resolve, reject) => {
    if (window.kakao && window.kakao.maps) {
      resolve(); // Already loaded
      return;
    }
    const script = document.createElement('script');
    const KAKAO_JS_KEY = import.meta.env.VITE_KAKAO_JAVASCRIPT_KEY;
    if (!KAKAO_JS_KEY) {
      alert("Kakao JavaScript API 키가 .env 파일에 설정되지 않았습니다. (VITE_KAKAO_JAVASCRIPT_KEY)");
      reject(new Error("Kakao JavaScript API key is missing."));
      return;
    }
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${KAKAO_JS_KEY}&libraries=services,drawing&autoload=false`;
    script.onload = () => window.kakao.maps.load(resolve);
    script.onerror = reject;
    document.head.appendChild(script);
  });
}

onMounted(async () => {
  try {
    await loadKakaoSdk();
    console.log('Kakao Maps SDK loaded successfully.');
    initializeKakaoMap();
    loadDropdownData();
  } catch (error) {
    console.error('Failed to load Kakao Maps SDK:', error);
    alert('지도 SDK를 불러오는데 실패했습니다. 페이지를 새로고침하거나 관리자에게 문의하세요.');
  }
});
</script>
