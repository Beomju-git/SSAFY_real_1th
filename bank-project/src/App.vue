<template>
  <div id="app">
    <!-- 네비게이션 바 컴퍼넌트 -->
    <NavigationBar />
    <!-- 라우팅 되는 페이지 주소에 따라서 다른 모습을 렌더링-->
    <router-view/>
    <!-- 푸터 컴퍼넌트 -->
    <Footer/>
  </div>
</template>

<script>
import NavigationBar from './components/NavigationBar.vue'
import Footer from './components/Footer.vue'

export default {
  name: 'App',
  components: {
    NavigationBar,
    Footer
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>