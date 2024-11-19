<template>
    <nav class="navigation-bar">
        <div class="nav-container">
            <div class="logo">
                <router-link to="/">JuukJuuk</router-link>
            </div>
            <button class="hamburger" @click="toggleMenu">
                <span class="bar"></span>
                <span class="bar"></span>
                <span class="bar"></span>
            </button>
            <div class="nav-links" :class="{ 'active': isMenuOpen }">
                <router-link to="/" class="nav-link">홈</router-link>
                <router-link to="/exchange" class="nav-link">환율 계산</router-link>
                <router-link to="/nearby-banks" class="nav-link">주변 은행</router-link>
                <router-link to="/articles" class="nav-link">커뮤니티</router-link>
                <router-link to="/product-recommendation" class="nav-link">금융 상품 추천</router-link>
                <button 
                    @click="openLoginModal" 
                    class="login-button"
                    @mouseenter="isHovered = true"
                    @mouseleave="isHovered = false"
                >
                    <div class="button-background"></div>
                    <span class="button-text">로그인</span>
                </button>
            </div>
        </div>
        <LoginModal :isVisible="isLoginModalVisible" :closeModal="closeLoginModal" />
    </nav>
    <div class="nav-spacer"></div>
</template>

<script setup>
import { ref } from 'vue'
import LoginModal from './LoginModal.vue'

const isLoginModalVisible = ref(false)
const isHovered = ref(false)
const isMenuOpen = ref(false)

const openLoginModal = () => {
    isLoginModalVisible.value = true
}

const closeLoginModal = () => {
    isLoginModalVisible.value = false
}

const toggleMenu = () => {
    isMenuOpen.value = !isMenuOpen.value
}
</script>

<style scoped>
.navigation-bar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background-color: white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    z-index: 1000;
}

.nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    height: 56px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo a {
    color: #2D60FF;
    font-size: 1.25rem;
    font-weight: bold;
    text-decoration: none;
}

.hamburger {
    display: none; /* Hide by default */
    flex-direction: column;
    cursor: pointer;
}

.bar {
    height: 3px;
    width: 25px;
    background-color: #2D60FF;
    margin: 3px 0;
    transition: 0.3s;
}

.nav-links {
    display: flex;
    gap: 24px;
    align-items: center;
}

.nav-links.active {
    display: flex; /* Show when active */
}

.nav-link {
    color: #666;
    text-decoration: none;
    font-size: 0.95rem;
    padding: 8px 12px;
    position: relative;
    transition: color 0.2s;
}

.nav-link:hover {
    color: #2D60FF;
}

.nav-link.router-link-active {
    color: #2D60FF;
}

.nav-link.router-link-active::after {
    content: '';
    position: absolute;
    bottom: -17px;
    left: 0;
    width: 100%;
    height: 2px;
    background-color: #2D60FF;
}

/* 토스 스타일 로그인 버튼 */
.login-button {
    position: relative;
    background-color: #2D60FF;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    overflow: hidden;
    transition: transform 0.2s ease;
}

.button-background {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(
        120deg,
        transparent 0%,
        transparent 40%,
        rgba(255, 255, 255, 0.2) 50%,
        transparent 60%,
        transparent 100%
    );
    background-size: 200% 100%;
    background-position: 100% 0;
    transition: background-position 0.5s ease;
}

.login-button:hover .button-background {
    background-position: -100% 0;
}

.button-text {
    position: relative;
    z-index: 1;
}

.login-button:hover {
    background-color: #1E4AD6;
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(45, 96, 255, 0.25);
}

.login-button:active {
    transform: translateY(1px);
    box-shadow: 0 1px 4px rgba(45, 96, 255, 0.2);
}

.nav-spacer {
    height: 56px;
}

/* Responsive Styles */
@media (max-width: 768px) {
    .hamburger {
        display: flex; /* Show hamburger on mobile */
    }

    .nav-links {
        display: none; /* Hide links by default on mobile */
        flex-direction: column;
        width: 100%;
        background-color: white;
        position: absolute;
        top: 56px; /* Below the navbar */
        left: 0;
        z-index: 999;
    }

    .nav-links.active {
        display: flex; /* Show links when active */
    }

    .nav-link {
        padding: 10px;
        width: 100%;
        text-align: center;
    }

    .login-button {
        width: 100%;
        margin-top: 10px;
    }
}
</style>