<template>
  <n-message-provider>
    <n-notification-provider>
      <NavBar />
      <main style="min-height: calc(100vh - 64px); padding-top: 64px;">
        <router-view />
      </main>
    </n-notification-provider>
  </n-message-provider>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from './stores/auth'
import NavBar from './components/NavBar.vue'
import { NMessageProvider, NNotificationProvider } from 'naive-ui'

const auth = useAuthStore()
onMounted(() => {
  if (auth.isAuthenticated) {
    auth.fetchProfile()
  }
})
</script>
