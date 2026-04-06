import { createRouter, createWebHistory } from 'vue-router'
import GreatCircleMap from '../views/GreatCircleMap.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: GreatCircleMap,
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      // component: () => import('@/views/GreatCircleMap.vue'),
    },
  ],
})

export default router
