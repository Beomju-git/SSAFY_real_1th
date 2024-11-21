<template>
    <div class="detail-container">
      <h1 class="title">{{ detail.product_type }} 상세페이지</h1>
      <div class="detail-box">
        <p><strong>공시 시작일:</strong> {{ detail.dcls_strt_day }}</p>
        <p><strong>금융 회사명:</strong> {{ detail.kor_co_nm }}</p> 
        <p><strong>금융 상품명:</strong> {{ detail.fin_prdt_nm }}</p>
        <p><strong>가입 방법:</strong> {{ detail.join_way }}</p>
        
        <p><strong>상세 설명:</strong><span class="detailed-description" v-html="formatDetail(detail.etc_note)"></span></p>
        <div v-if="!isZzimed">
        <button @click.prevent="recommend()"> 찜</button>
        </div>
        <div v-else>
        <button @click.prevent="recommend()"> 찜 취소</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { useRoute } from 'vue-router';
  import { ref,computed } from 'vue';
  import { onBeforeMount } from 'vue';
  import axios from 'axios';
  import { useAuthStore } from '@/stores/auth';

  const authStore = useAuthStore()
  
  const route = useRoute();
  const fin_prdt_cd = ref(route.params.fin_prdt_cd);
  const detail = ref();

  let isZzimed = ref()
  const recommend = () => {
    axios({
        method: 'post',
        url: `http://127.0.0.1:8000/products/term_deposit/detail/${fin_prdt_cd.value}/recommend/`,
        headers:{
            Authorization: `Token ${authStore.token}`
        }   
    }).then((req) => {
        console.log(req.data)
        console.log(authStore.user?.id)
        if (req.data.zzimed_product.includes(authStore.user?.id) ) {
            console.log(111)
            isZzimed.value = true
        }else{
            console.log(222)
            isZzimed.value = false
             }
          
    })
  }

  
  onBeforeMount(() => {
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/products/term_deposit/detail/${route.params.fin_prdt_cd}/`
    })
    .then((response) => {
      detail.value = response.data;
      console.log(detail.value);
      
      if (detail.value.zzimed_product.includes(authStore.user?.id) ) {
            console.log(111)
            isZzimed.value = true
        }else{
            console.log(222)
            isZzimed.value = false
             }
          
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
  button {
  display: inline-block;
  padding: 12px 20px;
  font-size: 1rem;
  font-weight: 600;
  color: #ffffff;
  background-color: #1a73e8; /* 토스 스타일 블루 */
  border: none;
  border-radius: 8px;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
}

/* 호버 및 클릭 효과 */
button:hover {
  background-color: #1666c1; /* 약간 더 어두운 블루 */
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

button:active {
  background-color: #124a94;
  transform: translateY(0);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2);
}

/* 찜 취소 버튼 색상 */
button:focus {
  outline: none;
}

button:disabled {
  background-color: #cccccc;
  color: #666666;
  cursor: not-allowed;
}

/* 반응형 버튼 크기 조정 */
@media (max-width: 768px) {
  button {
    padding: 10px 16px;
    font-size: 0.9rem;
  }
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
  