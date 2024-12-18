<template>
    <div class="article-update">
      <div v-if="loading" class="loading">
        데이터를 불러오는 중...
      </div>
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
  
      <div v-if="article && !loading" class="article-content">
        <form @submit.prevent="updateArticle" class="update-form">
          <div class="form-group">
            <label for="title">제목</label>
            <input
              id="title"
              v-model="article.title"
              type="text"
              required
            />
          </div>
  
          <div class="form-group">
            <label for="description">내용</label>
            <textarea
              id="description"
              v-model="article.description"
              required
            ></textarea>
          </div>
  
          <div class="form-group">
            <label for="image">이미지</label>
            <input
              id="image"
              type="file"
              @change="handleImageChange"
              accept="image/*"
            />
          </div>
  
          <div class="button-group">
            <button type="submit" class="update-button">수정하기</button>
            <RouterLink :to="`/articles/${article.id}`">
              <button type="button" class="cancel-button">취소</button>
            </RouterLink>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  import articlesAPI from '../apis/articlesAPI';
  import { useAuthStore } from '@/stores/auth';
  
  export default {
    name: 'ArticleUpdate',
    setup() {
      const router = useRouter();
      const route = useRoute();
      const article = ref({});
      const loading = ref(false);
      const error = ref(null);
      const authStore = useAuthStore() 
  
      const fetchArticle = async () => {
        try {
          loading.value = true;
          article.value = await articlesAPI.getArticle(route.params.articleId);
        } catch (err) {
          error.value = '게시글을 불러오는 데 실패했습니다.';
          console.error('게시글 로딩 에러:', err);
        } finally {
          loading.value = false;
        }
      };
  
      const updateArticle = async () => {
        try {
          loading.value = true;
          await articlesAPI.updateArticle(route.params.articleId, article.value);
          router.push(`/articles/${route.params.articleId}`); // 수정 완료 후 게시글 상세로 이동
        } catch (err) {
          error.value = '게시글 수정에 실패했습니다.';
          console.error('게시글 수정 에러:', err);
        } finally {
          loading.value = false;
        }
      };
  
      const handleImageChange = (event) => {
        const file = event.target.files[0];
        if (file) {
          article.value.image = file;
        } 
      };
  
      onMounted(fetchArticle);
  
      return {
        article,
        loading,
        error,
        authStore,
        updateArticle,
        handleImageChange
      };
    }
  };
  </script>
  
  <style scoped>
  .article-update {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .update-form {
    background-color: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
  }
  
  .form-group input[type='text'],
  .form-group textarea {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .form-group textarea {
    min-height: 200px;
  }
  
  .button-group {
    display: flex;
    gap: 10px;
    justify-content: flex-end;
  }
  
  .update-button,
  .cancel-button {
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
  
  .update-button {
  background-color: #0061f2c0; /* 토스 느낌의 파란색 */
  color: white;
  }
  
  .cancel-button {
    background-color: #72b8e7; /* 채도가 낮고 깊이가 있는 빨간색 */
    color: white;
  }
  
  .update-button:hover {
    background-color: #033888c0;
  }
  
  .cancel-button:hover {
    background-color: #406883
  }
  
  .loading {
    text-align: center;
    padding: 20px;
  }
  
  .error-message {
    color: #dc3545;
    text-align: center;
    padding: 20px;
  }
  </style>
  