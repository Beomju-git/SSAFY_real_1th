<!-- views/ArticleView.vue -->
<template>
  <div class="article-container">
    <h1>게시글 목록</h1>
    
    <div v-if="loading" class="loading">
      데이터를 불러오는 중...
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-if="!loading && !error" class="article-list">
      <div v-for="article in articles" :key="article.id" class="article-card">
        <router-link :to="`/articles/${article.id}`" class="article-link">
          <h2 class="article-title">{{ article.title }}</h2>
          <p class="article-meta">
            <span class="article-author">작성자: {{ article.author }}</span>
            <span class="article-date">등록일: {{ formatDate(article.created_at) }}</span>
          </p>
        </router-link>
        <button 
          v-if="isAuthor(article.author)" 
          @click="deleteArticle(article.id)" 
          class="delete-button"
        >
          삭제
        </button>
      </div>
    </div>

    <button @click="createArticle" class="create-button">
      새 게시글 작성
    </button>

    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>새 게시글 작성</h2>
          <button class="close-button" @click="closeModal">&times;</button>
        </div>
        
        <form @submit.prevent="submitArticle">
          <div class="form-group">
            <label for="title">제목</label>
            <input 
              id="title"
              v-model="newArticle.title"
              type="text"
              required
              placeholder="제목을 입력하세요"
            >
          </div>
          
          <div class="form-group">
            <label for="description">내용</label>
            <textarea
              id="description"
              v-model="newArticle.description"
              required
              placeholder="내용을 입력하세요"
              rows="5"
            ></textarea>
          </div>

          <div class="form-group">
            <label for="image">이미지 업로드</label>
            <input 
              id="image"
              type="file"
              @change="onFileChange"
            />
          </div>

          <div class="button-group">
            <button type="button" @click="closeModal" class="cancel-button">
              취소
            </button>
            <button type="submit" :disabled="loading" class="submit-button">
              {{ loading ? '작성 중...' : '작성하기' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import articlesAPI from '../apis/articlesAPI'
import { format } from 'date-fns'

export default {
  name: 'ArticleView',
  
  data() {
    return {
      articles: [],
      showModal: false,
      newArticle: {
        title: '',
        description: '',
        image: null
      },
      loading: false,
      error: null
    }
  },

  async created() {
    await this.fetchArticles()
  },

  methods: {
    async fetchArticles() {
      try {
        this.loading = true
        this.error = null
        this.articles = await articlesAPI.getArticles()
      } catch (error) {
        this.error = '게시글을 불러오는데 실패했습니다'
        console.error('게시글 로딩 에러:', error)
      } finally {
        this.loading = false
      }
    },

    createArticle() {
      this.showModal = true
    },

    closeModal() {
      this.showModal = false
      this.resetForm()
    },

    resetForm() {
      this.newArticle = {
        title: '',
        description: '',
        image: null
      }
    },

    onFileChange(event) {
      const file = event.target.files[0]
      this.newArticle.image = file
    },

    async submitArticle() {
      if (!this.newArticle.title || !this.newArticle.description) {
        this.error = '모든 필드를 입력해주세요'
        return
      }

      const formData = new FormData()
      formData.append('title', this.newArticle.title)
      formData.append('description', this.newArticle.description)
      if (this.newArticle.image) {
        formData.append('image', this.newArticle.image)
      }

      try {
        this.loading = true
        this.error = null
        await articlesAPI.createArticle(formData)
        await this.fetchArticles()
        this.closeModal()
      } catch (error) {
        this.error = '게시글 작성에 실패했습니다'
        console.error('게시글 작성 에러:', error)
      } finally {
        this.loading = false
      }
    },

    formatDate(date) {
      return format(new Date(date), 'yyyy-MM-dd HH:mm')
    },

    isAuthor(author) {
      // 현재 사용자와 게시글/댓글 작성자를 비교하는 로직을 구현해야 합니다.
      // 여기서는 간단하게 작성자 이름을 비교합니다.
      return this.currentUser === author
    },

    deleteArticle(id) {
      // 게시글 삭제 로직을 구현해야 합니다.
      // 여기서는 간단하게 게시글 ID를 콘솔에 출력합니다.
      console.log(`게시글 ${id}를 삭제했습니다.`)
    }
  }
}
</script>

<style scoped>
.article-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  color: #333;
  margin-bottom: 30px;
  text-align: center;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #666;
}

.error-message {
  background-color: #fff3f3;
  color: #dc3545;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 20px;
  text-align: center;
}

.article-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.article-card {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.article-card:hover {
  transform: scale(1.02);
}

.article-link {
  text-decoration: none;
  color: #333;
}

.article-title {
  font-size: 1.2rem;
  margin: 0;
}

.article-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

.article-author {
  color: #888;
  font-size: 0.9rem;
}

.article-date {
  color: #888;
  font-size: 0.9rem;
}

.create-button {
  margin-top: 20px;
  width: 100%;
  padding: 12px;
  background-color: #2D60FF;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.create-button:hover {
  background-color: #1a45d1;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 25px;
  border-radius: 8px;
  width: 500px;
  max-width: 90%;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #333;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #2D60FF;
  box-shadow: 0 0 0 2px rgba(45, 96, 255, 0.1);
}

.button-group {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
}

.button-group button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.cancel-button {
  background-color: #f8f9fa;
  color: #333;
}

.submit-button {
  background-color: #2D60FF;
  color: white;
}

.submit-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

@media (max-width: 600px) {
  .modal-content {
    width: 95%;
    margin: 10px;
    padding: 15px;
  }

  .button-group {
    flex-direction: column;
  }

  .button-group button {
    width: 100%;
  }
}
</style>