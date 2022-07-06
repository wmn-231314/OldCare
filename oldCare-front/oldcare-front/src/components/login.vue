<template>
  <div :style="height">

    <div class="login">
      <div class="login-box">

         <el-form :model="loginForm" :rules="rules" ref="loginForm" label-width="0px" class="ms-content">
                <el-form-item prop="username">
                    <el-input v-model="loginForm.username" placeholder="用户名" prefix-icon="el-icon-user">
                    </el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input type="password" placeholder="密码" v-model="loginForm.password" prefix-icon="el-icon-lock">
                    </el-input>
                </el-form-item>
                <div class="login-btn">
                  <button @click="submitLoginForm('loginForm')">登录</button>
                  <button @click="faceRecognition()">人脸识别登录</button>
                </div>
                <el-link type="primary" @click="register()" style="text-align: center;">去注册 ></el-link>
            </el-form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "login",
  data() {
    return {
      loginForm: {
        password: "",
        userName: ""
      },
      height: {
        height: ""
      },

      responseResult: [],
      rules: {
        userName: [
          { required: true, message: "请输入用户名", trigger: "blur" },
          { max: 10, message: "不能大于10个字符", trigger: "blur" }
        ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          { max: 10, message: "不能大于10个字符", trigger: "blur" }
        ]
      }
    };
  },
  components: {},
  created() {
    this.hh();
  },
  inject: ["reload"],
  methods: {
    submitLoginForm(loginForm) {
      let flag = true;
      this.$store.commit('login',flag);
      let _this = this;
       this.$axios
         .post("/login", {
           passWord: this.loginForm.password,
           userName: this.loginForm.userName
         })
         .then(res => {
           if (res.data.code === 200) {
             this.$router.push({ path: "/home/first" });
             this.$store.commit("handleUserName", res.data.data.userName);
             this.$message("登陆成功");
             this.$router.push({ path: "/home/first" });
             this.$store.commit("handleUserName", res.data.data.userName);
             this.$message("登陆成功");
           }
         })
         .catch(err => {
           this.$message("账号密码有误");
         });
    },
    faceRecognition(){
      this.$router.push({ path: "/register" });
    },
    register() {
      this.$router.push({ path: "/register" });
    },
    hh() {
      this.height.height = window.innerHeight + "px";
    }
  }
};
</script>

<style scoped>
body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  /* background: url(./../assets/loginbg.jpg) no-repeat;
		background-size: 100% 100%; */
  /* background: linear-gradient(91deg, #f1eefc, #9dc6ff 70%, #a5bcff); */
}
.login {
  width: 100%;
  height: 100%;
  /* background: linear-gradient(91deg, #f1eefc, #9dc6ff 70%, #a5bcff); */
  background-color: #112;

}

.login-box {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 350px;
  height:300px;
  margin: -190px 0 0 -175px;
  border-radius: 5px;
  background: rgba(86, 117, 143, 0.425);
  overflow: hidden;
}


.login-box .login-button {
  margin-top: 10px;
  width: 320px;
}

.ms-content {
    padding: 30px 30px;
}

.login-btn {
   text-align: center;
   position: center
}
.login-btn button{
  color:white;
  height: 40px;
  width: 70px;
  border: none;
  border-radius: 5px;
  background: rgb(90, 179, 251);

}
.login-btn button:hover{
  background: rgb(11, 65, 109);;
}


label {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1;
  padding-left: 0.1em;
  font-size: 4em;
  cursor: pointer;
  transition: all 0.5s cubic-bezier(0.65, 0.05, 0.36, 1);
}

</style>