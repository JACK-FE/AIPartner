<template>
  <div style="max-width: 600px; margin: 0 auto; padding: 24px;">
    <n-h2>个人中心</n-h2>
    <n-card>
      <div style="display: flex; flex-direction: column; align-items: center; gap: 16px; margin-bottom: 24px;">
        <div style="position: relative; cursor: pointer;" @click="triggerAvatarUpload">
          <n-avatar :src="auth.user?.avatar" :size="96" :fallback-src="`https://api.dicebear.com/9.x/avataaars/svg?seed=${auth.user?.email}`" />
          <div style="position: absolute; bottom: 0; right: 0; background: #18a058; border-radius: 50%; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; border: 2px solid #fff;">
            <n-icon size="16" color="#fff"><CameraOutline /></n-icon>
          </div>
        </div>
        <input ref="fileInput" type="file" accept="image/*" style="display: none" @change="uploadAvatar" />
        <div style="font-size: 20px; font-weight: 600;">{{ auth.user?.username }}</div>
        <div style="color: #999;">{{ auth.user?.email }}</div>
        <n-text depth="3">{{ auth.user?.bio || '这个人很懒，什么都没写' }}</n-text>
      </div>

      <n-divider />

      <n-form :model="editForm" @submit.prevent="handleUpdate">
        <n-form-item label="用户名">
          <n-input v-model:value="editForm.username" />
        </n-form-item>
        <n-form-item label="个人简介">
          <n-input v-model:value="editForm.bio" type="textarea" :rows="3" />
        </n-form-item>
        <n-button type="primary" attr-type="submit" :loading="saving" block>保存修改</n-button>
      </n-form>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useCharacterStore } from '../stores/character'
import client from '../api/client'
import { NCard, NH2, NAvatar, NIcon, NText, NForm, NFormItem, NInput, NButton, NDivider, useMessage } from 'naive-ui'
import { CameraOutline } from '@vicons/ionicons5'

const auth = useAuthStore()
const store = useCharacterStore()
const message = useMessage()
const saving = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)
const uploading = ref(false)

const editForm = ref({ username: '', bio: '' })

function triggerAvatarUpload() {
  fileInput.value?.click()
}

async function uploadAvatar(e: Event) {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  uploading.value = true
  try {
    const formData = new FormData()
    formData.append('avatar', file)
    const { data } = await client.post('/auth/avatar/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    if (auth.user) {
      auth.user.avatar = data.avatar
    }
    message.success('头像上传成功')
  } catch {
    message.error('头像上传失败')
  } finally {
    uploading.value = false
    input.value = ''
  }
}

onMounted(() => {
  if (auth.user) {
    editForm.value.username = auth.user.username
    editForm.value.bio = auth.user.bio
  }
  store.fetchMine()
})

async function handleUpdate() {
  saving.value = true
  try {
    await auth.updateProfile(editForm.value)
    message.success('保存成功')
  } catch (err: any) {
    message.error(err.response?.data?.username?.[0] || '保存失败')
  } finally {
    saving.value = false
  }
}
</script>
