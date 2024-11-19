<template>
  <Transition name="fade">
    <div v-if="isVisible" class="modal" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2 class="title">회원가입</h2>
          <button class="close-button" @click="closeModal" aria-label="닫기">×</button>
        </div>
        <form @submit.prevent="handleSignup" class="form">
          <div class="form-group">
            <input 
              type="text" 
              id="username"
              v-model="signupForm.username"
              placeholder="아이디"
              required
              class="form-input"
            />
          </div>
          <div class="form-group">
            <div class="password-input-wrapper">
              <input 
                :type="showPassword ? 'text' : 'password'"
                id="password1"
                v-model="signupForm.password1"
                placeholder="비밀번호"
                required
                class="form-input"
              />
              <button type="button" class="password-toggle" @click="showPassword = !showPassword">
                {{ showPassword ? '숨기기' : '보기' }}
              </button>
            </div>
          </div>
          <div class="form-group">
            <div class="password-input-wrapper">
              <input 
                :type="showPassword ? 'text' : 'password'"
                id="password2"
                v-model="signupForm.password2"
                placeholder="비밀번호 확인"
                required
                class="form-input"
              />
            </div>
          </div>
          <div class="form-group">
            <input 
              type="email" 
              id="email"
              v-model="signupForm.email"
              placeholder="이메일"
              required
              class="form-input"
            />
          </div>
          <div class="form-group">
            <input 
              type="tel" 
              id="phone_number"
              v-model="signupForm.phone_number"
              placeholder="전화번호 (예: 010-1234-5678)"
              pattern="[0-9]{3}-[0-9]{4}-[0-9]{4}"
              required
              class="form-input"
            />
          </div>
          <div class="form-group">
            <input 
              type="text" 
              id="address"
              v-model="signupForm.address"
              placeholder="주소"
              required
              class="form-input"
            />
          </div>
          <div class="form-group">
            <input 
              type="date" 
              id="birth_date"
              v-model="signupForm.birth_date"
              placeholder="생년월일"
              required
              class="form-input"
            />
          </div>
          <div class="form-group">
            <select 
              id="major_bank"
              v-model="signupForm.major_bank"
              required
              class="form-input"
            >
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
          <button 
            type="submit" 
            class="submit-button" 
            :class="{ 'loading': isLoading }"
            :disabled="isLoading || !isFormValid"
          >
            <span v-if="isLoading" class="loader"></span>
            <span>{{ isLoading ? '가입 중' : '가입하기' }}</span>
          </button>
        </form>
        <div class="login-section">
          <p>이미 계정이 있으신가요?</p>
          <a href="#" class="login-link" @click.prevent="switchToLogin">로그인</a>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const props = defineProps(['isVisible', 'closeModal', 'switchToLogin'])
const signupForm = ref({ 
  username: '', 
  password1: '', 
  password2: '',
  email: '',
  phone_number: '',
  address: '',
  birth_date: '',
  major_bank: ''
})
const error = ref('')
const isLoading = ref(false)
const showPassword = ref(false)

const isFormValid = computed(() => {
  return signupForm.value.username.length > 0 && 
         signupForm.value.password1.length > 0 &&
         signupForm.value.password2.length > 0 &&
         signupForm.value.password1 === signupForm.value.password2 &&
         signupForm.value.email.length > 0 &&
         signupForm.value.phone_number.length > 0 &&
         signupForm.value.address.length > 0 &&
         signupForm.value.birth_date.length > 0 &&
         signupForm.value.major_bank.length > 0
})

const emit = defineEmits(['close-signup', 'close-login'])

const handleSignup = async () => {
  try {
    isLoading.value = true
    error.value = ''
    
    // 1. 회원가입
    const signupResponse = await axios.post('http://localhost:8000/accounts/signup/', {
      username: signupForm.value.username,
      password1: signupForm.value.password1,
      password2: signupForm.value.password2,
    })
    console.log('Signup Response:', signupResponse.data)

    // 2. 로그인
    const loginResponse = await axios.post('http://localhost:8000/accounts/login/', {
      username: signupForm.value.username,
      password: signupForm.value.password1
    })
    console.log('Login Response:', loginResponse.data)

    const token = loginResponse.data.key

    // 3. 사용자 정보 조회
    const userResponse = await axios.get('http://localhost:8000/accounts/user/', {
      headers: {
        'Authorization': `Token ${token}`
      }
    })
    console.log('User Response:', userResponse.data)
    
    const userId = userResponse.data.pk

    // 4. 토큰 저장
    localStorage.setItem('token', token)
    const authStore = useAuthStore()
    authStore.token = token
    authStore.user = {
      id: userId,
      username: signupForm.value.username
    }

    // 5. 추가 정보 업데이트 시도 후
    try {
      // 전화번호에서 하이픈 제거
      const formattedPhoneNumber = signupForm.value.phone_number.replace(/-/g, '')
      
      // 날짜 형식 변환
      const formattedBirthDate = new Date(signupForm.value.birth_date)
        .toISOString()
        .split('T')[0]

      const detailResponse = await axios.put(`http://localhost:8000/profile/${userId}/detail/`, {
        email: signupForm.value.email,
        phone_number: formattedPhoneNumber,
        address: signupForm.value.address,
        birth_date: formattedBirthDate,
        major_bank: signupForm.value.major_bank
      }, {
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        }
      })
      console.log('Detail Update Response:', detailResponse.data)

      // 6. 폼 초기화
      signupForm.value = {
        username: '',
        password1: '',
        password2: '',
        email: '',
        phone_number: '',
        address: '',
        birth_date: '',
        major_bank: ''
      }
      
      // 7. 두 모달 모두 닫기
      emit('close-signup')
      emit('close-login')

    } catch (detailError) {
      console.error('Detail Update Error:', detailError.response?.data)
      // 추가 정보 업데이트 실패해도 회원가입은 완료된 것으로 처리
      emit('close-signup')
      emit('close-login')
    }

  } catch (err) {
    console.error('Signup Error:', err.response?.data)
    error.value = err.response?.data?.non_field_errors?.[0] || '회원가입에 실패했습니다'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 32px;
  border-radius: 24px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  margin-bottom: 2rem;
}

.title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #191f28;
  margin: 0;
}

.close-button {
  position: absolute;
  right: 1.5rem;
  top: 1.5rem;
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #8b95a1;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.close-button:hover {
  background-color: rgba(0,0,0,0.05);
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  width: 100%;
  margin-bottom: 1rem;
}

.form-input {
  width: 90%;
  height: 52px;
  padding: 0 16px;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  font-size: 16px;
  color: #111827;
  background-color: #F9FAFB;
  transition: all 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: #2D60FF;
  background-color: white;
  box-shadow: 0 0 0 4px rgba(45, 96, 255, 0.1);
}

.form-input::placeholder {
  color: #8b95a1;
}

.password-input-wrapper {
  position: relative;
}

.password-toggle {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #2D60FF;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.password-toggle:hover {
  background-color: rgba(45, 96, 255, 0.05);
}

select.form-input {
  appearance: none;
  padding-right: 40px;
  background-image: url("data:image/svg+xml,%3Csvg width='16' height='16' viewBox='0 0 16 16' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M4 6L8 10L12 6' stroke='%236B7280' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 16px center;
}

.submit-button {
  height: 52px;
  background-color: #2D60FF;
  color: white;
  border: none;
  border-radius: 16px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 1rem;
}

.submit-button:hover:not(:disabled) {
  background-color: #1E4AD6;
  transform: translateY(-1px);
}

.submit-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.login-section {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e8eb;
  text-align: center;
}

.login-section p {
  color: #8b95a1;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.login-link {
  color: #2D60FF;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s;
}

.login-link:hover {
  color: #1E4AD6;
  text-decoration: underline;
}

/* 스크롤바 커스터마이징 */
.modal-content::-webkit-scrollbar {
  width: 8px;
}

.modal-content::-webkit-scrollbar-track {
  background: transparent;
}

.modal-content::-webkit-scrollbar-thumb {
  background-color: #e5e8eb;
  border-radius: 4px;
}

.modal-content::-webkit-scrollbar-thumb:hover {
  background-color: #d1d6db;
}

/* 날짜 입력 필드 특별 스타일링 */
.form-input[type="date"] {
  padding: 0 12px;
  font-family: inherit;
}
</style>