<template>
  <div class="article-detail">
    <div v-if="loading" class="loading">
      데이터를 불러오는 중...
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-if="article && !loading" class="article-content">
      <div class="article-header">
        <h1>{{ article.title }}</h1>
        <div v-if="isArticleAuthor" class="article-admin-actions">
          <button @click="editArticle" class="edit-button">수정</button>
          <button @click="deleteArticle" class="delete-button">삭제</button>
        </div>
      </div>
      <div class="article-meta">
        <span>작성자: {{ article.author }}</span>
        <span>작성일: {{ formatDate(article.created_at) }}</span>
      </div>
      
      <div class="article-body">
        <p>{{ article.description }}</p>
        <img v-if="article.image" :src="article.image" alt="게시글 이미지" />
      </div>

      <div class="article-actions">
        <button @click="handleLike" :class="{ active: isLiked }" class="action-button">
          👍 좋아요 ({{ article.liked_users?.length || 0 }})
        </button>
        <button @click="handleDislike" :class="{ active: isDisliked }" class="action-button">
          👎 싫어요 ({{ article.disliked_users?.length || 0 }})
        </button>
      </div>

      <!-- 댓글 섹션 -->
      <div class="comments-section">
        <h2>댓글</h2>
        <form @submit.prevent="submitComment" class="comment-form">
          <textarea 
            v-model="newComment" 
            placeholder="댓글을 입력하세요"
            required
          ></textarea>
          <button type="submit" :disabled="!newComment.trim()">댓글 작성</button>
        </form>

        <div class="comments-list">
          <div v-for="comment in comments" :key="comment.id" class="comment">
            <div class="comment-header">
              <span class="comment-author">{{ comment.user }}</span>
              <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
            </div>
            <p class="comment-content">{{ comment.content }}</p>
            <div v-if="isCommentAuthor(comment)" class="comment-actions">
              <button @click="deleteComment(comment.id)" class="delete-button">삭제</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import articlesAPI from '../apis/articlesAPI'
import { format } from 'date-fns'
import { useAuthStore } from '../stores/auth'   

export default {
  name: 'ArticleDetailView',
  props: {
    articleId: {
      type: String,
      required: true
    }
  },

  setup(props) {
    const router = useRouter()
    const authStore = useAuthStore()
    const article = ref(null)
    const comments = ref([])
    const newComment = ref('')
    const loading = ref(false)
    const error = ref(null)

    const fetchArticle = async () => {
      try {
        loading.value = true
        article.value = await articlesAPI.getArticle(props.articleId)

        await fetchComments()
      } catch (error) {
        error.value = '게시글을 불러오는 데 실패했습니다.'
        console.error('게시글 로딩 에러:', error)
      } finally {
        loading.value = false
      }
    }

    const fetchComments = async () => {
      try {
        const response = await articlesAPI.getArticle(props.articleId)
        comments.value = response.comment_set
      } catch (error) {
        console.error('댓글 로딩 에러:', error)
      }
    }

    const handleLike = async () => {
      try {
        await articlesAPI.likeArticle(props.articleId)
        await fetchArticle()
      } catch (error) {
        console.error('좋아요 에러:', error)
      }
    }

    const handleDislike = async () => {
      try {
        await articlesAPI.dislikeArticle(props.articleId)
        await fetchArticle()
      } catch (error) {
        console.error('싫어요 에러:', error)
      }
    }

    const submitComment = async () => {
      try {
        await articlesAPI.createComment(props.articleId, { content: newComment.value })
        newComment.value = ''
        await fetchComments()
      } catch (error) {
        console.error('댓글 작성 에러:', error)
      }
    }

    const deleteComment = async (commentId) => {
      try {
        await articlesAPI.deleteComment(props.articleId, commentId)
        await fetchComments()
      } catch (error) {
        console.error('댓글 삭제 에러:', error)
      }
    }

    const formatDate = (date) => {
      return format(new Date(date), 'yyyy-MM-dd HH:mm')
    }

    const isCommentAuthor = (comment) => {
      console.log('Comment user ID:', comment.user)
      console.log('Current user ID:', authStore.user?.id)
      return String(comment.user) === String(authStore.user?.id)
    }

    const isArticleAuthor = computed(() => {
      console.log('Article data:', article.value)
      console.log('Current user ID:', authStore.user?.id)
      console.log('Article author ID:', article.value?.author)
      
      return String(article.value?.author) === String(authStore.user?.id)
    })

    const deleteArticle = async () => {
      if (confirm('정말로 이 게시글을 삭제하시겠습니까?')) {
        try {
          await articlesAPI.deleteArticle(props.articleId)
          router.push('/articles') // 삭제 후 목록으로 이동
        } catch (error) {
          console.error('게시글 삭제 에러:', error)
        }
      }
    }

    const editArticle = () => {
      router.push(`/articles/${props.articleId}/edit`)
    }

    const isLiked = computed(() => {
      return article.value?.liked_users?.includes(authStore.username)
    })

    const isDisliked = computed(() => {
      return article.value?.disliked_users?.includes(authStore.username)
    })

    onMounted(fetchArticle)

    return {
      article,
      comments,
      newComment,
      loading,
      error,
      handleLike,
      handleDislike,
      submitComment,
      deleteComment,
      formatDate,
      isCommentAuthor,
      isArticleAuthor,
      deleteArticle,
      editArticle,
      isLiked,
      isDisliked
    }
  }
}
</script>

<style scoped>
.article-detail {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.article-content {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.article-meta {
  color: #666;
  margin-bottom: 20px;
  display: flex;
  gap: 20px;
}

.article-actions {
  margin: 20px 0;
  display: flex;
  gap: 10px;
}

.action-button {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
}

.action-button.active {
  background-color: #2D60FF;
  color: white;
  border-color: #2D60FF;
}

.comments-section {
  margin-top: 40px;
}

.comment-form {
  margin-bottom: 20px;
}

.comment-form textarea {
  width: 100%;
  min-height: 80px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 10px;
}

.comment {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 10px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  color: #666;
}

.delete-button {
  color: #dc3545;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 0.9em;
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

.article-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.article-admin-actions {
  display: flex;
  gap: 10px;
}

.edit-button, .delete-button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.edit-button {
  background-color: #28a745;
  color: white;
}

.delete-button {
  background-color: #dc3545;
  color: white;
}

.edit-button:hover {
  background-color: #218838;
}

.delete-button:hover {
  background-color: #c82333;
}
</style>
