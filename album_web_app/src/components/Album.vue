<template>
    <div class="modal-overlay" @click.self="close">
        <div class="modal-container">
            <div class="modal-header">
                <h2>{{ props.album.name }}</h2>
                <div class="header-actions">
                    <input
                        type="file"
                        ref="fileInput"
                        accept="image/jpeg,image/png,image/webp,image/heif,image/heic,image/avif"
                        multiple
                        @change="handleFileSelect"
                        style="display: none"
                    />
                    <button class="upload-btn" @click="$refs.fileInput.click()">
                        Upload Images
                    </button>
                    <button class="close-btn" @click="close">✕</button>
                </div>
            </div>

            <div v-if="imageList.length === 0 && uploadingImages.length === 0" class="empty-state">
                <p>No images in this album yet</p>
                <button class="upload-btn-large" @click="$refs.fileInput.click()">
                    Upload Your First Image
                </button>
            </div>

            <div v-else class="album-container">
                <div
                    class="image-wrapper"
                    v-for="(img, index) in imageList"
                    :key="img.imageId"
                >
                    <img
                        :src="img.thumbnailUrl"
                        :alt="`Image ${index + 1}`"
                        @click="openImageViewer(img)"
                        class="thumbnail-image"
                    />
                    <button
                        class="delete-image-btn"
                        @click.stop="handleDeleteImage(img)"
                        title="Delete image"
                    >
                        ✕
                    </button>
                </div>
                <div
                    class="image-wrapper uploading-placeholder"
                    v-for="placeholder in uploadingImages"
                    :key="placeholder.tempId"
                >
                    <div class="uploading-content">
                        uploading...
                    </div>
                </div>
            </div>

            <ImageViewer
                v-if="selectedImage"
                :album-id="props.album.id"
                :image="selectedImage"
                @close="selectedImage = null"
            />

            <ConfirmDialog
                v-if="confirmDelete"
                :title="'Delete Image'"
                :message="'Are you sure you want to delete this image? This action cannot be undone.'"
                @confirm="confirmDeleteImage"
                @cancel="cancelDeleteImage"
            />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import ImageViewer from './ImageViewer.vue';
import ConfirmDialog from './ConfirmDialog.vue';
import { imageAPI, albumAPI } from '../services/api.js';

const props = defineProps({
    album: {
        type: Object,
        required: true,
    },
});

const emit = defineEmits(['close']);

const imageList = ref([]);
const selectedImage = ref(null);
const fileInput = ref(null);
const confirmDelete = ref(false);
const imageToDelete = ref(null);
const uploadingImages = ref([]);

onMounted(async () => {
    await loadAlbumImages();
});

const loadAlbumImages = async () => {
    try {
        const albumData = await albumAPI.getAlbum(props.album.id);
        const albumContentList = albumData.content.content
        if (albumContentList && albumContentList.length === 0) {
            imageList.value = [];
            return;
        }

        const loadedImages = [];
        for (let i = 0; i < albumContentList.length; i++) {
            const imageId = albumContentList[i].image_id;
            const thumbnailId = albumContentList[i].image_id;

            try {
                const thumbnailUrl = await imageAPI.getThumbnail(thumbnailId);
                loadedImages.push({
                    imageId,
                    thumbnailId,
                    thumbnailUrl,
                });
            } catch (error) {
                console.error(`Failed to load thumbnail for image ${imageId}:`, error);
            }
        }

        imageList.value = loadedImages;
    } catch (error) {
        console.error(error);
    }
};

const handleFileSelect = async (event) => {
    const files = Array.from(event.target.files);
    if (files.length === 0) return;

    try {
        for (const file of files) {
            await uploadImage(file);
        }
    } catch (error) {
        console.error(error);
    } finally {
        // Reset file input
        event.target.value = '';
    }
};

const uploadImage = async (file) => {
    const tempId = `temp-${Date.now()}-${Math.random()}`;

    // Add placeholder immediately
    uploadingImages.value.push({ tempId, fileName: file.name });

    try {
        // Upload the image
        const { job_id } = await imageAPI.uploadImage(props.album.id, file);

        // Wait for job to complete
        const result = await imageAPI.waitForJob(job_id);

        // Add the new image to the list
        // const thumbnailUrl = await imageAPI.getThumbnail(result.thumbnailId);
        // imageList.value.push({
        //     imageId: result.mainImageId,
        //     thumbnailId: result.thumbnailId,
        //     thumbnailUrl,
        // });
        await loadAlbumImages()
    } catch (error) {
        console.error('Upload error:', error);
        throw error;
    } finally {
        // Remove placeholder
        uploadingImages.value = uploadingImages.value.filter(
            (placeholder) => placeholder.tempId !== tempId
        );
    }
};

const openImageViewer = (img) => {
    selectedImage.value = img;
};

const handleDeleteImage = (img) => {
    imageToDelete.value = img;
    confirmDelete.value = true;
};

const confirmDeleteImage = async () => {
    try {
        await imageAPI.deleteImage(props.album.id, imageToDelete.value.imageId);

        // Remove from local list
        imageList.value = imageList.value.filter(
            (img) => img.imageId !== imageToDelete.value.imageId
        );
    } catch (error) {
        console.error(error);
    } finally {
        confirmDelete.value = false;
        imageToDelete.value = null;
    }
};

const cancelDeleteImage = () => {
    confirmDelete.value = false;
    imageToDelete.value = null;
};

const close = () => {
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
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 20px;
}

.modal-container {
    background: white;
    border-radius: 16px;
    width: 100%;
    max-width: 1200px;
    max-height: 90vh;
    display: flex;
    flex-direction: column;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 24px;
    border-bottom: 1px solid #e0e0e0;
}

.modal-header h2 {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 600;
    color: #333;
}

.header-actions {
    display: flex;
    gap: 12px;
    align-items: center;
}

.upload-btn {
    padding: 10px 20px;
    background: #4a90e2;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}

.upload-btn:hover {
    background: #357abd;
}

.close-btn {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: none;
    background: #f5f5f5;
    color: #666;
    font-size: 1.5rem;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
}

.close-btn:hover {
    background: #e0e0e0;
}

.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 80px 24px;
    color: #999;
}

.empty-state p {
    font-size: 1.1rem;
    margin-bottom: 24px;
}

.upload-btn-large {
    padding: 14px 32px;
    background: #4a90e2;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}

.upload-btn-large:hover {
    background: #357abd;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(74, 144, 226, 0.4);
}

.album-container {
    flex: 1;
    overflow-y: auto;
    padding: 24px;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 16px;
    align-content: start;
}

.image-wrapper {
    position: relative;
    aspect-ratio: 1;
    border-radius: 8px;
    overflow: hidden;
    background: #f5f5f5;
    cursor: pointer;
    transition: all 0.2s;
}

.image-wrapper:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.thumbnail-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.delete-image-btn {
    position: absolute;
    top: 8px;
    right: 8px;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    border: none;
    background: rgba(244, 67, 54, 0.9);
    color: white;
    font-size: 1rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: all 0.2s;
    padding: 0;
}

.image-wrapper:hover .delete-image-btn {
    opacity: 1;
}

.delete-image-btn:hover {
    background: #d32f2f;
    transform: scale(1.1);
}

.uploading-placeholder {
    background: #e0e0e0;
    cursor: default;
}

.uploading-placeholder:hover {
    transform: none;
    box-shadow: none;
}

.uploading-content {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #666;
    font-size: 0.9rem;
}

/* Tablet and below */
@media (max-width: 768px) {
    .modal-overlay {
        padding: 16px;
    }

    .modal-container {
        max-height: 92vh;
    }

    .modal-header {
        padding: 20px;
    }

    .modal-header h2 {
        font-size: 1.3rem;
    }

    .album-container {
        padding: 20px;
        grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
        gap: 12px;
    }

    .upload-btn {
        padding: 9px 16px;
        font-size: 0.9rem;
    }

    .empty-state {
        padding: 60px 20px;
    }

    .empty-state p {
        font-size: 1rem;
    }
}

/* Mobile devices */
@media (max-width: 480px) {
    .modal-overlay {
        padding: 12px;
    }

    .modal-container {
        max-height: 94vh;
        border-radius: 12px;
    }

    .modal-header {
        flex-direction: column;
        gap: 12px;
        align-items: stretch;
        padding: 16px;
    }

    .modal-header h2 {
        font-size: 1.2rem;
    }

    .header-actions {
        justify-content: space-between;
    }

    .upload-btn {
        padding: 10px 18px;
        font-size: 0.9rem;
        flex: 1;
    }

    .close-btn {
        width: 40px;
        height: 40px;
        font-size: 1.4rem;
    }

    .album-container {
        padding: 16px;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
    }

    .delete-image-btn {
        opacity: 1;
        width: 26px;
        height: 26px;
        top: 6px;
        right: 6px;
        font-size: 0.95rem;
    }

    .empty-state {
        padding: 50px 16px;
    }

    .empty-state p {
        font-size: 0.95rem;
        margin-bottom: 20px;
    }

    .upload-btn-large {
        padding: 12px 28px;
        font-size: 0.95rem;
    }

    .uploading-content {
        font-size: 0.85rem;
    }
}

/* Small mobile devices */
@media (max-width: 375px) {
    .modal-overlay {
        padding: 8px;
    }

    .modal-header {
        padding: 14px;
    }

    .modal-header h2 {
        font-size: 1.1rem;
    }

    .album-container {
        padding: 12px;
        gap: 6px;
    }

    .upload-btn {
        font-size: 0.85rem;
        padding: 9px 14px;
    }

    .close-btn {
        width: 36px;
        height: 36px;
    }
}
</style>
