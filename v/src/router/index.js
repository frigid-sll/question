import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import login from '@/components/login'
import register from '@/components/register'
import catalogue from '@/components/catalogue'
import question from '@/components/question'
import root from '@/components/root'
import download_local from '@/components/download_local'
import t from '@/components/t'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/login',
      name: 'login',
      component: login
    },
    {
      path: '/register',
      name: 'register',
      component: register
    },
    {
      path: '/catalogue',
      name: 'catalogue',
      component: catalogue
    },
    {
      path: '/question',
      name: 'question',
      component: question
    },
    {
      path: '/root',
      name: 'root',
      component: root
    },
    {
      path: '/download_local',
      name: 'download_local',
      component: download_local
    },
    {
      path: '/t',
      name: 't',
      component: t
    }
  ]
})
