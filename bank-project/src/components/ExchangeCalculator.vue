<!-- src/components/ExchangeCalculator.vue -->
<template>
  <div class="exchange-calculator">
    <h1 class="title">환율 계산기</h1>

    <!-- 로딩 상태 -->
    <div v-if="isLoading" class="loading">
      Loading...
    </div>

    <!-- 에러 메시지 -->
    <div v-else-if="error" class="error-message">
      {{ error }}
    </div>

    <!-- 메인 폼 -->
    <div v-else class="calculator-form">
      <!-- 금액 입력 -->
      <div class="input-group">
        <label>금액</label>
        <input 
          type="number" 
          v-model="amount"
          placeholder="금액을 입력하세요"
          min="0"
        >
      </div>

      <div class="currency-selectors">
        <!-- 출발 통화 -->
        <div class="select-group">
          <label>변환할 통화</label>
          <select v-model="fromCurrency">
            <option 
              v-for="currency in currencies" 
              :key="currency.id"
              :value="currency"
            >
              {{ currency.country }} ({{ currency.cur_unit }})
            </option>
          </select>
        </div>

        <!-- 도착 통화 -->
        <div class="select-group">
          <label>변환될 통화</label>
          <select v-model="toCurrency">
            <option 
              v-for="currency in currencies" 
              :key="currency.id"
              :value="currency"
            >
              {{ currency.country }} ({{ currency.cur_unit }})
            </option>
          </select>
        </div>
      </div>

      <!-- 결과 표시 -->
      <div v-if="fromCurrency && toCurrency && calculatedAmount" 
           class="result-card">
        <p class="conversion-result">
          <span class="amount">
            {{ formatNumber(amount) }} {{ fromCurrency.cur_unit }}
          </span>
          <span class="equals">=</span>
          <span class="converted-amount">
            {{ formatNumber(calculatedAmount) }} {{ toCurrency.cur_unit }}
          </span>
        </p>
        <p class="exchange-rate">
          환율: 1 {{ fromCurrency.cur_unit }} = 
          {{ formatNumber(getExchangeRate()) }} {{ toCurrency.cur_unit }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getExchangeRates } from '../apis/exchangeAPI'

// 기존 script 내용 유지
const currencies = ref([])
const amount = ref(100)
const fromCurrency = ref(null)
const toCurrency = ref(null)
const isLoading = ref(true)
const error = ref(null)

// 환율 계산
const calculatedAmount = computed(() => {
  if (!amount.value || !fromCurrency.value || !toCurrency.value) return null
  
  const fromRate = fromCurrency.value.rate
  const toRate = toCurrency.value.rate
  
  let result
  if (fromCurrency.value.cur_unit.includes('(100)')) {
    result = (amount.value * fromRate * 100) / toRate
  } else if (toCurrency.value.cur_unit.includes('(100)')) {
    result = (amount.value * fromRate) / (toRate * 100)
  } else {
    result = (amount.value * fromRate) / toRate
  }
  
  return result
})

const getExchangeRate = () => {
  if (!fromCurrency.value || !toCurrency.value) return 0
  
  const fromRate = fromCurrency.value.rate
  const toRate = toCurrency.value.rate
  
  if (fromCurrency.value.cur_unit.includes('(100)')) {
    return (fromRate * 100) / toRate
  } else if (toCurrency.value.cur_unit.includes('(100)')) {
    return fromRate / (toRate * 100)
  }
  return fromRate / toRate
}

const formatNumber = (value) => {
  return new Intl.NumberFormat('ko-KR', {
    maximumFractionDigits: 2,
    minimumFractionDigits: 2
  }).format(value)
}

const loadData = async () => {
  try {
    isLoading.value = true
    error.value = null
    const data = await getExchangeRates()
    currencies.value = data

    fromCurrency.value = data.find(c => c.cur_unit === 'USD')
    toCurrency.value = data.find(c => c.cur_unit === 'KRW')
  } catch (e) {
    error.value = '환율 정보를 불러오는데 실패했습니다.'
    console.error(e)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.exchange-calculator {
  max-width: 480px;
  margin: 0 auto;
  padding: 24px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.title {
  font-size: 24px;
  font-weight: 700;
  color: #191f28;
  margin-bottom: 32px;
}

.loading {
  text-align: center;
  padding: 24px;
  color: #8b95a1;
}

.error-message {
  background-color: #fff5f5;
  border: 1px solid #ff6b6b;
  color: #e03131;
  padding: 16px;
  border-radius: 12px;
  margin-bottom: 16px;
}

.calculator-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.input-group, .select-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.currency-selectors {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

label {
  font-size: 14px;
  font-weight: 500;
  color: #4e5968;
}

input, select {
  width: 100%;
  padding: 16px;
  border: 1px solid #e5e8eb;
  border-radius: 12px;
  font-size: 16px;
  color: #191f28;
  background-color: #fff;
  transition: all 0.2s ease;
}

input:focus, select:focus {
  outline: none;
  border-color: #3182f6;
  box-shadow: 0 0 0 3px rgba(49, 130, 246, 0.1);
}

input::placeholder {
  color: #8b95a1;
}

.result-card {
  background-color: #f8f9fa;
  padding: 24px;
  border-radius: 16px;
  border: 1px solid #e5e8eb;
}

.conversion-result {
  font-size: 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.amount {
  font-weight: 500;
}

.equals {
  color: #8b95a1;
}

.converted-amount {
  font-weight: 700;
  color: #3182f6;
}

.exchange-rate {
  font-size: 14px;
  color: #8b95a1;
}

/* 호버 효과 */
input:hover, select:hover {
  border-color: #ccd3dc;
}

/* 모바일 대응 */
@media (max-width: 480px) {
  .exchange-calculator {
    padding: 16px;
  }

  .currency-selectors {
    grid-template-columns: 1fr;
  }
}
</style>