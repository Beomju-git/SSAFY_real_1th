<template>
  <KakaoMap :lat="coordinate.lat" :lng="coordinate.lng" :draggable="true" ref="kakaoMap">
    <div v-for="location in locations" :key="location.id">
      <KakaoMapMarker :lat="location.y" :lng="location.x"
      @mouseOverKakaoMapMarker="hideInfoWindow(location)"
      ></KakaoMapMarker>
    </div>
  </KakaoMap>

  <!-- 검색창 영역 -->
  <div class="search-container">
    <input
      v-model="keyword"
      @keyup.enter="searchPlaces"
      placeholder="장소를 검색하세요"
      class="search-input"
    />
    <button @click="searchPlaces" class="search-button">검색</button>
  </div> 
</template>
<script setup>
import { KakaoMap, KakaoMapMarker } from 'vue3-kakao-maps';
import { ref } from 'vue';

const keyword = ref('');
const coordinate = ref({
  lat: 36.3547,
  lng: 127.3347
});
const locations = ref([]);

const searchPlaces = () => {
  if (!keyword.value.trim()) {
    alert('검색어를 입력해주세요');
    return;
  }

  const ps = new kakao.maps.services.Places();
  
  // Perform a keyword search
  ps.keywordSearch(keyword.value, (data, status) => {
    if (status === kakao.maps.services.Status.OK) {
      // Update locations with search results
      locations.value = data;

      // Set map center to the first result's coordinates
      coordinate.value.lat = parseFloat(data[0].y);
      coordinate.value.lng = parseFloat(data[0].x);

      // Optionally, adjust map bounds to fit all markers
      const bounds = new kakao.maps.LatLngBounds();
      data.forEach(place => {
        bounds.extend(new kakao.maps.LatLng(place.y, place.x));
      });
      
      // Access the map instance and adjust its bounds
      const mapInstance = $refs.kakaoMap.map;
      mapInstance.setBounds(bounds);
    } else {
      alert('검색 결과가 없습니다.');
    }
  });
};
const showInfoWindow = (location) => {
  console.log(1)
};

const infoWindow = new kakao.maps.InfoWindow({
  content :'안녕'
})
// 마커에서 마우스를 뗐을 때 인포윈도우 닫기 함수 (마우스아웃 시)
const hideInfoWindow = (location) => {
  console.log(2)
  infoWindow
};

</script>

<style scoped>
.map-wrapper {
  position: relative;
  width: 100%;
  height: 100vh;
  padding: 20px;
}

.search-container {
  position: relative;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
  display: flex;
  gap: 10px;
  width: 400px;
  padding: 15px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.search-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.search-button {
  padding: 8px 16px;
  background: #2c3e50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.map-container {
  width: 100%;
  height: calc(100vh - 40px);
  border-radius: 8px;
  overflow: hidden;
}

.search-results {
  position: absolute;
  top: 80px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
  width: 400px;
  max-height: 400px;
  overflow-y: auto;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.result-item {
  padding: 12px 15px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
}

.result-item:hover {
  background: #f5f5f5;
}

.result-item h3 {
  margin: 0;
  font-size: 15px;
  color: #333;
}

.result-item p {
  margin: 5px 0 0;
  font-size: 13px;
  color: #666;
}
</style>
