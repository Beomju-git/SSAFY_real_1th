<template>
  <div class="container">
    <div class="search-container">
      <div class="search-box">
        <input 
          type="text" 
          v-model="keyword" 
          placeholder="지역을 검색해보세요"
          @keyup.enter="searchPlaces"
        />
        <button @click="searchPlaces">검색</button>
      </div>
    </div>

    <div class="content-wrapper">
      <div class="map-container">
        <div id="map"></div>
        
        <div class="result-panel">
          <div class="result-list">
            <div 
              v-for="(place, index) in places" 
              :key="index"
              class="result-item"
              :class="{ active: selectedIndex === index }"
              @click="selectPlace(index)"
              @mouseover="displayInfowindow(index)"
              @mouseout="closeInfowindow"
            >
              <div class="marker-number">{{ index + 1 }}</div>
              <div class="place-info">
                <h3>{{ place.place_name }}</h3>
                <p>{{ place.road_address_name || place.address_name }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      map: null,
      ps: null,
      infowindow: null,
      keyword: "현충원역",
      places: [],
      markers: [],
      pagination: null,
      currentPage: 1,
      selectedIndex: null,
    };
  },
  computed: {
    paginationPages() {
      return this.pagination ? Array.from({ length: this.pagination.last }, (_, i) => i + 1) : [];
    },
  },
  mounted() {
    const kakao = window.kakao;
    const mapContainer = document.getElementById("map");
    const mapOption = {
      center: new kakao.maps.LatLng(37.566826, 126.9786567),
      level: 3,
    };

    this.map = new kakao.maps.Map(mapContainer, mapOption);
    this.ps = new kakao.maps.services.Places();
    this.infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });

    this.searchPlaces();
  },
  methods: {
    searchPlaces() {
      const kakao = window.kakao;

      if (!this.keyword.trim()) {
        alert("키워드를 입력해주세요!");
        return;
      }

      this.ps.keywordSearch(this.keyword + '은행', (data, status, pagination) => {
        if (status === kakao.maps.services.Status.OK) {
          this.places = data;
          this.pagination = pagination;
          this.displayMarkers();
        } else if (status === kakao.maps.services.Status.ZERO_RESULT) {
          alert("검색 결과가 존재하지 않습니다.");
        } else if (status === kakao.maps.services.Status.ERROR) {
          alert("검색 결과 중 오류가 발생했습니다.");
        }
      });
    },
    selectPlace(index) {
      this.selectedIndex = index;
      this.moveToLocation(index);
    },
    moveToLocation(index) {
      const kakao = window.kakao;

      // 클릭된 장소의 좌표 가져오기
      const position = new kakao.maps.LatLng(this.places[index].y, this.places[index].x);

      // 지도 중심을 해당 좌표로 이동
      this.map.setCenter(position);
      this.map.setLevel(3);
      // 선택된 마커에 인포윈도우 표시
      const content = `<div style="padding:5px;z-index:1;">${this.places[index].place_name}</div>`;
      this.infowindow.setContent(content);
      this.infowindow.open(this.map, this.markers[index]);
    },
    displayMarkers() {
      const kakao = window.kakao;
      this.clearMarkers();

      const bounds = new kakao.maps.LatLngBounds();
      this.places.forEach((place, index) => {
        const position = new kakao.maps.LatLng(place.y, place.x);
        const marker = this.createMarker(position, index);
        this.markers.push(marker);
        bounds.extend(position);
      });

      this.map.setBounds(bounds);
    },
    createMarker(position, index) {
      const kakao = window.kakao;
      const imageSrc = "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png";
      const imageSize = new kakao.maps.Size(36, 37);
      const imgOptions = {
        spriteSize: new kakao.maps.Size(36, 691),
        spriteOrigin: new kakao.maps.Point(0, index * 46 + 10),
        offset: new kakao.maps.Point(13, 37),
      };
      const markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imgOptions);

      const marker = new kakao.maps.Marker({
        position,
        image: markerImage,
      });

      // 클릭 했을 때 마커에 창 띄우기
      kakao.maps.event.addListener(marker, "click", () => {
        this.displayInfowindow(index);
        this.moveToLocation(index);
      });

      kakao.maps.event.addListener(marker, "mouseover", () => {
        this.displayInfowindow(index);
      });

      // 마우스를 떼었을 때 인포윈도우 닫기
      kakao.maps.event.addListener(marker, "mouseout", () => {
        this.closeInfowindow();
      });

      marker.setMap(this.map);
      return marker;
    },
    displayInfowindow(index) {
      const kakao = window.kakao;
      const content = `<div style="padding:5px;z-index:1;">${index + 1}. ${this.places[index].place_name}</div>`;
      this.infowindow.setContent(content);
      this.infowindow.open(this.map, this.markers[index]);
    },
    closeInfowindow() {
      this.infowindow.close();
    },
    clearMarkers() {
      this.markers.forEach((marker) => marker.setMap(null));
      this.markers = [];
    },
    gotoPage(page) {
      this.pagination.gotoPage(page);
      this.currentPage = page;
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.search-container {
  margin-bottom: 16px;
}

.search-box {
  display: flex;
  gap: 8px;
  max-width: 400px;
}

.search-box input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #eee;
  border-radius: 8px;
  font-size: 15px;
  outline: none;
  background: #f9f9f9;
  transition: all 0.2s;
}

.search-box input:focus {
  background: white;
  border-color: #3182f6;
}

.search-box button {
  padding: 0 24px;
  background: #3182f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.search-box button:hover {
  background: #1c6def;
}

.content-wrapper {
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  overflow: hidden;
}

.map-container {
  position: relative;
  height: 600px;
  display: flex;
}

#map {
  flex: 1;
  height: 100%;
}

.result-panel {
  width: 320px;
  background: white;
  border-left: 1px solid #eee;
  overflow-y: auto;
}

.result-list {
  padding: 8px;
}

.result-item {
  display: flex;
  align-items: center;
  padding: 12px;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.2s;
}

.result-item:hover {
  background: #f8f9fa;
}

.result-item.active {
  background: #e7f1ff;
}

.marker-number {
  width: 24px;
  height: 24px;
  background: #3182f6;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
  margin-right: 12px;
}

.place-info {
  flex: 1;
  min-width: 0;
}

.place-info h3 {
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.place-info p {
  margin: 4px 0 0;
  font-size: 13px;
  color: #666;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.custom-marker {
  background: #3182f6;
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 12px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

@media (max-width: 768px) {
  .container {
    padding: 12px;
  }
  
  .map-container {
    height: 400px;
  }

  .result-panel {
    width: 280px;
  }
}
</style>
