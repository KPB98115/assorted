<template>
    <div class="gallery-container">
        <div class="gallery-header">
            <h1>My Albums</h1>
            <button class="add-album-btn" @click="isInputModalOpen = true">
                <span class="btn-icon">+</span> New Album
            </button>
        </div>

        <div class="gallery-grid">
            <div class="gallery-item" v-for="album in gallery" :key="album.id">
                <div class="album-card" @click="openAlbum(album)">
                    <div class="album-icon">
                        <img
                            v-if="album.content && album.content.length > 0"
                            src="/folder-filled.svg"
                            alt="album-icon"
                        />
                        <img
                            v-else
                            src="/folder-empty.svg"
                            alt="empty-album-icon"
                        />
                    </div>
                    <div class="album-info">
                        <h3 class="album-name">{{ album.name }}</h3>
                        <p class="album-count">
                            {{ album.content ? album.content.length : 0 }}
                            {{ album.content && album.content.length === 1 ? 'image' : 'images' }}
                        </p>
                    </div>
                    <button
                        class="delete-album-btn"
                        @click.stop="handleDeleteAlbum(album)"
                        title="Delete album"
                    >
                        ✕
                    </button>
                </div>
            </div>
        </div>

        <InputModal
            v-if="isInputModalOpen"
            @close="handleInputModalClose"
        />

        <Album
            v-if="isAlbumOpen && selectedAlbum"
            :album="selectedAlbum"
            @close="handleAlbumClose"
        />

        <ConfirmDialog
            v-if="confirmDelete"
            :title="'Delete Album'"
            :message="`Are you sure you want to delete '${albumToDelete?.name}'? This will delete all images in the album.`"
            @confirm="confirmDeleteAlbum"
            @cancel="cancelDeleteAlbum"
        />
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Album from './Album.vue';
import InputModal from './InputModal.vue';
import ConfirmDialog from './ConfirmDialog.vue';
import { albumAPI } from '../services/api.js';

const gallery = ref([]);
const isAlbumOpen = ref(false);
const isInputModalOpen = ref(false);
const selectedAlbum = ref(null);
const confirmDelete = ref(false);
const albumToDelete = ref(null);

onMounted(async () => {
    await getAlbumList();
});

const getAlbumList = async () => {
    try {
        const albums = await albumAPI.getAllAlbums();
        gallery.value = albums.content;
    } catch (error) {
        console.error(error);
    }
};

const openAlbum = (album) => {
    selectedAlbum.value = album;
    isAlbumOpen.value = true;
};

const handleAlbumClose = async () => {
    isAlbumOpen.value = false;
    selectedAlbum.value = null;
    // Refresh album list to get updated image counts
    await getAlbumList();
};

const handleInputModalClose = async (name) => {
    if (name && name.length > 0) {
        await handleCreateAlbum(name);
    }
    isInputModalOpen.value = false;
};

const handleCreateAlbum = async (name) => {
    try {
        await albumAPI.createAlbum(name);
        await getAlbumList();
    } catch (error) {
        console.error(error);
    }
};

const handleDeleteAlbum = (album) => {
    albumToDelete.value = album;
    confirmDelete.value = true;
};

const confirmDeleteAlbum = async () => {
    try {
        await albumAPI.deleteAlbum(albumToDelete.value.id);
        await getAlbumList();
    } catch (error) {
        console.error(error);
    } finally {
        confirmDelete.value = false;
        albumToDelete.value = null;
    }
};

const cancelDeleteAlbum = () => {
    confirmDelete.value = false;
    albumToDelete.value = null;
};
</script>

<style scoped>
.gallery-container {
    width: 100%;
    max-width: 95vw;
    margin: 0 auto;
    padding: 24px;
}

.gallery-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 32px;
}

.gallery-header h1 {
    margin: 0;
    font-size: 2rem;
    font-weight: 600;
    color: #333;
}

.add-album-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 24px;
    background: #4a90e2;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    box-shadow: 0 2px 8px rgba(74, 144, 226, 0.3);
}

.add-album-btn:hover {
    background: #357abd;
    box-shadow: 0 4px 12px rgba(74, 144, 226, 0.4);
    transform: translateY(-1px);
}

.btn-icon {
    font-size: 1.25rem;
    font-weight: 300;
}

.gallery-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 24px;
}

.gallery-item {
    position: relative;
}

.album-card {
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transition: all 0.3s;
    cursor: pointer;
    position: relative;
}

.album-card:hover {
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    transform: translateY(-4px);
}

.album-icon {
    width: 100%;
    height: 140px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 16px;
    background: #f8f9fa;
    border-radius: 8px;
}

.album-icon img {
    width: 80px;
    height: 80px;
}

.album-info {
    text-align: center;
}

.album-name {
    margin: 0 0 8px 0;
    font-size: 1.1rem;
    font-weight: 600;
    color: #333;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.album-count {
    margin: 0;
    font-size: 0.9rem;
    color: #666;
}

.delete-album-btn {
    position: absolute;
    top: 12px;
    right: 12px;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    border: none;
    background: rgba(244, 67, 54, 0.9);
    color: white;
    font-size: 1.2rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: all 0.2s;
    padding: 0;
}

.album-card:hover .delete-album-btn {
    opacity: 1;
}

.delete-album-btn:hover {
    background: #d32f2f;
    transform: scale(1.1);
}

@media (max-width: 768px) {
    .gallery-header {
        width: 90%;
        gap: 16px;
        align-items: stretch;
    }

    .gallery-grid {
        grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
        gap: 16px;
        width: 90%;
    }

    .delete-album-btn {
        opacity: 1;
    }
}
</style>
