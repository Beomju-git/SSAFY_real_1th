import axios from 'axios'

const API_URL = 'http://localhost:8000/banking/articles/';  // 장고 서버 URL 실제배포라면 이거 다 바꿔줘야함

const articlesAPI = {
    getArticles: async () => {
        const response = await axios.get(API_URL);
        return response.data;
    },
    createArticle: async (articleData) => {
        const response = await axios.post(API_URL, articleData);
        return response.data;
    },
    getArticle: async (id) => {
        const response = await axios.get(`${API_URL}${id}/`);
        return response.data;
    },
    updateArticle: async (id, articleData) => {
        const response = await axios.put(`${API_URL}${id}/`, articleData);
        return response.data;
    },
    deleteArticle: async (id) => {
        await axios.delete(`${API_URL}${id}/`);
    },
    likeArticle: async (articleId) => {
        await axios.post(`${API_URL}${articleId}/like/`);
    },
    dislikeArticle: async (articleId) => {
        await axios.post(`${API_URL}${articleId}/dislike/`);
    }
};

export default articlesAPI;