<template>
  <div class="chat-container">
    <div class="chat-header">
      <h1>AI 금융 상품 추천</h1>
      <p>AI와 대화하면서 나에게 맞는 금융 상품을 찾아보세요</p>
    </div>

    <div class="chat-messages" ref="chatContainer">
      <div v-for="(message, index) in messages" 
           :key="index" 
           :class="['message', message.type]">
        <div class="message-content">
          <div v-if="message.type === 'bot'" class="bot-avatar">AI</div>
          <div v-if="message.type === 'bot'" class="recommendation-card">
            <h3 class="product">{{ message.recommendation.product }}</h3>
            <p class="reason">{{ message.recommendation.reason }}</p>
            <p class="details">{{ message.recommendation.details }}</p>
          </div>
          <div v-else>
            {{ message.text }}
          </div>
        </div>
      </div>
      <div v-if="isTyping" class="message bot">
        <div class="message-content">
          <div class="bot-avatar">AI</div>
          <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    </div>

    <div class="chat-input">
      <input 
        type="text" 
        v-model="userInput"
        @keyup.enter="sendMessage"
        placeholder="메시지를 입력하세요..."
        :disabled="isTyping"
      >
      <button @click="sendMessage" :disabled="isTyping || !userInput.trim()">
        전송
      </button>
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
  padding: 20px;
  height: 80vh;
  display: flex;
  flex-direction: column;
}

.chat-header {
  text-align: center;
  margin-bottom: 20px;
}

.chat-header h1 {
  color: #2c3e50;
  margin-bottom: 8px;
}

.chat-header p {
  color: #666;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
  margin-bottom: 20px;
}

.message {
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
}

.message-content {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 12px;
  line-height: 1.5;
}

.recommendation-card {
  background: #e9ecef;
  border-radius: 12px;
  padding: 16px;
}

.product {
  font-weight: bold;
  color: #2c3e50;
}

.reason {
  color: #42b983;
  font-weight: 500;
}

.details {
  color: #666;
  font-size: 0.95em;
}
</style>
