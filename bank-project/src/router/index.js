// router란?
// 페이지 이동을 관리하는 라이브러리
/* 
라우팅(routing)이란?
- 라우팅(Routing)은 애플리케이션에서 사용자 요청(URL)에 따라 특정 페이지나 컴포넌트로 연결하는 경로 지정의 과정을 말합니다. 


네비게이션이란, 
-사용자가 한 페이지에서 다른 페이지로 이동하는 것을 의미합니다. 
- 예를 들어, 은행 홈페이지에서 메인 페이지 → 로그인 페이지 → 계좌 상세 페이지로 이동하는 과정이 모두 네비게이션입니다.


정적 라우팅이란?
- 라우팅 경로가 고정되어있는 것을 의미합니다.
- 예를 들어, 메인 페이지 → 로그인 페이지 → 계좌 상세 페이지는 정적 라우팅입니다.

동적 라우팅이란?
- 라우팅 경로가 동적으로 변경되는 것을 의미합니다.
- 예를 들어, 메인 페이지 → 로그인 페이지 → 계좌 상세 페이지는 동적 라우팅입니다.

여기는 정적 라우팅을 사용하였습니다.
reason : 라우팅 경로가 고정되어있기 때문입니다.
*/

import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      // 홈 페이지
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      // 환율 계산 페이지
      path: '/exchange',
      name: 'exchange',
      // 환율 계산 페이지 컴포넌트(ExchangeView.vue) 불러오기
      component: () => import('../views/ExchangeView.vue'),
    },
    {
      // 근처 은행 페이지
      path: '/nearby-banks',
      name: 'nearby-banks',
      component: () => import('../views/NearbyBanksView.vue'),
    },
    {
      path: '/articles',
      name: 'articles',
      component: () => import('../views/ArticleView.vue'),
    },
    {
      path: '/articles/:articleId',
      name: 'article-detail',
      component: () => import('../views/ArticleDetailView.vue'),
      props: true,
    },
    {
      // 금융 상품 추천 페이지
      path: '/product-recommendation',
      name: 'product-recommendation',
      // 금융 상품 추천 페이지 컴포넌트(ProductRecommendationView.vue) 불러오기
      // 참고 Vue 파일의 명명 규칙 : 파스칼 케이스
      component: () => import('../views/ProductRecommendationsView.vue'),
    },
    {
      path: '/products',
      name: 'products',
      component: () => import('../views/ProductsView.vue')
    },
    {
      path: '/products/term_deposit/detail/:fin_prdt_cd',
      name: 'products_detail',
      component: () => import('../views/ProductsDetailView.vue')
    },
  ],
})

export default router
