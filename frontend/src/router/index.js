import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import NavbarComponent from '../components/NavbarComponent.vue'
import FooterComponent from '@/components/FooterComponent.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
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
  ],
})

export default router
