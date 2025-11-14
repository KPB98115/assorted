import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useIndexStore = defineStore('index', () => {
    const isLoading = ref(false)

    return {
        isLoading,
    }
})