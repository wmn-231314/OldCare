import Vue from 'vue'
import Router from 'vue-router'
// 登录注册
import login from '@/components/login.vue'
import register from '@/components/register.vue'
import faceRecognition from '@/components/faceRecognition.vue'
// 主页
import home from '@/components/home.vue'
import headSide from '@/components/headSide.vue'
import navBar from '@/components/navBar.vue'
// 首页
import first from '@/page/view/first'
// 监控
import camera from '@/page/camera/camera'
// 表格
import breakIn from '@/page/chart/breakIn'
import emotionRecognition from '@/page/chart/emotionRecognition'
import fallDetection from '@/page/chart/fallDetection'
import volunteerInformation from '@/page/chart/volunteerInformation'
import olderInformation from '@/page/chart/olderInformation'
import olderVolunteer from '@/page/chart/olderVolunteer'
// 信息采集页面
import oldinformationAcquisition from '@/page/information/oldInformationAcquisition'
import volunteerinformationAcquisition from '@/page/information/volunteerInformationAcquisition'
import faceAcquisition from '@/page/information/faceAcquisition'







Vue.use(Router)

export default new Router({

  routes: [

    {
      path: '/',
      redirect: '/login'
    },
    // 登录
    {
      path: '/login',
      name: 'login',
      component: login,
      meta:{ title: '登录' ,requireAuth:true}
    },

    // 主页
    {
      path: '/home',
      name: 'home',
      component: home,
      meta: { title: '首页', requireAuth:true },
      children:[
        // 整体概况
        {
          path: '/home/first',
          name: 'first',
          component : first,
          meta: { requireAuth:true },
        },
        // 监控管理
        {
          path: '/home/camera',
          name: 'camera',
          component : camera,
          meta: { title: '摄像头' , requireAuth:true}
        },
        // 信息采集
        // 老人信息采集
        {
          path: '/home/oldinformationAcquisition',
          name: 'oldinformationAcquisition',
          component : oldinformationAcquisition,
          meta: { title: '老人信息采集' , requireAuth:true}
        },
        // 护工信息采集
        {
          path: '/home/volunteerinformationAcquisition',
          name: 'volunteerinformationAcquisition',
          component : volunteerinformationAcquisition,
          meta: { title: '护工信息采集' , requireAuth:true}
        },
        // 人脸采集
        {
          path: '/home/faceAcquisition',
          name: 'faceAcquisition',
          component : faceAcquisition,
          meta: { title: '人脸信息采集' , requireAuth:true}
        },
        // 老人信息表
        {
          path: '/home/olderInformation',
          name: 'olderInformation',
          component : olderInformation,
          meta: { title: '老人信息表' , requireAuth:true}
        },
        // 护工信息表
        {
          path: '/home/volunteerInformation',
          name: 'volunteerInformation',
          component : volunteerInformation,
          meta: { title: '护工信息表' , requireAuth:true}
        },
        // 情绪识别表
        {
          path: '/home/emotionRecognition',
          name: 'emotionRecognition',
          component : emotionRecognition,
          meta: { title: '情绪识别表' , requireAuth:true}
        },
        // 闯入表
        {
          path: '/home/breakIn',
          name: 'breakIn',
          component : breakIn,
          meta: { title: '闯入表' , requireAuth:true}
        },
        // 跌倒检测表
        {
          path: '/home/fallDetection',
          name: 'fallDetection',
          component : fallDetection,
          meta: { title: '跌倒检测表' , requireAuth:true}
        },
        // 老人护工交互表
        {
          path: '/home/olderVolunteer',
          name: 'olderVolunteer',
          component : olderVolunteer,
          meta: { title: '老人护工交互表' , requireAuth:true}
        },
        
      ]
    },
    // 注册
    {
      path: '/register',
      name: 'register',
      component: register,
      meta:{ title: '注册' ,requireAuth:true}
    },
    // 人脸识别
    {
      path: '/faceRecognition',
      name: 'faceRecognition',
      component: faceRecognition,
      meta:{ title: '人脸识别' ,requireAuth:true}
    },
    {
      path: '/headSide',
      name: 'headSide',
      component : headSide,
      meta:{ requireAuth:true}
    },
    {
      path: '/navBar',
      name: 'navBar',
      component : navBar,
      meta:{ requireAuth:true}
    },
    
  ]
});



