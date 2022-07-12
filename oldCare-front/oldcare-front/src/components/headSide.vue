<template>
  <div>
    <el-container>
      <el-header class="my-header">
        <div class="left">
          <img src="../assets/logo.png" alt /> 
          <span>智慧养老系统</span>
        </div>

        <div class="btn-fullscreen" @click="handleFullScreen">
          <el-tooltip effect="dark" :content="fullscreen ? `取消全屏`:`全屏显示`" placement="bottom">
            <i class="el-icon-rank"></i>
          </el-tooltip>
        </div>

        <!-- 用户 -->
        <div class="right">
          <el-dropdown size="medium">
            <span class="el-dropdown-link" style="font-size:20px;">
              <i class="el-icon-s-custom" style="font-size:20px; margin-right:10px"></i>
              {{this.username}}
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item icon="el-icon-user" split-button="true">
                <span @click="logOut()">登出</span>
              </el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
      </el-header>
    </el-container>
  </div>
</template>

<script>
import { MessageBox } from 'element-ui';


export default {
  name: "headSide",
  data() {
    return {
      fullscreen: false,
      drawer: false,
      direction: "rtl"
    };
  },
  components: {},
  computed: {
    username() {
      return this.$store.state.user_name;
    }
  },
  created() {},
  methods: {
    // tologin() {
    //   this.$router.push({ path: "/" });
    // },
    // tozhuce() {
    //   let flag = false;
    //   this.$store.commit("login", flag);
    //   this.$router.push("/");
    //   console.log("退出登录");
    // },
    logOut(){
      MessageBox.confirm(this.lang.logoutTip).then(action => {
        this.$store.commit('%_removeStorage')
        this.$router.push('/login')
        alert(this.lang.logOutSuccess)
      }).catch(function (error){
        console.log(error)
      })
    },
    handleFullScreen() {
      let element = document.documentElement;
      if (this.fullscreen) {
        if (document.exitFullscreen) {
          document.exitFullscreen();
        } else if (document.webkitCancelFullScreen) {
          document.webkitCancelFullScreen();
        } else if (document.mozCancelFullScreen) {
          document.mozCancelFullScreen();
        } else if (document.msExitFullscreen) {
          document.msExitFullscreen();
        }
      } else {
        if (element.requestFullscreen) {
          element.requestFullscreen();
        } else if (element.webkitRequestFullScreen) {
          element.webkitRequestFullScreen();
        } else if (element.mozRequestFullScreen) {
          element.mozRequestFullScreen();
        } else if (element.msRequestFullscreen) {
          // IE11
          element.msRequestFullscreen();
        }
      }
      this.fullscreen = !this.fullscreen;
    },
    handleClose(done) {
      done();
    }
  }
};
</script>

<style>
html,
body {
  margin: 0;
  padding: 0;
  font-family: sans-serif;
}
.my-header {
  position: relative;
}
.el-header {
  background-color: rgb(245, 246, 246);
  line-height: 60px;
  box-shadow: 0 2px 12px 0 rgba(102, 100, 100, 0.1);
  border-bottom: 1px solid #dcdfe6;
}
.right {
  /* float: right; */
  position: absolute;
  top: 0;
  right: 20px;
}
.left img {
  float: left;
  width: 60px;
  height: 60px;
}
.left span{
  font-weight: 900;
  font-size: 25px;
}
.left {
  margin-left: 15px;
}
.btn-fullscreen {
  position: absolute;
  right: 80px;
  top: 0;
}

</style>