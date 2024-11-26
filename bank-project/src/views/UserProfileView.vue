<template>
  <div class="profile-container">
    <div class="profile-header">
      <h1>{{ username }}님의 프로필</h1>
    </div>
    <div class="profile-content">
      <div class="profile-info" v-if="userProfile">
        <!-- 조회 모드 -->
        <div v-if="!isEditing">
          <div class="article-header">
            <h2>회원 정보</h2>
            <div class="article-admin-actions">
              <button @click="startEditing" class="edit-button">수정</button>
            </div>
          </div>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">이메일:</span>
              <span>{{ userProfile.email }}</span>
            </div>
            <div class="info-item">
              <span class="label">전화번호:</span>
              <span>{{ userProfile.phone_number }}</span>
            </div>
            <div class="info-item">
              <span class="label">주소:</span>
              <span>{{ userProfile.address }}</span>
            </div>
            <div class="info-item">
              <span class="label">생년월일:</span>
              <span>{{ formatDate(userProfile.birth_date) }}</span>
            </div>
            <div class="info-item">
              <span class="label">주거래은행:</span>
              <span>{{ userProfile.major_bank }}</span>
            </div>
          </div>
        </div>
        <!-- 수정 모드 -->
        <div v-else>
          <div class="article-header">
            <h2>회원 정보 수정</h2>
            <div class="article-admin-actions">
              <button @click="saveChanges" class="edit-button">저장</button>
              <button @click="cancelEdit" class="delete-button">취소</button>
            </div>
          </div>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">이메일:</span>
              <input v-model="editedProfile.email" type="email" class="edit-input">
            </div>
            <div class="info-item">
              <span class="label">전화번호:</span>
              <input v-model="editedProfile.phone_number" type="tel" class="edit-input">
            </div>
            <div class="info-item">
              <span class="label">주소:</span>
              <input v-model="editedProfile.address" type="text" class="edit-input">
            </div>
            <div class="info-item">
              <span class="label">생년월일:</span>
              <input v-model="editedProfile.birth_date" type="date" class="edit-input">
            </div>
            <div class="info-item">
              <span class="label">주거래은행:</span>
              <select v-model="editedProfile.major_bank" class="edit-input">
                <option value="">주거래은행 선택</option>
                <option value="KB">KB국민은행</option>
                <option value="신한">신한은행</option>
                <option value="우리">우리은행</option>
                <option value="하나">하나은행</option>
                <option value="농협">농협은행</option>
                <option value="기업">IBK기업은행</option>
                <option value="카카오">카카오뱅크</option>
                <option value="토스">토스뱅크</option>
              </select>
            </div>
            <div class="password-change-section">
              <h3>비밀번호 변경</h3>
              <div class="info-item">
                <span class="label">현재 비밀번호:</span>
                <input v-model="passwordForm.currentPassword" type="password" class="edit-input">
              </div>
              <div class="info-item">
                <span class="label">새 비밀번호:</span>
                <input v-model="passwordForm.newPassword1" type="password" class="edit-input">
              </div>
              <div class="info-item">
                <span class="label">새 비밀번호 확인:</span>
                <input v-model="passwordForm.newPassword2" type="password" class="edit-input">
              </div>
              <div class="password-actions">
                <button @click="changePassword" class="password-change-button">비밀번호 변경</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="profile-section">
        <h2>작성한 게시글</h2>
        <div v-if="loading" class="loading">데이터를 불러오는 중...</div>
        <h4 v-else-if="userArticles.length === 0" class="no-content">작성한 게시글이 없습니다.</h4>
        <div v-else class="articles-list">
          <div v-for="(article, index) in userArticles" :key="article.id" class="article-item">
            <router-link :to="`/articles/${article.id}/`">
              <h3>{{ index+1 }}. 제목 : {{ article.title }}</h3>
            </router-link>
          </div>
        </div>
      </div>
      <div class="profile-section2">
        <h2>추천 상품</h2>
        <div v-if="loading" class="loading">데이터를 불러오는 중...</div>
        <div v-else-if="zzimedProduct.length" class="no-content">
          <div v-for="(zzim, index) in zzimedProduct" :key="zzim.fin_prdt_cd" class="article-item">
            <router-link :to="`/products/term_deposit/detail/${zzim.fin_prdt_cd}/`">
              <h3>{{ index+1 }}. {{zzim.kor_co_nm}} - {{ zzim.fin_prdt_nm }}</h3>
            </router-link>
            <div class="chart">
            </div>
          </div>
          <Bar :data="chartData" :options="chartOptions" />
        </div>
        <div v-else class="articles-list">
          <h4>선택한 상품이 없습니다.</h4>
        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { format } from 'date-fns'
import userAPI from '../apis/userAPI'
import { useAuthStore } from '../stores/auth'
import axios from 'axios'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const route = useRoute()
const authStore = useAuthStore()
const username = ref(route.params.username)
const userArticles = ref([])
const userProfile = ref(null)
const loading = ref(true)
const zzimedProduct = ref(null)
const isEditing = ref(false)
const editedProfile = ref({})
const passwordForm = ref({
  currentPassword: '',
  newPassword1: '',
  newPassword2: ''
})


const chartOptions = ref({
  responsive: true,
  plugins: {
    title: {
      display: true,
      text: '상품별 이자율 그래프',
      color: '#000000',
      font: {
        family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
        size: 20,
        weight: '600'
      },
    },
  },
  
  scales: {
    x: {
      title: {
        display: true,
        text: '기간 (months)',
        color: '#000000',
         font: {
          family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
          size: 14,
          weight: '10000'
        }

      }
    },
    y: {
      title: {
        display: true,
        text: '이자율 (%)',
        color: '#000000',
        font: {
          family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
          size: 14,
          weight: '500'
        }
      },
      beginAtZero: true
    }
  }
})

const labels = ref([])
const datasets = ref([])

// computed로 차트 데이터 관리
const chartData = computed(() => ({
  labels: labels.value,
  datasets: datasets.value.map(dataset => ({
    ...dataset,
    backgroundColor: getRandomColor(0.5),
    borderWidth: 1,
    tension: 0.1
  }))
}))

const getRandomColor = (alpha = 1) => {
  const r = Math.floor(Math.random() * 255)
  const g = Math.floor(Math.random() * 255)
  const b = Math.floor(Math.random() * 255)
  return `rgba(${r}, ${g}, ${b}, ${alpha})`
}

const fetchUserData = async () => {
  try {
    const profileResponse = await userAPI.getUserProfile(username.value)
    userProfile.value = profileResponse
    
    // 게시글 데이터 처리
    if (profileResponse.article_set && Array.isArray(profileResponse.article_set)) {
      userArticles.value = profileResponse.article_set
    } else {
      userArticles.value = []
    }
    
    // 추천 상품 데이터 처리
    if (profileResponse.zzim_product && Array.isArray(profileResponse.zzim_product)) {
      zzimedProduct.value = profileResponse.zzim_product
      
      // 차트 데이터 처리
      if (profileResponse.zzim_product.length > 0) {
        // x축 라벨 설정 (기간)
        labels.value = Array.from(new Set(
          profileResponse.zzim_product.flatMap(product => 
            product.termdepositoptions_set.map(option => option.save_trm)
          )
        )).sort((a, b) => a - b)

        // 데이터셋 설정
        datasets.value = profileResponse.zzim_product.map(product => ({
          label: `${product.kor_co_nm} - ${product.fin_prdt_nm}`,
          data: labels.value.map(term => {
            const option = product.termdepositoptions_set.find(opt => opt.save_trm === term)
            return option ? option.intr_rate : null
          })
        }))
      }
    } else {
      zzimedProduct.value = null
    }

  } catch (error) {
    console.error('Error:', error)
    userArticles.value = []
    zzimedProduct.value = null
    labels.value = []
    datasets.value = []
  } finally {
    loading.value = false
  }
}

const formatDate = (date) => format(new Date(date), 'yyyy-MM-dd')

const startEditing = () => {
  editedProfile.value = { ...userProfile.value }
  isEditing.value = true
}

const cancelEdit = () => {
  isEditing.value = false
  editedProfile.value = {}
}

const saveChanges = async () => {
  try {
    const userId = localStorage.getItem('userId')
    const response = await userAPI.updateProfile(userId, editedProfile.value)
    if (response) {
      userProfile.value = response
      isEditing.value = false
      alert('프로필이 성공적으로 수정되었습니다.')
    }
  } catch (error) {
    console.error('프로필 수정 실패:', error)
    alert('프로필 수정에 실패했습니다.')
  }
}

const changePassword = async () => {
  try {
    if (passwordForm.value.newPassword1 !== passwordForm.value.newPassword2) {
      alert('새 비밀번호가 일치하지 않습니다.')
      return
    }
    const response = await axios.post(
      'http://localhost:8000/accounts/password/change/',
      {
        old_password: passwordForm.value.currentPassword,
        new_password1: passwordForm.value.newPassword1,
        new_password2: passwordForm.value.newPassword2
      },
      {
        headers: {
          'Authorization': `Token ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        }
      }
    )
    if (response.status === 200) {
      alert('비밀번호가 성공적으로 변경되었습니다.')
      passwordForm.value = {
        currentPassword: '',
        newPassword1: '',
        newPassword2: ''
      }
    }
  } catch (error) {
    console.error('비밀번호 변경 실패:', error)
    alert(error.response?.data?.old_password?.[0] || 
          error.response?.data?.new_password1?.[0] || 
          error.response?.data?.new_password2?.[0] || 
          '비밀번호 변경에 실패했습니다.')
  }
}
// onBeforeMount(fetchUserData)
onMounted(fetchUserData)
</script>


<style scoped>
.profile-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 24px;
}

.profile-header {
  text-align: center;
  margin-bottom: 40px;
}

.profile-header h1 {
  font-size: 32px;
  font-weight: 700;
  color: #191F28;
}

.profile-section {
  background: #FFFFFF;
  border-radius: 16px;
  padding: 32px;
  margin-top: 20px;
  margin-bottom: 10px;
  border: 1px solid #E5E8EB;
}


.profile-section h2 {
  font-size: 28px;
  font-weight: 700;
  color: #191F28;
  margin-bottom: 32px;
  position: relative;
  display: inline-block;
}

.profile-section2 {
  background: #FFFFFF;
  border-radius: 16px;
  padding: 32px;
  margin-top: 20px;
  margin-bottom: 80px;
  border: 1px solid #E5E8EB;
}


.profile-section2 h2 {
  font-size: 28px;
  font-weight: 700;
  color: #191F28;
  margin-bottom: 32px;
  position: relative;
  display: inline-block;
}

.profile-section h2::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, #2D60FF 0%, #1E4AD6 100%);
  border-radius: 2px;
}

.article-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.article-header h2 {
  font-size: 24px;
  font-weight: 700;
  color: #191F28;
}

.info-grid {
  display: grid;
  gap: 24px;
}

.info-item {
  margin-bottom: 1px; /* 간격 증가 */

  display: flex;
  align-items: center; /* 라벨과 입력 필드 수평 정렬 */
}

.label {
  min-width: 120px;
  font-size: 16px;
  font-weight: 500;
  color: #4E5968;
}

.edit-input {
  flex: 1;
  height: 48px;
  padding: 0 16px;
  margin-left : 10px;
  border: 1px solid #E5E8EB;
  border-radius: 8px;
  font-size: 16px;
  color: #191F28;
  background: #FFFFFF;
}

.edit-input:focus {
  outline: none;
  border-color: #2D60FF;
}

button {
  height: 48px;
  padding: 0 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}

.edit-button {
  background-color: #0061f2c0; /* 토스 느낌의 파란색 */
  color: white;
  border: none;
  margin-right: 10px;
  border-radius: 50px; /* 더 둥근 모서리 */
  padding: 6px 14px; /* 여백을 적당히 줄여서 크기 작게 */
  font-size: 14px; /* 글씨 크기 줄이기 */
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 부드러운 그림자 효과 */
  transition: all 0.3s ease; /* 모든 속성에 부드러운 전환 효과 */
}

.edit-button:hover {
  background: #1E4AD6;
}

.delete-button {
  background-color: #72b8e7; /* 채도가 낮고 깊이가 있는 빨간색 */
  color: white;
  border: none;
  margin-right: 10px;
  border-radius: 50px; /* 더 둥근 모서리 */
  padding: 6px 14px; /* 여백을 적당히 줄여서 크기 작게 */
  font-size: 14px; /* 글씨 크기 줄이기 */
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 부드러운 그림자 효과 */
  transition: all 0.3s ease; /* 모든 속성에 부드러운 전환 효과 */
}

.delete-button:hover {
  background-color: #406883;
  color : red
}

.password-change-section {
  margin-top: 48px;
  padding-top: 32px;
  border-top: 1px solid #E5E8EB;
}

.password-change-section h3 {
  font-size: 20px;
  font-weight: 600;
  color: #191F28;
  margin-bottom: 24px;
}

.no-content, .loading, .articles-list {
  text-align: left;
  color: #000000;
  font-size: 16px;
}

@media (max-width: 768px) {
  .profile-container {
    padding: 24px 16px;
  }
  
  .info-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .label {
    min-width: auto;
  }
  
  .edit-input {
    width: 100%;
  }
}
.articles-list .article-item a {
  text-decoration: none; /* 밑줄 제거 */
  color: inherit; /* 기본 텍스트 색상 상속 */
}

/* 링크를 클릭했을 때 효과도 제거 */
.articles-list .article-item a:hover {
  text-decoration: none; /* hover 시에도 밑줄 제거 */
  color: inherit; /* hover 시 색상 변경되지 않도록 */
}
.no-content .article-item a {
  text-decoration: none; /* 밑줄 없애기 */
  color: inherit; /* 텍스트 색상 상속 */
}

.no-content .article-item a:hover {
  color: inherit; /* 마우스 오버 시 색상 변경을 방지 */
}
.password-change-button {
  background-color: #0061f2c0; /* 토스 느낌의 파란색 */
  position: relative;
  display: flex;
  justify-content: center; /* 수평 가운데 정렬 */
  align-items: center; /* 수직 가운데 정렬 */
  color: white;
  border: none;
  margin: auto;
  border-radius: 50px; /* 더 둥근 모서리 */
  padding: 6px 14px; /* 여백을 적당히 줄여서 크기 작게 */
  font-size: 14px; /* 글씨 크기 줄이기 */
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 부드러운 그림자 효과 */
  transition: all 0.3s ease; /* 모든 속성에 부드러운 전환 효과 */
}

.password-change-button:hover{
  background-color: #033888c0;
}

.chart {
  margin-bottom: 0px;
}
</style>