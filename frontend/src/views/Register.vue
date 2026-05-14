<template>
  <div style="display: flex; justify-content: center; align-items: center; min-height: calc(100vh - 64px);">
    <n-card title="注册" style="width: 400px;">
      <n-form :model="form" :rules="rules" @submit.prevent="handleRegister">
        <n-form-item label="用户名" path="username">
          <n-input v-model:value="form.username" placeholder="请输入用户名" />
        </n-form-item>
        <n-form-item label="邮箱" path="email">
          <n-input v-model:value="form.email" placeholder="请输入邮箱" />
        </n-form-item>
        <n-form-item label="密码" path="password">
          <n-input v-model:value="form.password" type="password" placeholder="至少6位密码" />
        </n-form-item>
        <n-button type="primary" block attr-type="submit" :loading="loading">注册</n-button>
      </n-form>
      <div style="text-align: center; margin-top: 16px;">
        <n-text depth="3">已有账号？</n-text>
        <n-button text @click="router.push('/login')">立即登录</n-button>
      </div>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { NCard, NForm, NFormItem, NInput, NButton, NText, useMessage } from 'naive-ui'

const router = useRouter()
const auth = useAuthStore()
const message = useMessage()
const loading = ref(false)

const form = ref({ username: '', email: '', password: '' })
const rules = {
  username: [{ required: true, message: '请输入用户名' }],
  email: [{ required: true, message: '请输入邮箱' }],
  password: [{ required: true, min: 6, message: '密码至少6位' }],
}

async function handleRegister() {
  loading.value = true
  try {
    await auth.register(form.value.username, form.value.email, form.value.password)
    message.success('注册成功')
    router.push('/')
  } catch (err: any) {
    const data = err.response?.data
    const msg = data?.username?.[0] || data?.email?.[0] || data?.password?.[0] || '注册失败'
    message.error(msg)
  } finally {
    loading.value = false
  }
}
</script>
