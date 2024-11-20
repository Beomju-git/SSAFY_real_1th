<template>
  <div class="profile-container">
    <div class="profile-header">
      <h1>{{ username }}님의 프로필</h1>
    </div>

    <div class="profile-content">
      <div class="profile-info" v-if="userProfile">
        <h2>회원 정보</h2>
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
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { format } from 'date-fns'
import userAPI from '../apis/userAPI'
import { useAuthStore } from '../stores/auth'

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
        
        // 7단계: 게시글 데이터 할당 후 확인
        console.log('7. Final articles data:', userArticles.value)
        
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

    onMounted(fetchUserData)

    return {
      username,
      userArticles,
      userProfile,
      loading,
      formatDate
    }
  }
}
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.profile-header {
  text-align: center;
  margin-bottom: 40px;
}

.profile-section {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.profile-section h2 {
  color: #333;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #2D60FF;
}

.loading, .no-content {
  text-align: center;
  padding: 20px;
  color: #666;
}

.article-item, .comment-item {
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.article-item:last-child, .comment-item:last-child {
  border-bottom: none;
}

.article-item a {
  text-decoration: none;
  color: inherit;
}

.article-item h3 {
  color: #2D60FF;
  margin-bottom: 5px;
}

.article-date, .comment-date {
  color: #666;
  font-size: 0.9em;
}

.comment-content {
  margin-bottom: 10px;
}

.article-link {
  color: #2D60FF;
  text-decoration: none;
  font-size: 0.9em;
}

.article-link:hover {
  text-decoration: underline;
}

.info-grid {
  display: grid;
  gap: 1rem;
  padding: 1rem;
}

.info-item {
  display: flex;
  gap: 1rem;
}

.label {
  font-weight: bold;
  min-width: 100px;
  color: #666;
}
</style>