import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'Square', component: () => import('../views/Square.vue') },
  { path: '/chat/:id', name: 'Chat', component: () => import('../views/Chat.vue'), meta: { requiresAuth: true } },
  { path: '/friends', name: 'Friends', component: () => import('../views/Friends.vue'), meta: { requiresAuth: true } },
  { path: '/create', name: 'Create', component: () => import('../views/Create.vue'), meta: { requiresAuth: true } },
  { path: '/profile', name: 'Profile', component: () => import('../views/Profile.vue'), meta: { requiresAuth: true } },
  { path: '/login', name: 'Login', component: () => import('../views/Login.vue') },
  { path: '/register', name: 'Register', component: () => import('../views/Register.vue') },
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('access_token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
