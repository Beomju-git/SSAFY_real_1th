<template>
  <Transition name="fade">
    <div v-if="isVisible" class="modal" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2 class="title">로그인/회원가입</h2>
          <button class="close-button" @click="closeModal" aria-label="닫기">×</button>
        </div>
        <form @submit.prevent="handleLogin" class="form">
          <div class="form-group">
            <input 
              type="text" 
              id="username"
              v-model="loginForm.username"
              :disabled="isLoading"
              placeholder="아이디"
              required
              class="form-input"
            />
          </div>
          <div class="form-group">
            <div class="password-input-wrapper">
              <input 
                :type="showPassword ? 'text' : 'password'"
                id="password"
                v-model="loginForm.password"
                :disabled="isLoading"
                placeholder="비밀번호"
                required
                class="form-input"
              />
              <button 
                type="button" 
                class="password-toggle"
                @click="showPassword = !showPassword"
              >
                {{ showPassword ? '숨기기' : '보기' }}
              </button>
            </div>
          </div>
          <Transition name="fade">
            <div v-if="error" class="error-message">
              {{ error }}
            </div>
          </Transition>
          <button 
            type="submit" 
            class="submit-button" 
            :class="{ 'loading': isLoading }"
            :disabled="isLoading || !isFormValid"
          >
            <span v-if="isLoading" class="loader"></span>
            <span>{{ isLoading ? '로그인 중' : '로그인' }}</span>
          </button>
        </form>
        <div class="signup-section">
          <p>아직 계정이 없으신가요?</p>
          <a href="#" class="signup-link" @click.prevent="switchToSignup">
            회원가입
          </a>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const props = defineProps(['isVisible', 'closeModal', 'switchToSignup'])
const emit = defineEmits(['close'])
const authStore = useAuthStore()
const loginForm = ref({ username: '', password: '' })
const error = ref('')
const isLoading = ref(false)
const showPassword = ref(false)

const isFormValid = computed(() => {
  return loginForm.value.username.length > 0 && 
         loginForm.value.password.length > 0
})

const handleLogin = async () => {
  try {
    isLoading.value = true
    error.value = ''
    const response = await axios.post('http://localhost:8000/accounts/login/', {
      username: loginForm.value.username,
      password: loginForm.value.password
    })
    
    console.log('로그인 응답:', response.data)

    if (response.data.key) {
      authStore.token = response.data.key
      loginForm.value = { username: '', password: '' }
      props.closeModal()
    } else {
      error.value = '로그인 실패: 토큰이 없습니다'
      console.error('토큰 없음:', response.data)
    }
  } catch (err) {
    console.error('로그인 에러:', err.response?.data || err)
    error.value = err.response?.data?.non_field_errors?.[0] || 
                 '아이디 또는 비밀번호가 일치하지 않습니다'
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
  padding: 1.75rem;
  border-radius: 16px;
  width: 100%;
  max-width: 320px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #191f28;
  margin: 0;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #8b95a1;
  cursor: pointer;
  padding: 0.25rem;
  line-height: 1;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
}

.form-group {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  margin-bottom: 1rem;
}

.form-input {
  width: 100%;
  height: 44px;
  padding: 0 0.875rem;
  border: 1px solid #e5e8eb;
  border-radius: 8px;
  font-size: 0.9375rem;
  transition: all 0.2s ease;
  background-color: white;
}

.form-input::placeholder {
  color: #8b95a1;
}

.form-input:focus {
  outline: none;
  border-color: #2D60FF;
  box-shadow: 0 0 0 2px rgba(45, 96, 255, 0.08);
}

.form-input:disabled {
  background-color: #f9fafb;
  cursor: not-allowed;
}

.password-input-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  position: relative;
}

.password-toggle {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #2D60FF;
  font-size: 0.8125rem;
  font-weight: 500;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
}

.error-message {
  font-size: 0.8125rem;
  color: #e64c3c;
  margin: 0.25rem 0;
  text-align: center;
}

.submit-button {
  width: 100%;
  height: 44px;
  background-color: #2D60FF;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 0.5rem;
}

.submit-button:hover:not(:disabled) {
  background-color: #1E4AD6;
}

.submit-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loader {
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s linear infinite;
  margin-right: 0.5rem;
  display: inline-block;
  vertical-align: middle;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.signup-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 1.5rem;
  text-align: center;
}

.signup-section p {
  color: #8b95a1;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.signup-link {
  color: #2D60FF;
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 600;
  transition: color 0.2s ease;
}

.signup-link:hover {
  color: #1E4AD6;
  text-decoration: underline;
}
</style>    