<template>
  <div style="display: flex; justify-content: center; align-items: center; min-height: calc(100vh - 64px);">
    <n-card title="登录" style="width: 400px;">
      <n-form :model="form" :rules="rules" @submit.prevent="handleLogin">
        <n-form-item label="用户名/邮箱" path="email">
          <n-input v-model:value="form.email" placeholder="请输入用户名或邮箱" />
        </n-form-item>
        <n-form-item label="密码" path="password">
          <n-input v-model:value="form.password" type="password" placeholder="请输入密码" />
        </n-form-item>
        <n-button type="primary" block attr-type="submit" :loading="loading">登录</n-button>
      </n-form>
      <div style="text-align: center; margin-top: 16px;">
        <n-text depth="3">还没有账号？</n-text>
        <n-button text @click="router.push('/register')">立即注册</n-button>
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

const form = ref({ email: '', password: '' })
const rules = {
  email: [{ required: true, message: '请输入用户名或邮箱' }],
  password: [{ required: true, message: '请输入密码' }],
}

async function handleLogin() {
  loading.value = true
  try {
    await auth.login(form.value.email, form.value.password)
    message.success('登录成功')
    router.push('/')
  } catch (err: any) {
    message.error(err.response?.data?.detail || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>
