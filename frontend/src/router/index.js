import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import ListView from '../views/ListView.vue';
import LoginView from '../views/LoginView.vue';
import outputType2 from '../views/ouputType2.vue';
import outputType3 from '../views/outputType3.vue';
import registerModule from '../views/registerModule.vue';
import admin from '../views/Admin.vue';
import editRule from '../views/EditRule.vue';
import addToken from '../views/AddToken.vue';
import tokenList from '../views/TokenList.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/:out1Code',
      name: 'home',
      component: HomeView
    },
    { 
      path: '/', 
      redirect: '/defult' 
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
    },
    {
      path: '/admin',
      name: 'admin',
      component: admin
    },
    {
      path: '/editRule/:editID',
      name: 'editRule',
      component: editRule
    },
    {
      path: '/addToken',
      name: 'addToken',
      component: addToken
    },
    {
      path: '/tokenList',
      name: 'tokenList',
      component: tokenList
    }
  ]
})

export default router
