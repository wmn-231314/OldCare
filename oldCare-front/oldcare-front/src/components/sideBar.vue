<template>
  <div class="home">
    <el-container style="height:100%">
      <div style="border-right:1px solid #dcdfe6;" :style="height" class="leftm">
        <el-aside width="200px">

          <!-- 整体概况-首页 -->
          <el-menu :default-active="$route.path" style="min-height: 100%;" router>
            <el-menu-item index="/home/first">
              <i class="el-icon-odometer"></i>
              <span slot="title">整体概况</span>
            </el-menu-item>
            
            <!-- 监控管理 -->
            <el-submenu index="2">
              <template slot="title">
                <i class="el-icon-aim"></i>
                <span>监控管理</span>
              </template>
              <!-- 摄像头1 -->
              <el-menu-item-group>
                <el-menu-item index="/home/camera1">摄像头1</el-menu-item>
              </el-menu-item-group>
              <!-- 摄像头2 -->
              <el-menu-item-group>
                <el-menu-item index="/home/camera2">摄像头2</el-menu-item>
              </el-menu-item-group>
              <!-- 摄像头3 -->
              <el-menu-item-group>
                <el-menu-item index="/home/camera3">摄像头3</el-menu-item>
              </el-menu-item-group>
              <!-- 摄像头4 -->
            <el-menu-item-group>
                <el-menu-item index="/home/camera4">摄像头4</el-menu-item>
              </el-menu-item-group>
            </el-submenu>

            

            <!-- 信息采集 -->
            <el-menu-item index="/home/informationAcquisition">
              <i class="el-icon-s-claim"></i>
              <span slot="title">信息采集</span>
            </el-menu-item>

            <!-- 老人信息表 -->
            <el-menu-item index="/home/olderInformation">
              <i class="el-icon-s-claim"></i>
              <span slot="title">老人信息表</span>
            </el-menu-item>

            <!-- 护工信息表 -->
            <el-menu-item index="/home/nurseInformation">
              <i class="el-icon-s-claim"></i>
              <span slot="title">护工信息表</span>
            </el-menu-item>

            <!-- 情绪识别表 -->
            <el-menu-item index="/home/emotionRecognition">
              <i class="el-icon-s-claim"></i>
              <span slot="title">情绪识别表</span>
            </el-menu-item>

            <!-- 闯入表 -->
            <el-menu-item index="/home/breakIn">
              <i class="el-icon-s-claim"></i>
              <span slot="title">闯入表</span>
            </el-menu-item>

            <!-- 跌倒检测表 -->
            <el-menu-item index="/home/fallDetection">
              <i class="el-icon-s-claim"></i>
              <span slot="title">跌倒检测表</span>
            </el-menu-item>

            <!-- 老人护工交互表 -->
            <el-menu-item index="/home/olderNurse">
              <i class="el-icon-s-claim"></i>
              <span slot="title">老人护工交互表</span>
            </el-menu-item>
          
          </el-menu>
        </el-aside>
      </div>
      <el-container>
        <!-- 主要内容 -->
        <el-main>
          <div class="bar">
            <nav-bar></nav-bar>
          </div>
          <transition name="slide-fade">
            <router-view></router-view>
          </transition>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import navBar from "./navBar.vue";
export default {
  data() {
    return {
      height: {
        height: ""
      },
      isCollapse: true
    };
  },
  components: {
    navBar
  },
  mounted() {},
  methods: {
  },
  created() {
  },
  computed: {},
  watch: {}
};
</script>

<style>
html,
body {
  margin: 0;
  padding: 0;
  font-family: sans-serif;
  background-color: #fff;
  height: 100%;
}

.el-aside {
  background-color: #545c64;
}
.el-menu {
  border: none;
}
.bar {
  margin-bottom: 8px;
}
.slide-fade {
  position: absolute;
  left: 0;
  right: 0;
}
.slide-fade-enter-active {
  transition: all 1.2s ease;
}
.slide-fade-leave-active {
  transition: all 0.1s cubic-bezier(2, 0.5, 0.8, 1);
}
.slide-fade-enter,
.slide-fade-leave-to {
  left: 0;
  right: 0;
  transform: translateX(50px);
  opacity: 0;
}
.el-menu-item-group__title {
  padding: 0px 0px 0px 20px;
}
</style>
