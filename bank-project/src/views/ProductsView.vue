<template>
  <div class="products-view">
    <h1>금융 상품 정보</h1>
    <ProductList />
  </div>
</template>

<script setup>
import ProductList from '@/components/ProductList.vue'
import { onMounted } from 'vue'
import { useProductStore } from '@/stores/product'

const productStore = useProductStore()

onMounted(async () => {
  await productStore.fetchProducts()
})
</script>

<style scoped>
.products-view {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  color: #2c3e50;
  text-align: center;
  margin-bottom: 30px;
}
</style>