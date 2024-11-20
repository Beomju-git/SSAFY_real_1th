<template>
  <div class="map_wrap">
    <div id="map" style="width: 100%; height: 100%; position: relative; overflow: hidden;"></div>
    <div id="menu_wrap" class="bg_white">
      <div class="option">
        <form @submit.prevent="searchPlaces">
          키워드:
          <input type="text" v-model="keyword" id="keyword" size="15" />
          <button type="submit">검색하기</button>
        </form>
      </div>
      <hr />
      <ul id="placesList">
        <li v-for="(place, index) in places" :key="index" class="item" @mouseover="displayInfowindow(index)" @mouseout="closeInfowindow" @click="moveToLocation(index)">
          <span :class="'markerbg marker_' + (index + 1)" :style="{ backgroundPosition: '0px -' + (index * 46) + 'px' }"></span>
          <div class="info">
            <h5>{{ place.place_name }}</h5>
            <span v-if="place.road_address_name">{{ place.road_address_name }}</span>
            <span class="jibun gray">{{ place.address_name }}</span>
            <span class="tel">{{ place.phone }}</span>
          </div>
        </li>
      </ul>
      <div id="pagination">
        <a v-for="page in paginationPages" :key="page" href="#" @click.prevent="gotoPage(page)" :class="{ on: page === currentPage }">
          {{ page }}
        </a>
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

      this.ps.keywordSearch(this.keyword +'은행', (data, status, pagination) => {
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
        this.moveToLocation(index)
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
      const content = `<div style="padding:5px;z-index:1;">${index+1}. ${this.places[index].place_name}</div>`;
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
.map_wrap {
  position: relative;
  width: 100%;
  height: 500px;
}
.map_wrap * {
  margin: 0;
  padding: 0;
  font-family: "Malgun Gothic", dotum, "돋움", sans-serif;
  font-size: 12px;
}
.map_wrap a,
.map_wrap a:hover,
.map_wrap a:active {
  color: #000;
  text-decoration: none;
}
#menu_wrap {
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  width: 250px;
  margin: 10px 0 30px 10px;
  padding: 5px;
  overflow-y: auto;
  background: rgba(255, 255, 255, 0.7);
  z-index: 1;
  font-size: 12px;
  border-radius: 10px;
}
#menu_wrap hr {
  display: block;
  height: 1px;
  border: 0;
  border-top: 2px solid #5f5f5f;
  margin: 3px 0;
}
#placesList li {
  list-style: none;
}
.item {
  position: relative;
  border-bottom: 1px solid #888;
  overflow: hidden;
  cursor: pointer;
  min-height: 65px;
}
.item span {
  display: block;
  margin-top: 4px;
}
.item h5,
.item .info {
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
}
.item .info {
  padding: 10px 0 10px 55px;
}
.item .info .gray {
  color: #8a8a8a;
}
.item .info .tel {
  color: #009900;
}
.item .markerbg {
  float: left;
  position: absolute;
  width: 36px;
  height: 37px;
  margin: 10px 0 0 10px;
  background: url("https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png") no-repeat;
}
#pagination a {
  display: inline-block;
  margin-right: 10px;
}
#pagination .on {
  font-weight: bold;
  cursor: default;
  color: #777;
}
</style>
