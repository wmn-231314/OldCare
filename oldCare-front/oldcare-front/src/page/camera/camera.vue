<template>
    <div class="camera-box">
        <div>
            <el-button type="danger" icon="el-icon-video-camera-solid" plain @click="video1">摄像头1</el-button>
            <el-button type="warning" icon="el-icon-video-camera-solid" plain @click="video2">摄像头2</el-button>
            <el-button type="success" icon="el-icon-video-camera-solid" plain @click="video3">摄像头3</el-button>
            <el-button type="primary" icon="el-icon-video-camera-solid" plain @click="video4">摄像头4</el-button>
            <el-button type="info" icon="el-icon-video-camera-solid" plain @click="videoclose">停止</el-button>
        </div>
        
        <video muted controls autoplay width="100%" height="500" src="" id="videoElement"></video>
        <el-p class="tips" text-align="center">若查看其他菜单信息，请先点击上方停止按钮</el-p> 
        <div class="change" v-if="flag == 4">
            <el-button type="primary" plain @click="changeSize0()">禁区上移</el-button>
            <el-button type="primary" plain @click="changeSize1()">禁区下移</el-button>
            <el-button type="primary" plain @click="changeSize2()">禁区左移</el-button>
            <el-button type="primary" plain @click="changeSize3()">禁区右移</el-button>
            <el-button type="primary" plain @click="changeSize4()">禁区扩张</el-button>
            <el-button type="primary" plain @click="changeSize5()">禁区缩减</el-button>
        </div> 
    </div>
</template>
<script>
import flvjs from 'flv.js'
export default {
  data () {
    return {
	  flvPlayer:null,
      src:'http://1.15.63.218:7001/live/rawvideo.flv',
      flag:0
    }
  },

   mounted() {
    console.log('ceshi')
    var src=this.src
    this.play(src)
    },
    methods:{
        videoclose(){
            if(this.flvPlayer){
                this.flvPlayer.pause();
                this.flvPlayer.unload();
                this.flvPlayer.detachMediaElement();
                this.flvPlayer=null
            }
        },

      play (src) {
        if (flvjs.isSupported()) {
        var videoElement = document.getElementById('videoElement');
        this.flvPlayer = flvjs.createPlayer({
          type: 'flv',
		  isLive: true,
		  hasAudio: false,
          url: src
        });
        this.flvPlayer.attachMediaElement(videoElement);
        this.flvPlayer.load();
        let playPromise = this.flvPlayer.play()
       if (playPromise !== undefined) {
          playPromise.then(() => {
         this.flvPlayer.play()
        }).catch(()=> {})
        }
      }
      },
        video1(){
            this.videoclose()
            var src='http://1.15.63.218:7001/live/facial.flv'
            this.play(src)
            this.flag = 0
        },
        video2(){
            this.videoclose()
            var src='http://1.15.63.218:7001/live/fall.flv'
            this.play(src)
            this.flag = 0
        },
        video3(){
            this.videoclose()
            var src='http://1.15.63.218:7001/live/interaction.flv'
            this.play(src)
            this.flag = 0
        },
        video4(){
            this.videoclose()
            var src='http://1.15.63.218:7001/live/checkfence.flv'
            this.play(src)
            this.flag = 4
        },
        changeSize0(){
            this.$axios({
                method:'post',
                url:'',
                data:{
                    changeNum:1
                },
                headers: {
                        "Access-Control-Allow-Origin": "*",
                        "Content-Type": "application/json;charset=utf-8"
                    }
            }).then(res => {
                if(res.data.code == 200){                      
                       
                }else{
                    alert("修改失败！")
                }
            }).catch(function (error){
                console.log(error)
            })
        },
        changeSize1(){
            this.$axios({
                method:'post',
                url:'',
                data:{
                    changeNum:2
                },
                headers: {
                        "Access-Control-Allow-Origin": "*",
                        "Content-Type": "application/json;charset=utf-8"
                    }
            }).then(res => {
                if(res.data.code == 200){                      
                       
                }else{
                    alert("修改失败！")
                }
            }).catch(function (error){
                console.log(error)
            })
        },
        changeSize2(){
            this.$axios({
                method:'post',
                url:'',
                data:{
                    changeNum:3
                },
                headers: {
                        "Access-Control-Allow-Origin": "*",
                        "Content-Type": "application/json;charset=utf-8"
                    }
            }).then(res => {
                if(res.data.code == 200){                      
                       
                }else{
                    alert("修改失败！")
                }
            }).catch(function (error){
                console.log(error)
            })
        },
        changeSize3(){
            this.$axios({
                method:'post',
                url:'',
                data:{
                    changeNum:4
                },
                headers: {
                        "Access-Control-Allow-Origin": "*",
                        "Content-Type": "application/json;charset=utf-8"
                    }
            }).then(res => {
                if(res.data.code == 200){                      
                       
                }else{
                    alert("修改失败！")
                }
            }).catch(function (error){
                console.log(error)
            })
        },
        changeSize4(){
            this.$axios({
                method:'post',
                url:'',
                data:{
                    changeNum:5
                },
                headers: {
                        "Access-Control-Allow-Origin": "*",
                        "Content-Type": "application/json;charset=utf-8"
                    }
            }).then(res => {
                if(res.data.code == 200){                      
                       
                }else{
                    alert("修改失败！")
                }
            }).catch(function (error){
                console.log(error)
            })
        },
        changeSize5(){
            this.$axios({
                method:'post',
                url:'',
                data:{
                    changeNum:6
                },
                headers: {
                        "Access-Control-Allow-Origin": "*",
                        "Content-Type": "application/json;charset=utf-8"
                    }
            }).then(res => {
                if(res.data.code == 200){                      
                       
                }else{
                    alert("修改失败！")
                }
            }).catch(function (error){
                console.log(error)
            })
        }
    }
}</script>
<style>
  .camera-box{
    border: none;
    background-color:rgba(216, 212, 212, 0.293);
    height:600px;
    text-align:center;
    padding: 15px;
  }

</style>