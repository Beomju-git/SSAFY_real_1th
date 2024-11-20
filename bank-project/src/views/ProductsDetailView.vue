<template>
    <div class="detail-container">
      <h1 class="title">정기 예금 상세페이지</h1>
      <div class="detail-box">
        <p><strong>공시 시작일:</strong> {{ detail.dcls_strt_day }}</p>
        <p><strong>금융 회사명:</strong> {{ detail.kor_co_nm }}</p> 
        <p><strong>금융 상품명:</strong> {{ detail.fin_prdt_nm }}</p>
        <p><strong>가입 방법:</strong> {{ detail.join_way }}</p>
        <p><strong>상세 설명:</strong><span class="detailed-description" v-html="formatDetail(detail.etc_note)"></span></p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { useRoute } from 'vue-router';
  import { ref } from 'vue';
  import { onBeforeMount } from 'vue';
  import axios from 'axios';
  
  const route = useRoute();
  const fin_prdt_cd = ref(route.params.fin_prdt_cd);
  const detail = ref();
  
  onBeforeMount(() => {
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/products/term_deposit/detail/${route.params.fin_prdt_cd}/`
    })
    .then((response) => {
      detail.value = response.data;
      console.log(detail.value);
    });
  });
  
  // 상세 설명을 <p> 태그로 나누어 출력하는 함수
  const formatDetail = (text) => {
    return text.split('/').map(line => `<p>${line.trim()}</p>`).join('');
  };
  </script>
  
  <style scoped>
  /* 전체 컨테이너 스타일 */
  .detail-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f8f9fa;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  }
  
  .title {
    font-size: 2.5rem;
    font-weight: 600;
    text-align: center;
    margin-bottom: 30px;
    color: #1a73e8; /* 토스 색상에 가까운 블루 */
    text-transform: uppercase;
  }
  
  /* 상세 정보 박스 스타일 */
  .detail-box {
    background-color: #ffffff;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  
  .detail-box p {
    font-size: 1.1rem;
    color: #555;
    line-height: 1.6;
    margin: 10px 0;
  }
  
  .detail-box strong {
    font-weight: 600;
    color: #333;
  }
  
  /* 상세 설명 텍스트 스타일 */
  .detailed-description p {
    color: #333;
    margin-bottom: 10px;
    font-size: 1rem;
    white-space: pre-line; /* 줄바꿈 처리 */
  }
  
  /* 반응형 디자인 */
  @media (max-width: 768px) {
    .detail-container {
      padding: 15px;
    }
  
    .title {
      font-size: 2rem;
    }
  
    .detail-box p {
      font-size: 1rem;
    }
  }
  </style>
  