import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import ListView from '../views/ListView.vue';
import LoginView from '../views/LoginView.vue';
import outputType2 from '../views/ouputType2.vue';
import outputType3 from '../views/outputType3.vue';
import registerModule from '../views/registerModule.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/list',
      name: 'list',
      component: ListView
    },
    {
      path: '/auth',
      name: 'auht',
      component: LoginView
    },
    {
      path: '/output2/:out2Code',
      name: 'outputType2',
      component: outputType2
    },
    {
      path: '/output3/:out3Code',
      name: 'outputType3',
      component: outputType3
    },
    {
      path: '/registerModule',
      name: 'registerModule',
      component: registerModule
    }
  ]
})

export default router
