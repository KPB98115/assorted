<template>
    <div v-if="isOpen" class="confirm-overlay" @click.self="handleCancel">
        <div class="confirm-dialog">
            <h3 class="confirm-title">{{ title }}</h3>
            <p class="confirm-message">{{ message }}</p>
            <div class="confirm-actions">
                <button class="btn-cancel" @click="handleCancel">Cancel</button>
                <button class="btn-confirm" @click="handleConfirm">{{ confirmText }}</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
    title: {
        type: String,
        default: 'Confirm'
    },
    message: {
        type: String,
        required: true
    },
    confirmText: {
        type: String,
        default: 'Delete'
    }
})

const emit = defineEmits(['confirm', 'cancel'])

const isOpen = ref(true)

const handleConfirm = () => {
    emit('confirm')
    isOpen.value = false
}

const handleCancel = () => {
    emit('cancel')
    isOpen.value = false
}
</script>

<style scoped>
.confirm-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2000;
}

.confirm-dialog {
    background: white;
    border-radius: 12px;
    padding: 24px;
    max-width: 400px;
    width: 90%;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.confirm-title {
    margin: 0 0 12px 0;
    font-size: 1.25rem;
    font-weight: 600;
    color: #333;
}

.confirm-message {
    margin: 0 0 24px 0;
    color: #666;
    line-height: 1.5;
}

.confirm-actions {
    display: flex;
    gap: 12px;
    justify-content: flex-end;
}

.btn-cancel,
.btn-confirm {
    padding: 8px 16px;
    border-radius: 6px;
    border: none;
    font-size: 0.9rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}

.btn-cancel {
    background: #f5f5f5;
    color: #666;
}

.btn-cancel:hover {
    background: #e0e0e0;
}

.btn-confirm {
    background: #f44336;
    color: white;
}

.btn-confirm:hover {
    background: #d32f2f;
}
</style>
