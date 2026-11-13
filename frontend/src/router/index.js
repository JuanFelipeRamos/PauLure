import { createRouter, createWebHistory } from 'vue-router'
import LoginAdmin from '@/views/LoginAdmin.vue'
import HomeView from '../views/HomeView.vue'
import NavbarComponent from '../components/NavbarComponent.vue'
import FooterComponent from '@/components/FooterComponent.vue'

import HomePanelAdmin from '@/views/HomePanelAdmin.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login-admin',
      name: 'loginadmin',
      component: LoginAdmin,
    },
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },

    {
      path: '/navbar',
      name: 'navbar',
      component: NavbarComponent
    },

    {
      path: '/footer',
      name: 'footer',
      component: FooterComponent
    },

    {
      path: '/homepaneladmin',
      name: 'homepaneladmin',
      component: HomePanelAdmin
    },
  ],
})

export default router
