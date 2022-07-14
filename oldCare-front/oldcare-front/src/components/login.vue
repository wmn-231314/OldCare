<template>
<div class="container">
  <div class="login">
    <!-- <h2 style="margin:30px 0 0 30px;">Hello!</h2> -->
    <div class="title">
        <img src="../assets/logo1.png"/>
        <span style="margin-top: 20px; font-size: 20px;">智慧养老系统</span>
    </div>
    <div class="login-box">
      <el-form :model="userInfo" :rules="rules" ref="userInfo" label-width="0px" class="content">
        <el-form-item prop="username">
          <el-input v-model="userInfo.username" placeholder="用户名" prefix-icon="el-icon-user">
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input type="password" v-model="userInfo.password" placeholder="请输入密码" prefix-icon="el-icon-lock">
          </el-input>
        </el-form-item>
        <div class="login-btn">
            <button @click="onsubmit()">账号密码登陆</button>
        </div>
        <div class="login-btn">
            <button @click="faceLogin()">人脸识别登陆</button>
        </div>
        <el-link type="primary" @click="register()" style="text-align: center;margin-top: 12px;">注册管理员></el-link>
      </el-form>   
    </div>
    <!-- <el-footer style="text-align: center;">智慧养老系统 created by 小学期小组</el-footer> -->
  </div>
</div>    
</template>

<script>
import router from '../router'

export default {
    data(){
        return {
            userInfo: {
                username:"",
                password:""
            },

            rules: {
              username: [
                { required: true, message: "请输入用户名", trigger: "blur" },
                { max: 10, message: "不能大于10个字符", trigger: "blur" }
              ],
              password: [
                { required: true, message: "请输入密码", trigger: "blur" },
                { max: 10, message: "不能大于10个字符", trigger: "blur" }
              ]
            }
        }
    },
    methods:{
        onsubmit(){
            console.log(this.userInfo.username)
            console.log(this.userInfo.password)
            let _this = this
            this.$axios.post('/login',  //url
            {
                username:this.userInfo.username,
                password:this.userInfo.password,
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    "Content-Type": "application/json;charset=utf-8"
                }
            }).then(function (response){
                let res = response.data
                console.log(res.data.token)
                if(res.code == 200){
                    // token处理
                    // var userinfo = res.data
                    _this.$store.commit('$_setToken',res.data.token)
                    alert("登陆成功！")
                    _this.$router.push('/home/first')
                }else{
                    alert("登陆失败，用户名或密码错误")
                }
            }).catch(function (error){
                console.log(error)
            })
        },
        faceLogin(){
            this.$router.push('/faceRecognition')
        },
        register(){
            this.$router.push('/register')
        }

    }
}
</script>

<style scoped>
.container{
    position: fixed;
    width: 100%;
    height: 100%;
    background: url("../assets/bgPic1.png") no-repeat;
    /*设置图片适应*/
    background-position: left;
    background-size: 75% 100%;
    background-attachment:fixed;
}

.title{
    margin-top: 8px;
    margin-left: 22px;
    padding: 0;
}

img{
    width: 60px;
    height: 60px;
    margin-top: -6px;
    padding: 0;
    vertical-align: middle;
}

.login{
    position:absolute;
    left:76%;
    top:45%;
    width: 320px;
    height: 400px;
    margin: -190px 0 0 -155px;
    border-radius: 5px;
    /* background: rgba(172, 203, 230, 0.607); */
    overflow: hidden;
    opacity:1;
}

.content {
    margin-top: -20px;
    padding: 30px 30px;
}

input{
    background-color: rgb(230, 235, 235);
}

.login-btn {
   text-align: center;
   position: center
}
.login-btn button{
  color:rgb(89, 88, 88);
  height: 36px;
  width: 160px;
  margin-bottom: 12px;
  border: solid 1px;
  border-color: rgb(90, 179, 251);
  border-radius: 8px;
  background: white;

}
.login-btn button:hover{
  background: rgb(90, 179, 251);
  color: white;
}

</style>
