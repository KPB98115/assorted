<template>
    <div class="modal-overlay" @click.self="close(false)">
        <div class="modal-container">
            <div class="modal-header">
                <h2>Create New Album</h2>
            </div>
            <div class="modal-content">
                <label for="album-name">Album Name:</label>
                <input
                    id="album-name"
                    type="text"
                    v-model="name"
                    @keyup.enter="close(true)"
                    placeholder="Enter album name..."
                    autofocus
                />
            </div>
            <div class="modal-footer">
                <button class="btn-secondary" @click="close(false)">Cancel</button>
                <button class="btn-primary" @click="close(true)">Create</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useIndexStore } from '../store/index';

const emit = defineEmits(['close']);

const indexStore = useIndexStore();
const name = ref('');

const close = (withValue) => {
    if (withValue) {
        if (name.value.trim() === '') {
            indexStore.openPopup('Error', 'Album name cannot be empty.');
            return;
        }
        emit('close', name.value.trim());
        return;
    }
    emit('close', false);
};
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal-container {
    background: white;
    border-radius: 12px;
    width: 90%;
    max-width: 450px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.modal-header {
    padding: 24px 24px 16px 24px;
    border-bottom: 1px solid #e0e0e0;
}

.modal-header h2 {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 600;
    color: #333;
}

.modal-content {
    padding: 24px;
}

.modal-content label {
    display: block;
    margin-bottom: 8px;
    font-weight: 500;
    color: #555;
    font-size: 0.95rem;
}

.modal-content input {
    width: 100%;
    padding: 12px;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.2s;
    box-sizing: border-box;
}

.modal-content input:focus {
    outline: none;
    border-color: #4a90e2;
}

.modal-footer {
    padding: 16px 24px 24px 24px;
    display: flex;
    gap: 12px;
    justify-content: flex-end;
}

.btn-primary,
.btn-secondary {
    padding: 10px 24px;
    border-radius: 8px;
    border: none;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}

.btn-primary {
    background: #4a90e2;
    color: white;
}

.btn-primary:hover {
    background: #357abd;
}

.btn-secondary {
    background: #f5f5f5;
    color: #666;
}

.btn-secondary:hover {
    background: #e0e0e0;
}
</style>
