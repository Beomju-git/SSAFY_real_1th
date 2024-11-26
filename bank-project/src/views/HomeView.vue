<template>
  <div class="home">
    <!-- Hero 섹션 -->
    <section class="hero">
      <div class="container">
        <div class="hero-content">
          <h1 class="hero-title">금융의 미래를<br />함께 만들어가요</h1>
          <p class="hero-description">
            주욱주욱과 함께 스마트한 금융생활을 시작하세요.<br />
            실시간 환율부터 맞춤형 금융상품까지 한번에 확인하세요.
          </p>
          <button class="btn btn-primary btn-lg" @click="handleGetStarted">상품 추천 받기</button>
        </div>
        <div class="hero-image d-none d-lg-block">
          <!-- 이미지 플레이스홀더 -->
        </div>
      </div>
    </section>

    <!-- 서비스 섹션 -->
    <section class="services a">
      <div class="container">
        <h2 class="section-title">주요 서비스</h2>
        <div class="service-grid">
          <div
            v-for="service in services"
            :key="service.id"
            class="service-card"

          >
          <div v-if="service.title === '환율 계산'">
            <RouterLink :to="{name:'exchange'}">
              <div class="service-content">
              <div class="service-icon">
                <i :class="service.icon"></i>
              </div>
              <h3>{{ service.title }}</h3>
              <p>{{ service.description }}</p>
            </div>
            </RouterLink>
          </div>
          <div v-else-if="service.title === '주변 은행찾기'">
            <RouterLink :to="{name:'nearby-banks'}">
              <div class="service-content">
              <div class="service-icon">
                <i :class="service.icon"></i>
              </div>
              <h3>{{ service.title }}</h3>
              <p>{{ service.description }}</p>
            </div>
            </RouterLink>
          </div>
          <div v-else-if="service.title === '커뮤니티'">
            <RouterLink :to="{name:'articles'}">
              <div class="service-content">
              <div class="service-icon">
                <i :class="service.icon"></i>
              </div>
              <h3>{{ service.title }}</h3>
              <p>{{ service.description }}</p>
            </div>
            </RouterLink>
          </div>
          <div v-else-if="service.title === '상품 정보'">
            <RouterLink :to="{name:'products'}">
              <div class="service-content">
              <div class="service-icon">
                <i :class="service.icon"></i>
              </div>
              <h3>{{ service.title }}</h3>
              <p>{{ service.description }}</p>
            </div>
            </RouterLink>
          </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { RouterLink } from "vue-router";

const router = useRouter();

// 서비스 목록
const services = ref([
  {
    id: 1,
    icon: "fas fa-calculator",
    title: "환율 계산",
    description: "실시간 환율 정보와 함께 정확한 환전 금액을 계산해보세요.",
  },
  {
    id: 2,
    icon: "fas fa-map-marker-alt",
    title: "주변 은행찾기",
    description: "가까운 은행과 ATM 위치를 쉽게 찾아보세요.",
  },
  {
    id: 3,
    icon: "fas fa-comments",
    title: "커뮤니티",
    description: "다양한 금융 정보와 경험을 공유하세요.",
  },
  {
    id: 4,
    icon: "fas fa-chart-line",
    title: "상품 정보",
    description: "나에게 맞는 최적의 금융상품을 추천받으세요.",
  },
]);

// 시작하기 버튼 클릭 시 환율 페이지로 이동
const handleGetStarted = () => {
  router.push("/product-recommendation");
};

// 서비스 카드 클릭 시 해당 서비스 페이지로 이동
const navigateToService = (serviceId) => {
  router.push(`/service/${serviceId}`);
};
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  width: 100%;
  min-height: 100vh;
}

/* 공통 섹션 스타일 */
section {
  width: 100%;
  padding: 3rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

/* Hero 섹션 */
.hero {
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(147, 197, 253, 0.1) 100%);
  display: flex;
  align-items: center;
  text-align: center;
  padding: 4rem 0;
}

.hero-content {
  max-width: 600px;
  margin: 0 auto;
}

.hero-title {
  font-size: 2.5rem;
  font-weight: 700;
  line-height: 1.3;
  margin-bottom: 1.5rem;
}

.hero-description {
  font-size: 1rem;
  color: #4b5563;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.btn-primary {
  background-color: #2563eb;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 500;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.btn-primary:hover {
  transform: translateY(-3px);
}

/* 서비스 섹션 */
.service-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
}

.service-card {
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
}

.service-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.service-icon {
  width: 60px;
  height: 60px;
  margin: 0 auto 1rem;
  background: rgba(37, 99, 235, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.service-icon i {
  font-size: 1.5rem;
  color: #2563eb;
}

/* 섹션 타이틀 */
.section-title {
  text-align: center;
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 2rem;
  color: #111827;
}

/* 반응형 스타일 */
@media (min-width: 768px) {
  .hero-content {
    text-align: left;
  }
  .hero-title {
    font-size: 3rem;
  }
}

@media (min-width: 1024px) {
  .hero {
    text-align: left;
    padding: 5rem 0;
  }
  .container {
    padding: 0 2rem;
  }
}
a {
  text-decoration: none;
  color: inherit;
}

a:hover {
  text-decoration: none;
}
</style>
