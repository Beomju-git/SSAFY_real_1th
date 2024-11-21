import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const API_URL = 'http://localhost:8000/banking/articles/';  // 장고 서버 URL 실제배포라면 이거 다 바꿔줘야함

const articlesAPI = {
    base_URL:'http://localhost:8000/',
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
        const authStore = useAuthStore();
        console.log(articleData)
        // FormData 객체 생성
        const formData = new FormData();
        
        // title과 description을 formData에 추가
        formData.append('title', articleData.title);
        formData.append('description', articleData.description);
        
        // image가 있을 때만 formData에 추가
        if (articleData.image instanceof File) {
            formData.append('image', articleData.image);
        } 
    
        try {
            const { data } = await axios.put(`${API_URL}${id}/`, formData, {
                headers: {
                    'Authorization': `Token ${authStore.token}`,
                }
            });
            return data; // 요청 성공 시 서버에서 반환된 데이터 반환
        } catch (err) {
            console.error('게시글 수정 에러:', err);
            throw err; // 에러를 던져서 상위에서 처리할 수 있게 함
        }
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
    updateComment: async (articleId, commentId, content) => {
        const authStore = useAuthStore();
        return await axios.put(`${API_URL}${articleId}/comments/${commentId}/`,content, {
            headers: {
                'Authorization': `Token ${authStore.token}`
            }
        });
    },
};

export default articlesAPI;