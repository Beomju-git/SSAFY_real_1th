<template>
  <div class="products-view">
    <h1 class="text-2xl font-bold mb-6">금융 상품 정보</h1>
    <div class="products-container">
      <ProductList />
    </div>
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
  width: 100%;
  min-height: 100vh;
  background-color: #f8f9fa;
}

.products-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

h1 {
  text-align: center;
  padding: 2rem 0;
  color: #2c3e50;
}
</style>