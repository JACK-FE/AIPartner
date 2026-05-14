<template>
  <n-layout-header bordered style="position: fixed; top: 0; left: 0; right: 0; z-index: 100; background: #fff; height: 64px; display: flex; align-items: center; padding: 0 24px;">
    <div style="display: flex; align-items: center; gap: 32px; width: 100%; max-width: 1200px; margin: 0 auto;">
      <router-link to="/" style="font-size: 20px; font-weight: 700; color: #18a058;">AI Partner</router-link>
      <n-space v-if="auth.isAuthenticated" style="flex: 1;">
        <n-button text :type="route.name === 'Square' ? 'primary' : 'default'" @click="router.push('/')">广场</n-button>
        <n-button text :type="route.name === 'Friends' ? 'primary' : 'default'" @click="router.push('/friends')">好友</n-button>
        <n-button text :type="route.name === 'Create' ? 'primary' : 'default'" @click="router.push('/create')">创作</n-button>
      </n-space>
      <div style="flex: 1;" v-else />
      <div style="display: flex; align-items: center; gap: 12px;">
        <template v-if="auth.isAuthenticated && auth.user">
          <n-button text @click="router.push('/profile')">
            <n-avatar :src="auth.user.avatar" size="small" :fallback-src="`https://api.dicebear.com/9.x/avataaars/svg?seed=${auth.user.email}`" />
          </n-button>
          <n-button @click="auth.logout(); router.push('/login')" size="small" secondary>退出</n-button>
        </template>
        <template v-else>
          <n-button @click="router.push('/login')" size="small" secondary>登录</n-button>
          <n-button @click="router.push('/register')" size="small" type="primary">注册</n-button>
        </template>
      </div>
    </div>
  </n-layout-header>
</template>

<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { NLayoutHeader, NSpace, NButton, NAvatar } from 'naive-ui'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
</script>
