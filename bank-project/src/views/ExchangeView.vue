<!-- Start of Selection -->
<!-- 환율 계산 페이지: Vue의 template은 HTML과 유사한 구조로, 사용자 인터페이스를 정의하는 데 사용됩니다. -->
<!-- 차이 : Vue는 가상DOM을 사용하여 조금더 동적으로 제어가 가능한 반면, 전통적인 html은 수동으로 DOM 요소를 조작해야 합니다. -->
<!-- 환율 계산: 이 컴포넌트는 환율 계산 기능을 제공하는 페이지입니다. -->

<!-- End of Selection -->
<template>
  <div class="exchange-view">
    <div class="card">
    </div>
    <ExchangeCalculator />
  </div>
</template>

<style>

</style>

<script>
import ExchangeCalculator from '../components/ExchangeCalculator.vue'

export default {
  name: 'ExchangeView',
  components: {
    ExchangeCalculator
  }
}
</script>