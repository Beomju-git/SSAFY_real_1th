import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const API_URL = 'http://localhost:8000/banking/articles/';  // 장고 서버 URL 실제배포라면 이거 다 바꿔줘야함

const articlesAPI = {
    getArticles: async () => {
        const { data } = await axios.get(API_URL);
        return data;
    },
    createArticle: async (formData) => {
        const authStore = useAuthStore()
        return await axios.post(API_URL, formData, {
            headers: {
                'Authorization': `Token ${authStore.token}`,
                'Content-Type': 'multipart/form-data'
            }
        })
    },
    getArticle: async (id) => {
        const { data } = await axios.get(`${API_URL}${id}/`);
        return data;
    },
    updateArticle: async (id, articleData) => {
        const { data } = await axios.put(`${API_URL}${id}/`, articleData);
        return data;
    },
    deleteArticle: async (id) => {
        const authStore = useAuthStore()
        await axios.delete(`${API_URL}${id}/`, {
            headers: {
                'Authorization': `Token ${authStore.token}`
            }
        });
    },
    likeArticle: async (articleId) => {
        const authStore = useAuthStore();
        await axios.post(`${API_URL}${articleId}/like/`, {}, {
            headers: {
                'Authorization': `Token ${authStore.token}`
            }
        });
    },
    dislikeArticle: async (articleId) => {
        const authStore = useAuthStore();
        await axios.post(`${API_URL}${articleId}/dislike/`, {}, {
            headers: {
                'Authorization': `Token ${authStore.token}`
            }
        });
    },
    getComments: async (articleId) => {
        const { data } = await axios.get(`${API_URL}${articleId}/comments/`);
        return data;
    },
    createComment: async (articleId, commentData) => {
        const authStore = useAuthStore();
        return await axios.post(`${API_URL}${articleId}/comments/`, commentData, {
            headers: {
                'Authorization': `Token ${authStore.token}`,
                'Content-Type': 'application/json'
            }
        });
    },
    deleteComment: async (articleId, commentId) => {
        const authStore = useAuthStore();
        return await axios.delete(`${API_URL}${articleId}/comments/${commentId}/`, {
            headers: {
                'Authorization': `Token ${authStore.token}`
            }
        });
    },
};

export default articlesAPI;