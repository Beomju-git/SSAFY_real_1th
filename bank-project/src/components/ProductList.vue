<template>
  <div class="w-full">
    <!-- 검색 필터 -->
    <div class="mb-4">
      <input
        v-model="searchTerm"
        type="text"
        placeholder="은행명 또는 상품명으로 검색..."
        class="w-full max-w-sm px-4 py-2 border rounded-lg"
      />
    </div>

    <!-- 데이터 테이블 -->
    <div class="overflow-x-auto border rounded-lg">
      <table class="w-full text-sm">
        <thead class="bg-gray-100">
          <tr>
            <!-- 각 컬럼 헤더 -->
            <th 
              v-for="column in columns" 
              :key="column.key"
              @click="handleSort(column.key)"
              class="px-4 py-3 border-b cursor-pointer hover:bg-gray-200"
              :class="column.align === 'right' ? 'text-right' : 'text-left'"
            >
              <div class="flex items-center" :class="column.align === 'right' ? 'justify-end' : ''">
                <span>{{ column.label }}</span>
                <div class="w-4 h-4 ml-1">
                  <template v-if="sortKey === column.key">
                    <!-- 정렬 방향 아이콘 -->
                    <svg v-if="sortOrder === 'asc'" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="18 15 12 9 6 15"></polyline>
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="6 9 12 15 18 9"></polyline>
                    </svg>
                  </template>
                </div>
              </div>
            </th>
          </tr>
        </thead>
        <tbody>
          <!-- 데이터 행 -->
          <tr 
            v-for="item in sortedAndFilteredData" 
            :key="`${item.fin_prdt_nm}-${item.dcls_strt_day}`"
            class="hover:bg-gray-50"
          >
          <RouterLink :to="{name:'products_detail', params:{fin_prdt_cd: item.fin_prdt_cd}}">
            <td class="px-4 py-3 border-b">{{ formatDate(item.dcls_strt_day) }}</td>
            <td class="px-4 py-3 border-b" >{{ item.kor_co_nm }}</td>
            <td class="px-4 py-3 border-b">{{ item.product_type }}</td>
            <td class="px-4 py-3 border-b">{{ item.fin_prdt_nm }}</td>
          </RouterLink>
            <td 
              v-for="period in ['6', '12', '24', '36']" 
              :key="period"
              class="px-4 py-3 text-right border-b"
            >
              {{ getInterestRate(item, period) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useProductStore } from '@/stores/product'
import { RouterLink } from 'vue-router';

const productStore = useProductStore()
const searchTerm = ref('')
const sortKey = ref('dcls_strt_day')
const sortOrder = ref('desc')

// 컬럼 정의
const columns = [
  { key: 'dcls_strt_day', label: '공시일자', align: 'left' },
  { key: 'kor_co_nm', label: '은행명', align: 'left' },
  { key: 'product_type', label: '상품유형', align: 'left' },
  { key: 'fin_prdt_nm', label: '상품명', align: 'left' },
  { key: '6', label: '6개월', align: 'right' },
  { key: '12', label: '12개월', align: 'right' },
  { key: '24', label: '24개월', align: 'right' },
  { key: '36', label: '36개월', align: 'right' }
]

// 정렬 처리 함수
const handleSort = (key) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortOrder.value = 'asc'
  }
}

// 날짜 포맷 함수
const formatDate = (dateStr) => {
  const year = dateStr.substring(0, 4)
  const month = dateStr.substring(4, 6)
  const day = dateStr.substring(6, 8)
  return `${year}-${month}-${day}`
}

// 금리 정보 가져오기
const getInterestRate = (item, period) => {
  const option = item.termdepositoptions_set.find(opt => opt.save_trm === Number(period))
  return option ? option.intr_rate + '%' : '-'
}

// 필터링 및 정렬된 데이터
const sortedAndFilteredData = computed(() => {
  let data = [...productStore.products]
  
  // 검색어 필터링
  if (searchTerm.value) {
    const term = searchTerm.value.toLowerCase()
    data = data.filter(item => 
      item.fin_prdt_nm.toLowerCase().includes(term) ||
      item.kor_co_nm.toLowerCase().includes(term)
    )
  }

  // 정렬
  return data.sort((a, b) => {
    let aValue, bValue
    
    if (sortKey.value === 'dcls_strt_day' || sortKey.value === 'kor_co_nm' || sortKey.value === 'fin_prdt_nm') {
      aValue = a[sortKey.value]
      bValue = b[sortKey.value]
    } else {
      // 금리 정보로 정렬
      aValue = getInterestRate(a, sortKey.value)
      bValue = getInterestRate(b, sortKey.value)
      
      // '%' 제거하고 숫자로 변환
      aValue = aValue === '-' ? -1 : parseFloat(aValue.replace('%', ''))
      bValue = bValue === '-' ? -1 : parseFloat(bValue.replace('%', ''))
    }

    if (sortOrder.value === 'asc') {
      return aValue > bValue ? 1 : -1
    }
    return aValue < bValue ? 1 : -1
  })
})

// 컴포넌트 마운트 시 데이터 로드
onMounted(() => {
  productStore.fetchProducts()
})
</script>

<style scoped>
.w-full {
  padding: 2rem;
  background-color: #f8f9fa;
}

/* 검색 필터 스타일링 */
input[type="text"] {
  width: 100%;
  max-width: 400px;
  padding: 0.75rem 1rem;
  border: 1px solid #e5e8eb;
  border-radius: 8px;
  font-size: 0.9375rem;
  transition: all 0.2s ease;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
}

input[type="text"]:focus {
  outline: none;
  border-color: #2D60FF;
  box-shadow: 0 0 0 3px rgba(45, 96, 255, 0.1);
}

/* 테이블 스타일링 */
.overflow-x-auto {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

table {
  border-collapse: separate;
  border-spacing: 0;
  width: 100%;
}

thead {
  background-color: #f8f9fa;
  position: sticky;
  top: 0;
  z-index: 10;
}

th {
  padding: 1rem;
  font-weight: 600;
  color: #4a5568;
  border-bottom: 2px solid #e5e8eb;
  white-space: nowrap;
}

td {
  padding: 1rem;
  color: #2d3748;
  border-bottom: 1px solid #e5e8eb;
}

/* 행 호버 효과 */
tbody tr:hover {
  background-color: #f8faff;
  transition: background-color 0.2s ease;
}

/* 정렬 아이콘 스타일링 */
.flex {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* 금리 셀 스타일링 */
td[class*="text-right"] {
  font-family: 'Roboto Mono', monospace;
  font-weight: 500;
  color: #2D60FF;
}

/* 반응형 테이블 */
.table-container {
  max-height: 70vh;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: #cbd5e0 #f8f9fa;
}

.table-container::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.table-container::-webkit-scrollbar-track {
  background: #f8f9fa;
}

.table-container::-webkit-scrollbar-thumb {
  background-color: #cbd5e0;
  border-radius: 4px;
}

/* 애니메이션 효과 */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

tbody tr {
  animation: fadeIn 0.3s ease-in-out;
}
</style>