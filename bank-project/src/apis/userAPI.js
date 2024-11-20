import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const API_URL = 'http://localhost:8000/';

const userAPI = {
    getUserProfile: async (username) => {
        const authStore = useAuthStore()
        const userResponse = await axios.get(`${API_URL}accounts/user/`, {
            headers: {
                'Authorization': `Token ${authStore.token}`
            }
        })
        const userId = userResponse.data.pk
        
        const { data } = await axios.get(`${API_URL}profile/${userId}/detail/`, {
            headers: {
                'Authorization': `Token ${authStore.token}`
            }
        })
        return data
    },



    updateUserProfile: async (userId, profileData) => {
        const authStore = useAuthStore()
        const { data } = await axios.put(`${API_URL}profile/${userId}/detail/`, profileData, {
            headers: {
                'Authorization': `Token ${authStore.token}`
            }
        })
        return data
    }
}

export default userAPI