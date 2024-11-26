<template>
  <div class="chat-container">
    <header class="chat-header">
      <h1 class="title">AI 금융 상담</h1>
      <p class="subtitle">맞춤형 금융 상품을 추천해드려요</p>
    </header>

    <main class="chat-messages" ref="chatContainer">
      <div v-for="(message, index) in messages" 
           :key="index" 
           :class="['message', message.type]">
        <div class="message-content">
          <div v-if="message.type === 'bot'" class="bot-avatar">
            <span class="avatar-text">AI</span>
          </div>
          <div v-if="message.type === 'bot'" class="recommendation-card">
            <h3 class="product-title">{{ message.recommendation.product }}</h3>
            <div class="recommendation-content">
              <p class="reason-text">{{ message.recommendation.reason }}</p>
              <p class="details-text">{{ message.recommendation.details }}</p>
            </div>
          </div>
          <div v-else class="user-message">
            {{ message.text }}
          </div>
        </div>
      </div>
      <div v-if="isTyping" class="message bot">
        <div class="message-content">
          <div class="bot-avatar">
            <span class="avatar-text">AI</span>
          </div>
          <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    </main>

    <div class="chat-input-container">
      <div class="input-wrapper">
        <input 
          type="text" 
          v-model="userInput"
          @keyup.enter="sendMessage"
          placeholder="궁금한 금융 상품을 물어보세요"
          :disabled="isTyping"
          class="chat-input"
        >
        <button 
          @click="sendMessage" 
          :disabled="isTyping || !userInput.trim()"
          class="send-button"
        >
          전송
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import axios from 'axios'

const messages = ref([])
const userInput = ref('')
const isTyping = ref(false)
const chatContainer = ref(null)

// 초기 메시지
onMounted(() => {
  addBotMessage({
    product: '안녕하세요!',
    reason: '금융 상품 추천 AI 어시스턴트입니다.',
    details: '어떤 금융 상품을 찾고 계신가요?'
  })
})

watch(messages, () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
})

const addBotMessage = async (recommendation) => {
  isTyping.value = true
  await new Promise(resolve => setTimeout(resolve, 1000))
  messages.value.push({ 
    type: 'bot', 
    recommendation: recommendation 
  })
  isTyping.value = false
}

const chatWithBot = async (message) => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/chat/recommend/', {
      message: message
    });
    return response.data.message;
  } catch (error) {
    console.error('챗봇 오류:', error);
    throw error;
  }
};

const sendMessage = async () => {
  if (!userInput.value.trim() || isTyping.value) return

  const userMessage = userInput.value
  messages.value.push({ type: 'user', text: userMessage })
  userInput.value = ''

  try {
    isTyping.value = true
    const botResponse = await chatWithBot(userMessage)
    await addBotMessage(botResponse)
  } catch (error) {
    await addBotMessage({
      product: '오류 발생',
      reason: '죄송합니다. 일시적인 오류가 발생했습니다.',
      details: '잠시 후 다시 시도해주세요.'
    })
  } finally {
    isTyping.value = false
  }
}
</script>

<style scoped>
.chat-container {
  max-width: 800px;
  margin: 0 auto;
  height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 20px 20px 80px; /* 하단 패딩 증가 */
  box-sizing: border-box;
}

.chat-header {
  text-align: center;
  padding: 16px 0;
  flex-shrink: 0;
}

.title {
  font-size: 28px;
  font-weight: 700;
  color: #191f28;
  margin-bottom: 8px;
}

.subtitle {
  font-size: 16px;
  color: #8b95a1;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f9fafc;
  border-radius: 16px;
  margin-bottom: 20px;
  min-height: 200px; /* 최소 높이 설정 */
}

.message {
  margin-bottom: 20px;
}

.message-content {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.bot-avatar {
  width: 40px;
  height: 40px;
  background: #3182f6;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.avatar-text {
  color: white;
  font-weight: 600;
  font-size: 14px;
}

.recommendation-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  max-width: 600px;
}

.product-title {
  font-size: 18px;
  font-weight: 700;
  color: #191f28;
  margin-bottom: 12px;
}

.recommendation-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.reason-text {
  color: #3182f6;
  font-weight: 500;
  font-size: 15px;
}

.details-text {
  color: #4e5968;
  font-size: 14px;
  line-height: 1.6;
}

.user-message {
  background: #3182f6;
  color: white;
  padding: 12px 16px;
  border-radius: 16px;
  margin-left: auto;
  font-size: 15px;
}

.chat-input-container {
  flex-shrink: 0;
  background: white;
  padding: 16px 0;
  margin-top: auto;
}

.input-wrapper {
  display: flex;
  gap: 12px;
}

.chat-input {
  flex: 1;
  padding: 16px;
  border: 1px solid #eaecef;
  border-radius: 12px;
  font-size: 15px;
  transition: all 0.2s;
}

.chat-input:focus {
  outline: none;
  border-color: #3182f6;
  box-shadow: 0 0 0 3px rgba(49, 130, 246, 0.1);
}

.send-button {
  padding: 0 24px;
  background: #3182f6;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 15px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.send-button:hover {
  background: #1b64da;
}

.send-button:disabled {
  background: #e9ecef;
  cursor: not-allowed;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 12px 16px;
  background: white;
  border-radius: 16px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: #3182f6;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
.typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .chat-container {
    padding: 16px 16px 60px;
  }

  .title {
    font-size: 24px;
  }

  .chat-messages {
    padding: 16px;
  }

  .recommendation-card {
    padding: 16px;
  }
}
</style>
