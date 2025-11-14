<template>
    <div v-if="isLoading" class="loading-overlay">
        <div class="loading-spinner">
            <div class="spinner"></div>
            <p>Loading...</p>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';
import { useIndexStore } from '../store/index';

const indexStore = useIndexStore();

const isLoading = computed(() => indexStore.isLoading);
</script>

<style scoped>
.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255, 255, 255, 0.9);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
}

.loading-spinner {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
}

.spinner {
    width: 50px;
    height: 50px;
    border: 4px solid #e0e0e0;
    border-top: 4px solid #4a90e2;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
}

.loading-spinner p {
    margin: 0;
    font-size: 1rem;
    color: #666;
    font-weight: 500;
}
</style>
