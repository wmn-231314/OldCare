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
        <br>
        <el-p text-align="center">若查看其他菜单信息，请先点击上方停止按钮</el-p> 
        <div class="change">
            <el-button type="primary" plain @click="changeSize()">禁止区上移</el-button>
            <el-button type="primary" plain @click="changeSize()">禁止区下移</el-button>
            <el-button type="primary" plain @click="changeSize()">禁止区左移</el-button>
            <el-button type="primary" plain @click="changeSize()">禁止区右移</el-button>
            <el-button type="primary" plain @click="changeSize()">禁止区扩张</el-button>
            <el-button type="primary" plain @click="changeSize()">禁止区缩减</el-button>
        </div> 
    </div>
</template>
<script>
import flvjs from 'flv.js'
export default {
  data () {
    return {
	  flvPlayer:null,
      src:'http://1.15.63.218:7001/live/rawvideo.flv'
    }
  },

   mounted() {
    console.log('ceshi')
    var src=this.src
    this.play(src);
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
        var src='http://1.15.63.218:7001/live/rawvideo.flv'
        this.play(src)
    },
    video2(){
        this.videoclose()
        var src='http://1.15.63.218:7001/live/test.flv'
        this.play(src)
    },
    video3(){
        this.videoclose()
        var src='http://1.15.63.218:7001/live/rawvideo.flv'
        this.play(src)
    },
    video4(){
        this.videoclose()
        var src='http://1.15.63.218:7001/live/rawvideo.flv'
        this.play(src)
    },
    changeSize(){

    }
    }
}</script>
<style>
.camera-box{
    border: none;
    background-color:rgba(216, 212, 212, 0.293);
    height:700px;
    text-align:center;
    padding: 10px;
}

</style>