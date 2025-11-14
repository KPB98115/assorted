<template>
    <div class="modal-overlay" @click.self="close">
        <div class="modal-container">
            <button class="close-btn" @click="close">✕</button>
            <div class="image-container">
                <img v-if="imageUrl" :src="imageUrl" :alt="'Full size image'" class="full-image" />
                <div v-else class="loading-placeholder">Loading image...</div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { imageAPI } from '../services/api.js';

const props = defineProps({
    albumId: {
        type: String,
        required: true,
    },
    image: {
        type: Object,
        required: true,
    },
});

const emit = defineEmits(['close']);

const imageUrl = ref(null);

onMounted(async () => {
    await loadFullImage();
});

const loadFullImage = async () => {
    try {
        const url = await imageAPI.getImage(props.albumId, props.image.imageId);
        imageUrl.value = url;
    } catch (error) {
        console.error('Failed to load full image:', error);
    }
};

const close = () => {
    // Clean up object URL to prevent memory leaks
    if (imageUrl.value) {
        URL.revokeObjectURL(imageUrl.value);
    }
    emit('close');
};
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.95);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1500;
    padding: 20px;
}

.modal-container {
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.close-btn {
    position: absolute;
    top: 20px;
    right: 20px;
    width: 48px;
    height: 48px;
    border-radius: 50%;
    border: none;
    background: rgba(255, 255, 255, 0.9);
    color: #333;
    font-size: 1.8rem;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    z-index: 10;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.close-btn:hover {
    background: white;
    transform: scale(1.1);
}

.image-container {
    max-width: 100%;
    max-height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.full-image {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    border-radius: 8px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
}

.loading-placeholder {
    color: white;
    font-size: 1.2rem;
    padding: 40px;
}

@media (max-width: 768px) {
    .close-btn {
        top: 10px;
        right: 10px;
        width: 40px;
        height: 40px;
        font-size: 1.5rem;
    }
}
</style>
