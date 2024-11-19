import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useKakao } from 'vue3-kakao-maps/@utils';

useKakao('37f9b8f93858026c0c87a81348ccf644');


const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')


