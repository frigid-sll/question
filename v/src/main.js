// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
Vue.prototype.axios=axios


Vue.config.productionTip = false


var whittelist = ['/login','/register']
router.beforeEach((to, from, next) => {
  let account = window.localStorage.getItem('account');
  if (account || whittelist.indexOf(to.path) > -1) {
    next()
  }
  else {
    next('/login')
  }
})


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
