// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App'
import router from './router'
import echarts from 'echarts'
import bmap from 'vue-baidu-map'
import './assets/normalize.css'
import store from './store/store'
import axios from 'axios'




// var axios = require('axios')
// 配置公共url
axios.defaults.baseURL = 'https://l4159b2312.imdo.co'

Vue.prototype.$axios = axios
Vue.prototype.$echarts = echarts
Vue.config.productionTip = false


Vue.use(bmap,{
  ak : 'ybm7GO5cyZOsVS80dLuzBCKi306RfUrz'
})
Vue.use(ElementUI)
Vue.config.productionTip = false

router.beforeEach((to, from, next) => {
  // if (to.meta.requireAuth) {
  //   if (JSON.parse(localStorage.getItem("islogin"))) {
  //     next();
  //   } else {
  //     next({
  //       path: "/"//指向为你的登录界面
  //     });
  //   }
  // } else {
  //   next();
  // }

  if (to.fullPath === "/") {
    if (JSON.parse(localStorage.getItem("islogin"))) {
      next({
        path: from.fullPath
      });
    } else {
      next();
    }
  }

  if(to.matched.some(m => m.meta.requireAuth)){  // 权限验证
    if(window.localStorage.token && window.localStorage.isLogin === '1'){
      next()
    }else if(to.path !== '/login' && to.path !== '/faceRecognition' && to.path !== '/register'){
      let token = window.localStorage.token;
      if(token === 'null' || token === '' || token === undefined){
        next({path:'/login'})
        alert("您还未登录，请先登陆后在进行操作！")
      }else{
        next()
      }
    }else{   // 不需要登录
      next()
    }
  }

});

// 添加请求拦截器
axios.interceptors.request.use(
  config => {
    if(store.state.token){
      config.headers.common['token'] = store.state.token
    }
    return config
  },
  error => {      // 请求错误
    return Promises.reject(error)
  }
)

// http response响应拦截器
axios.interceptors.response.use(
  response => {
    return response
  },
  error => {
    if(error.response){
      switch(error.response.status){
        case 401:
          localStorage.removeItem('token')
          router.replace({
            path: '/login',
            quary:{redirect: router.currentRoute.fullPath} // 登陆成功后跳转入当前浏览页
          })
      }
    }
  }
)


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})




