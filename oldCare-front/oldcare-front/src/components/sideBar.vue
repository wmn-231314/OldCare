<template>
  <div class="home">
    <el-container style="height:100%">
      <div style="border-right:1px solid #dcdfe6;"  class="leftm">
        <el-aside width="200px">
          <!-- 整体概况-首页 -->
          <el-menu :default-active="$route.path" style="min-height: 100%;" router>
            <el-menu-item index="/home/first">
              <i class="el-icon-s-home"></i>
              <span slot="title">整体概况</span>
            </el-menu-item>
          
            <!-- 监控管理 -->
            <el-menu-item index="/home/camera">
              <i class="el-icon-video-camera"></i>
              <span slot="title">监控管理</span>
            </el-menu-item>
            <!-- 信息采集 -->
            <el-submenu index="3">
              <template slot="title">
                <i class="el-icon-upload"></i>
                <span>信息采集</span>
              </template>
              <!-- 老人信息采集 -->
              <el-menu-item-group>
                <el-menu-item index="/home/oldInformationAcquisition">
                  <i class="el-icon-user-solid"></i>
                  <span slot="title">老人信息采集</span>
                </el-menu-item>
              </el-menu-item-group>
              <!-- 护工信息采集 -->
              <el-menu-item-group>
                <el-menu-item index="/home/volunteerinformationAcquisition">
                  <i class="el-icon-user"></i>
                  <span slot="title">护工信息采集</span>
                </el-menu-item>
              </el-menu-item-group>
            </el-submenu>

            <!-- 老人信息表 -->
            <el-menu-item index="/home/olderInformation">
              <i class="el-icon-user-solid"></i>
              <span slot="title">老人信息表</span>
            </el-menu-item>

            <!-- 护工信息表 -->
            <el-menu-item index="/home/volunteerInformation">
              <i class="el-icon-user"></i>
              <span slot="title">护工信息表</span>
            </el-menu-item>

            <!-- 情绪识别表 -->
            <el-menu-item index="/home/emotionRecognition">
              <i class="el-icon-loading"></i>
              <span slot="title">情绪识别表</span>
            </el-menu-item>

            <!-- 闯入表 -->
            <el-menu-item index="/home/breakIn">
              <i class="el-icon-aim"></i>
              <span slot="title">闯入表</span>
            </el-menu-item>

            <!-- 跌倒检测表 -->
            <el-menu-item index="/home/fallDetection">
              <i class="el-icon-view"></i>
              <span slot="title">跌倒检测表</span>
            </el-menu-item>

            <!-- 老人护工交互表 -->
            <el-menu-item index="/home/olderVolunteer">
              <i class="el-icon-s-order"></i>
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
