<template>
    
    <div class="face">
        <h2 class="title" text-align="center"><b>人脸信息采集</b></h2>
        <div class="videos" ref="videos">
            <video id="video_cam" autoplay="autoplay"></video>
            <canvas id="canvas" height="480px" width="640px"></canvas>
        </div>
        <h2 class="tips" v-if="a == -1" text-align="center"><b>请正对摄像头</b></h2>
        <h2 class="tips" v-if="a == 0" text-align="center"><b>请眨眼</b></h2>
        <h2 class="tips" v-if="a == 1" text-align="center"><b>请张嘴</b></h2>
        <h2 class="tips" v-if="a == 2" text-align="center"><b>请抬头</b></h2>
        <h2 class="tips" v-if="a == 3" text-align="center"><b>请低头</b></h2>
        <h2 class="tips" v-if="a == 4" text-align="center"><b>请看左边</b></h2>
        <h2 class="tips" v-if="a == 5" text-align="center"><b>请看右边</b></h2>
        <h2 class="tips" v-if="a == 6" text-align="center"><b>采集结束</b></h2>
        <div>
            <el-button type="primary" plain @click="collect()">点击录入采集数据</el-button>
            <el-button type="primary" plain @click="upload()">确认上传数据</el-button>
        </div>
        

    </div>
</template>


<script>
var trans = new Array()
var inner = new Array()
// var action = new Array()
var k
export default{
    
    data(){
        return{
            a:-1,
            type: '',
            id: ''
        }     
    },
    created(){

        let type1 = this.$route.params.infoType
        let id1 = this.$route.params.infoId
        this.type = type1
        this.id = id1
    },
    methods:{
        camera_options(){
            k = 1;
            var constraints = {
                video: {
                    width: 640,
                    height: 480
                },
            };
            let video = document.getElementById("video_cam")
            //    console.info(videos);
            var promise = navigator.mediaDevices.getUserMedia(constraints);
            promise.then((MediaStream) => {
                video.srcObject = MediaStream;
                video.play();
            }).catch((error) => {
                console.info(error);
            });

            // 拍照截图，获得canvas对象
            setTimeout(function() {
                for (var i = 1; i < 501; i++) {
                    setTimeout(function () {
                        // console.log(k)
                        // console.log(aa)
                        k = k + 1;
                        let canvas = document.getElementById("canvas");
                        canvas.getContext('2d').drawImage(video, 0, 0, 640, 480);
                        canvas = canvas.toDataURL("image/png");
                        inner.push(canvas);
                    },500)    
                }
                setTimeout(function(){
                    for(var i = 0 ; i < 500 ; i++){
                        if(i % 5 === 0){
                            trans.push(inner[i]);
                        }
                    }
                },1000);
            }, 2000);

            setTimeout(function () {
                //    console.info(inner)
                // console.info(trans.length);
                console.log(trans)
                alert('采集结束');
            },5000);

        },
        
        upload(){    
            console.log(this.type)
            console.log(this.id)
            this.$axios({
                url:'/collectInfo',  
                method:'post',
                data:{
                    img_array: trans,
                    role: this.type,
                    id: this.id
                },
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    "Content-Type": "application/json;charset=utf-8"
                }
            }).then(res => {
                console.log(res.data)
                if(res.data.code === 200){
                    alert("信息录入成功！")
                    if(this.type == 'old'){
                        this.beforeDestroy()
                        // this.$router.push('/home/olderInfomation')
                        location.reload()
                    }else{
                        this.beforeDestroy()
                        // this.$router.push('/home/volunteerInformation')
                        location.reload()
                    }

                }else if(res.data.code == -1){
                    alert("信息录入失败，请重新录入！")
                    this.beforeDestroy()
                    location.reload()      
                }else{
                    alert(res.data.msg)
                }
            })
        },
        collect(){
            this.camera_options()
            var aa = 0
            for(var i = 0;i < 4;i++){
                setTimeout(function(){
                    aa = aa + 1
                },5000)
                this.a = this.a + aa
            }

        },
        // 关闭摄像头
        beforeDestroy(){
            this.closeVideo()
        },
        closeVideo(){
            this.MediaStreamTrack && this.MediaStreamTrack.stop();
        },
    }
}
</script>

<style scoped>
    .face{
    border: none;
    background-color:rgba(216, 212, 212, 0.293);
    height:640px;
    text-align:center;
    padding: 10px;
  }

    #video_cam{        
        height: 480px;
        width: 640px;       
    }
    
    #canvas{
        height: 480px;
        width: 640px;
        display: none;
    }


</style>