<template>
  <div style="max-width: 800px; margin: 0 auto; padding: 24px;">
    <n-h2>我创建的AI好友</n-h2>

    <div v-if="store.myCharacters.length || true" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px;">
      <n-card hoverable @click="showCreateModal = true" style="cursor: pointer; min-height: 220px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <div style="display: flex; flex-direction: column; align-items: center; gap: 8px; padding: 24px 0;">
          <n-icon size="48" color="#18a058"><AddOutline /></n-icon>
          <div style="font-weight: 600; color: #18a058;">创建AI好友</div>
        </div>
      </n-card>

      <n-card v-for="c in store.myCharacters" :key="c.id" hoverable @click="router.push(`/chat/${c.id}`)" style="cursor: pointer;">
        <template #cover>
          <div style="display: flex; justify-content: center; padding: 12px;">
            <n-avatar :src="c.avatar" :size="64" />
          </div>
        </template>
        <div style="text-align: center; font-weight: 500;">{{ c.name }}</div>
        <template #footer>
          <div style="display: flex; gap: 8px; justify-content: center;">
            <n-button size="tiny" @click.stop="editCharacter(c)">编辑</n-button>
            <n-button size="tiny" type="error" @click.stop="deleteCharacter(c.id)">删除</n-button>
          </div>
        </template>
      </n-card>
    </div>

    <n-empty v-if="!store.myCharacters.length" description="还没有创建过AI好友，点击上方卡片开始创建吧" />

    <n-modal v-model:show="showCreateModal" :mask-closable="false" preset="card" title="创建AI好友" style="width: 520px;">
      <n-form :model="form" :rules="rules" @submit.prevent="handleCreate">
        <n-form-item label="头像" path="avatar">
          <div style="display: flex; flex-direction: column; gap: 12px; width: 100%;">
            <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
              <n-avatar v-for="a in avatars" :key="a" :src="a" :size="44" :style="{ cursor: 'pointer', border: form.avatar === a && !customAvatarPreview ? '3px solid #18a058' : '3px solid transparent', borderRadius: '8px' }" @click="customAvatarPreview = ''; form.avatar = a" />
            </div>
            <n-divider style="margin: 0;" />
            <div style="display: flex; align-items: center; gap: 12px;">
              <div v-if="customAvatarPreview" style="position: relative;">
                <n-avatar :src="customAvatarPreview" :size="60" style="border-radius: 8px;" />
                <div style="position: absolute; top: -6px; right: -6px; background: #e74c3c; border-radius: 50%; width: 18px; height: 18px; display: flex; align-items: center; justify-content: center; cursor: pointer; border: 2px solid #fff;" @click="customAvatarPreview = ''; form.avatar = avatars[0]">
                  <n-icon size="12" color="#fff"><CloseOutline /></n-icon>
                </div>
              </div>
              <n-button size="small" @click="triggerCharAvatarUpload" :type="customAvatarPreview ? 'primary' : 'default'">
                <template #icon><n-icon><CloudUploadOutline /></n-icon></template>
                {{ customAvatarPreview ? '更换图片' : '上传自定义头像' }}
              </n-button>
              <input ref="charAvatarInput" type="file" accept="image/*" style="display: none" @change="onCharAvatarUpload" />
            </div>
          </div>
        </n-form-item>
        <n-form-item label="名称" path="name">
          <n-input v-model:value="form.name" placeholder="给AI好友起个名字" />
        </n-form-item>
        <n-form-item label="简介" path="description">
          <n-input v-model:value="form.description" type="textarea" :rows="2" placeholder="简短介绍" />
        </n-form-item>
        <n-form-item label="性格描述" path="personality">
          <n-input v-model:value="form.personality" type="textarea" :rows="3" placeholder="描述性格特点，如：温柔知性，喜欢用温暖的语气鼓励人" />
        </n-form-item>
        <n-form-item label="模型" path="model">
          <n-select v-model:value="form.model" :options="modelOptions" placeholder="选择模型" />
        </n-form-item>
        <n-form-item label="公开">
          <n-switch v-model:value="form.is_public" />
          <n-text style="margin-left: 8px;" depth="3">{{ form.is_public ? '公开 - 所有人可见' : '私密 - 仅自己可见' }}</n-text>
        </n-form-item>
        <div style="display: flex; gap: 12px; justify-content: flex-end;">
          <n-button @click="showCreateModal = false">取消</n-button>
          <n-button type="primary" attr-type="submit" :loading="creating">创建</n-button>
        </div>
      </n-form>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCharacterStore } from '../stores/character'
import { charactersApi } from '../api/characters'
import client from '../api/client'

import type { AICharacter } from '../types'
import { NCard, NH2, NModal, NForm, NFormItem, NInput, NSelect, NSwitch, NButton, NAvatar, NIcon, NText, NDivider, NEmpty, useMessage } from 'naive-ui'
import { AddOutline, CloudUploadOutline, CloseOutline } from '@vicons/ionicons5'

const router = useRouter()
const store = useCharacterStore()
const message = useMessage()
const creating = ref(false)
const showCreateModal = ref(false)

const charAvatarInput = ref<HTMLInputElement | null>(null)
const customAvatarPreview = ref('')

const avatars = [
  'https://api.dicebear.com/9.x/bottts/svg?seed=friend1',
  'https://api.dicebear.com/9.x/bottts/svg?seed=friend2',
  'https://api.dicebear.com/9.x/bottts/svg?seed=friend3',
  'https://api.dicebear.com/9.x/bottts/svg?seed=friend4',
  'https://api.dicebear.com/9.x/bottts/svg?seed=helper1',
  'https://api.dicebear.com/9.x/bottts/svg?seed=helper2',
  'https://api.dicebear.com/9.x/icons/svg?seed=star',
  'https://api.dicebear.com/9.x/icons/svg?seed=heart',
  'https://api.dicebear.com/9.x/icons/svg?seed=smile',
  'https://api.dicebear.com/9.x/icons/svg?seed=rocket',
]

const form = ref({
  name: '',
  avatar: avatars[0],
  description: '',
  personality: '',
  model: null as number | null,
  is_public: true,
})

const rules = {
  name: [{ required: true, message: '请输入名称' }],
  model: [{ required: true, message: '请选择模型', type: 'number' as const }],
}

const modelOptions = computed(() => store.models.map(m => ({ label: `${m.provider} / ${m.model_name}`, value: m.id })))

function triggerCharAvatarUpload() {
  charAvatarInput.value?.click()
}

async function onCharAvatarUpload(e: Event) {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = () => {
    customAvatarPreview.value = reader.result as string
    form.value.avatar = reader.result as string
  }
  reader.readAsDataURL(file)
  input.value = ''
}

async function handleCreate() {
  creating.value = true
  try {
    let avatarUrl = form.value.avatar
    if (avatarUrl.startsWith('data:')) {
      const resp = await fetch(avatarUrl)
      const blob = await resp.blob()
      const formData = new FormData()
      formData.append('avatar', blob, 'avatar.png')
      const { data } = await client.post('/characters/avatar/upload/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      avatarUrl = data.avatar
    }
    await charactersApi.create({ ...form.value, avatar: avatarUrl } as any)
    message.success('创建成功')
    showCreateModal.value = false
    form.value = { name: '', avatar: avatars[0], description: '', personality: '', model: null, is_public: true }
    customAvatarPreview.value = ''
    await store.fetchMine()
  } catch (err: any) {
    message.error(err.response?.data?.name?.[0] || '创建失败')
  } finally {
    creating.value = false
  }
}

async function deleteCharacter(id: number) {
  try {
    await charactersApi.delete(id)
    message.success('已删除')
    await store.fetchMine()
  } catch {
    message.error('删除失败')
  }
}

function editCharacter(c: AICharacter) {
  showCreateModal.value = true
  form.value = {
    name: c.name,
    avatar: c.avatar || avatars[0],
    description: c.description || '',
    personality: c.personality || '',
    model: null,
    is_public: c.is_public,
  }
  message.info('编辑功能可复用创建表单，当前仅预填数据')
}

onMounted(async () => {
  await Promise.all([store.fetchModels(), store.fetchMine()])
})
</script>
