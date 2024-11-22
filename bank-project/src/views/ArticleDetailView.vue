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
        <span>작성자: {{ article.author.username }}</span>
        <span>작성일: {{ formatDate(article.created_at) }}</span>
      </div>

      <div class="article-body">
        <p>{{ article.description }}</p>
        <img v-if="article.image" :src="`${baseUrl}${article.image}`" alt="게시글 이미지" />
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
        <div class="comment-input">
          <form @submit.prevent="submitComment" class="comment-form">
            <textarea v-model="newComment" placeholder="댓글을 입력하세요" required></textarea>
            <button class='comment-button' type="submit" :disabled="!newComment.trim()">댓글 작성</button>
          </form>
        </div>

        <div class="comments-list">
          <div v-for="comment in comments" :key="comment.id" class="comment">
            <div v-if="isUpdated && comment.id === editingCommentId"> 
              <div class="comment-header">
                <span class="comment-author">작성자 :{{ comment.user.username }}</span>
              </div>
              <div class="comment-form">
              <textarea v-model="editedCommentContent" placeholder="댓글 수정" ></textarea>
            </div>
              <div class="comment-actions">
                <button @click="saveCommentEdit(comment.id)" class="save-button">수정 저장</button>
                <button @click="cancelEdit" class="cancel-button">수정 취소</button>
              </div>
            </div>
            <div v-else>
              <div class="comment-header">
                <span class="comment-author">작성자 :{{ comment.user.username }} /</span>
                <span class="comment-date"> 작성일 : {{ formatDate(comment.created_at) }}</span>
              </div>
              <p class="comment-content">{{ comment.content }}</p>
              <div v-if="isCommentAuthor(comment)" class="comment-actions">
                <button @click="editComment(comment.id, comment.content)" class="edit-button">수정</button>
                <button @click="deleteComment(comment.id)" class="delete-button">삭제</button>
              </div>
              <hr>
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
    const baseUrl = articlesAPI.base_URL
    const editedCommentContent = ref('')
    const isUpdated = ref(true)
    const editingCommentId = ref(null)

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

    const editComment = async (commentId, content) => {
      try {
        await articlesAPI.updateComment(props.articleId, commentId, content)
        await fetchComments()
      } catch (error) {
        console.error('댓글 수정 에러:', error)
      }
      editingCommentId.value = commentId
      editedCommentContent.value = content
    }

    const cancelEdit = () => {
      editingCommentId.value = null
      editedCommentContent.value = ''
    }

    const saveCommentEdit = async (commentId) => {
      try {
        await articlesAPI.updateComment(props.articleId, commentId, { content: editedCommentContent.value })
        await fetchComments()
        cancelEdit()
      } catch (error) {
        console.error('댓글 수정 에러:', error)
      }
    }

    const formatDate = (date) => {
      return format(new Date(date), 'yyyy-MM-dd HH:mm')
    }

    const isCommentAuthor = (comment) => {
      return String(comment.user.id) === String(authStore.user?.id)
    }

    const isArticleAuthor = computed(() => {
      return String(article.value.author.id) === String(authStore.user?.id)
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
      baseUrl,
      article,
      comments,
      newComment,
      editedCommentContent,
      loading,
      error,
      handleLike,
      handleDislike,
      submitComment,
      deleteComment,
      editComment,
      cancelEdit,
      saveCommentEdit,
      formatDate,
      isCommentAuthor,
      isUpdated,
      isArticleAuthor,
      editingCommentId,
      deleteArticle,
      editArticle,
      isLiked,
      isDisliked,
      authStore
    }
  }
}
</script>

<style scoped>
.article-detail {
  max-width: 40%;
  margin: 0 auto;
  padding: 20px;
  padding-bottom: 130px;
  background-color: #f9f9f9;
}

.article-content {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.article-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.article-header h1 {
  margin: 0;
  font-size: 2em;
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
  justify-content: center; /* 버튼을 가로로 가운데 정렬 */
  position: relative;
}

.action-button {
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  border: none;
  background-color: transparent; /* 배경색 없애기 */
  color: inherit; /* 부모의 텍스트 색상 상속 */
}

.action-button:hover {
  background-color: #ebebeb;
  border-radius: 10px;
}

.action-button.active {
  background-color: #007bff;
  color: white;
}

.comment-form {
  margin-bottom: 20px;
}

.comment-form textarea {
  width: 98%; /* 부모 요소의 너비에 맞게 설정 */
  height: auto; /* 고정된 높이 설정 */
  resize: none; /* 크기 조절을 비활성화 */
  padding: 10px; /* 여백 설정 */
  margin-right: 10px;
  border: 1px solid #ccc; /* 테두리 설정 */
  border-radius: 5px; /* 둥근 테두리 설정 */
  font-size: 14px; /* 글자 크기 설정 */
}

.comment-actions {
  margin-top: 10px;
  text-align: right; /* 버튼을 우측 정렬 */
}

.comment-actions button {
  padding: 5px 10px;
  cursor: pointer;
  display: inline-block; /* 버튼들을 가로로 배치 */
}

.article-admin-actions .edit-button,
.comment-actions .save-button,
.comment-actions .edit-button {
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

.article-admin-actions .delete-button,
.comment-actions .delete-button,
.comment-actions .cancel-button {
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

.comment-button {
  background-color: #95a5a6; /* 부드럽고 자연스러운 회색 톤 */
  color: rgb(29, 29, 29);
  border: none;
  margin-right: 10px;
  border-radius: 50px; /* 더 둥근 모서리 */
  padding: 6px 14px; /* 여백을 적당히 줄여서 크기 작게 */
  font-size: 14px; /* 글씨 크기 */
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 부드러운 그림자 효과 */
  transition: all 0.3s ease; /* 모든 속성에 부드러운 전환 효과 */
}

.comment-button:hover {
  background-color: #6e7a7a; 
}

.edit-button:hover,
.save-button:hover
 {
    background-color: #033888c0;
  }
  
  .cancel-button:hover,
  .delete-button:hover {
    background-color: #406883
  }
  
  .article-body{
    width: 80%; /* 가로 폭을 부모 요소에 맞게 100%로 설정 */
    height: auto; /* 세로는 자동으로 비율을 맞추어 크기 조정 */
  }
  .comment-header {
  font-weight: bold; /* 글씨를 볼드체로 설정 */
}

</style>
