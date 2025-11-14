import axios from 'axios';

// Use relative URL - Vite proxy will forward to backend
const API_BASE_URL = '';

// Create axios instance with default config
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Album API endpoints
export const albumAPI = {
    // Get all albums
    async getAllAlbums() {
        const response = await apiClient.post('/api/album/getAll');
        console.log("Get All Albums response:", response.data);
        return response.data;
    },

    // Get single album by ID
    async getAlbum(albumId) {
        console.log("getAlbum called with ID:", albumId, "Type:", typeof albumId);
        try {
            const response = await apiClient.post('/api/album/get', { id: albumId });
            console.log("Get Album response:", response.data);
            return response.data;
        } catch (error) {
            console.error("getAlbum error:", error.response?.data || error.message);
            throw error;
        }
    },

    // Create new album
    async createAlbum(name) {
        try {
            const response = await apiClient.post('/api/album/create', { name });
            console.log("Create album: ", response)
            return response.data;
        } catch (error) {
            console.error(error)
        }
    },

    // Delete album
    async deleteAlbum(albumId) {
        try {
            const response = await apiClient.post('/api/album/delete', { id: albumId });
            console.log("Delete album: ", response)
            return response.data;
        } catch (error) {
            console.log(error)
        }
    },
};

// Image API endpoints
export const imageAPI = {
    // Upload image
    async uploadImage(albumId, file, onProgress) {
        try {
            const formData = new FormData();
            formData.append('album_id', albumId);
            formData.append('image', file);
    
            const response = await axios.post(
                `${API_BASE_URL}/api/album/image/upload`,
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                    onUploadProgress: onProgress,
                }
            );
            console.log("Upload image: ", response)
            return response.data.content;
        } catch (error) {
            console.log(error)
        }
    },

    // Get job status
    async getJobStatus(jobId) {
        try {
            const response = await axios.get(`${API_BASE_URL}/api/album/image/job/${jobId}`);
            console.log("Get job status: ", response.data)
            return response.data.content;
        } catch(error) {
            console.log(error)
        }
    },

    // Delete job
    async deleteJob(jobId) {
        try {
            const response = await axios.delete(`${API_BASE_URL}/api/album/image/job/${jobId}`);
            console.log("Delete job: ", response)
            return response.data;
        } catch (error) {
            console.error(error)
        }
    },

    // Poll job until completion
    async waitForJob(jobId, onProgress, pollInterval = 2000) {
        while (true) {
            const status = await this.getJobStatus(jobId);

            if (onProgress) onProgress(status);
            
            if (status.overall_status === 'SUCCESS') {
                await this.deleteJob(jobId);
                return {
                    mainImageId: status.main_image.gridfs_id,
                    thumbnailId: status.thumbnail.gridfs_id,
                };
            } else if (status.overall_status === 'FAILED') {
                await this.deleteJob(jobId);
                throw new Error(status.main_image.error_message || 'Upload failed');
            }

            await new Promise((resolve) => setTimeout(resolve, pollInterval));
        }
    },

    // Get full-size image
    async getImage(albumId, imageId) {
        try {
            const response = await axios.post(
                `${API_BASE_URL}/api/album/image/get`,
                { album_id: albumId, image_id: imageId },
                { responseType: 'blob' }
            );
            console.log("Get Image: ", response)
            return URL.createObjectURL(response.data);
        } catch (error) {
            console.error(error)
        }
    },

    // Get thumbnail
    async getThumbnail(thumbnailId) {
        try {
            const response = await axios.post(
                `${API_BASE_URL}/api/album/image/thumbnail/get`,
                { thumbnail_id: thumbnailId },
                { responseType: 'blob' }
            );
            console.log("Get Thumbnail: ", response)
            return URL.createObjectURL(response.data);
        } catch (error) {
            console.error(error)
        }
    },

    // Delete image
    async deleteImage(albumId, imageId) {
        try {
            const response = await apiClient.post('/api/album/image/delete', {
                album_id: albumId,
                image_id: imageId,
            });
            console.log("Delete image: ", response)
            return response.data;
        } catch (error) {
            console.error(error)
        }
    },
};
