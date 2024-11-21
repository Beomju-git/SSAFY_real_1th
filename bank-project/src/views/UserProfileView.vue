<template>
  <div class="profile-container">
    <div class="profile-header">
      <h1>{{ username }}님의 프로필</h1>
    </div>

    <div class="profile-content">
      <div class="profile-info" v-if="userProfile">
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
                <input 
                  v-model="passwordForm.currentPassword" 
                  type="password" 
                  class="edit-input"
                >
              </div>
              <div class="info-item">
                <span class="label">새 비밀번호:</span>
                <input 
                  v-model="passwordForm.newPassword1" 
                  type="password" 
                  class="edit-input"
                >
              </div>
              <div class="info-item">
                <span class="label">새 비밀번호 확인:</span>
                <input 
                  v-model="passwordForm.newPassword2" 
                  type="password" 
                  class="edit-input"
                >
              </div>
              <div class="password-actions">
                <button @click="changePassword" class="password-change-button">
                  비밀번호 변경
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="profile-section">
        <h2>작성한 게시글</h2>
        <div v-if="loading" class="loading">
          데이터를 불러오는 중...
        </div>
        <div v-else-if="userArticles.length === 0" class="no-content">
          작성한 게시글이 없습니다.
        </div>
        <div v-else class="articles-list">
          <div v-for="article in userArticles" :key="article.id" class="article-item">
            <router-link :to="`/articles/${article.id}/`">
              <h3>{{ article.title }}</h3>
            </router-link>
          </div>
        </div>
      </div>
      <div class="profile-section">
        <h2>추천 상품</h2>
        <div v-if="loading" class="loading">
          데이터를 불러오는 중...
        </div>
        <div v-else-if="zzimedProduct" class="no-content">
          <div v-for="zzim in zzimedProduct" :key="zzim.fin_prdt_cd" class="article-item">
            <router-link :to="`/products/term_deposit/detail/${zzim.fin_prdt_cd}/`">
              <h3> {{zzim.kor_co_nm}} - {{ zzim.fin_prdt_nm }}</h3>
            </router-link>
          </div>          
        </div>
        <div v-else class="articles-list">
          <p>선택한 상품이 없습니다.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { format } from 'date-fns'
import userAPI from '../apis/userAPI'
import { useAuthStore } from '../stores/auth'
import axios from 'axios'

const debuginfo = () => {
  console.log(userAPI)
}

export default {
  name: 'UserProfileView',
  
  setup() {
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

    const fetchUserData = async () => {
      try {
        // 1단계: username 확인
        console.log('1. Username from route:', username.value)
        
        // 2단계: API 호출 전
        console.log('2. Calling getUserProfile API...')
        const profileResponse = await userAPI.getUserProfile(username.value)
        
        // 3단계: API 응답 전체 데이터 확인
        console.log('3. Full API Response:', profileResponse)
        
        // 4단계: 프로필 데이터 할당 전 확인
        console.log('4. Profile data before assignment:', profileResponse)
        userProfile.value = profileResponse
        
        // 5단계: 프로필 데이터 할당 후 확인
        console.log('5. Profile data after assignment:', userProfile.value)
        
        // 6단계: 게시글 데이터 할당 전 확인
        console.log('6. Articles data before assignment:', profileResponse.article_set)
        userArticles.value = profileResponse.article_set || []
        zzimedProduct.value = profileResponse.zzim_product || '선택한 상품이 없습니다.'
        // 7단계: 게시글 데이터 할당 후 확인
        console.log('7. Final articles data:', userArticles.value)
        console.log(profileResponse.zzim_product)
        
      } catch (error) {
        // 8단계: 에러 발생 시 상세 정보
        console.error('8. Error occurred:', {
          message: error.message,
          response: error.response?.data,
          status: error.response?.status
        })
      } finally {
        loading.value = false
      }
    }

    const formatDate = (date) => {
      return format(new Date(date), 'yyyy-MM-dd')
    }

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
        const response = await userAPI.updateProfile(
          userId,
          editedProfile.value
        )
        
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

        const response = await axios.post(`http://localhost:8000/accounts/password/change/`, {
          old_password: passwordForm.value.currentPassword,
          new_password1: passwordForm.value.newPassword1,
          new_password2: passwordForm.value.newPassword2
        }, {
          headers: {
            'Authorization': `Token ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          }
        })

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

    onMounted(fetchUserData)

    return {
      username,
      userArticles,
      userProfile,
      loading,
      zzimedProduct,
      formatDate,
      isEditing,
      editedProfile,
      startEditing,
      cancelEdit,
      saveChanges,
      passwordForm,
      changePassword
    }
  }
}
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
  margin-top: 40px;
  margin-bottom: 40px;
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
  display: flex;
  align-items: center;
  gap: 16px;
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
  background: #2D60FF;
  color: #FFFFFF;
  border: none;
}

.edit-button:hover {
  background: #1E4AD6;
}

.delete-button {
  background: #FFFFFF;
  color: #F04452;
  border: 1px solid #E5E8EB;
}

.delete-button:hover {
  background: #F9FAFB;
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

.no-content, .loading {
  text-align: center;
  padding: 48px 0;
  color: #8B95A1;
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
</style>