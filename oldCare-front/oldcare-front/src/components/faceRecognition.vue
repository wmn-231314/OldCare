<template>
    
    <div class="face">
        <h2 class="tip"><b>请面向摄像头</b></h2>
        <div class="videos" ref="videos">
            <video id="video_cam" autoplay="autoplay"></video>
            <canvas id="canvas" height="480px" width="640px"></canvas>
        </div>
        <button @click="onSubmit()">点击登陆</button>
        <button @click="back()">返回账号密码登陆</button>
    </div>
</template>

<script>
    var imgFace;
    export default{
        // name: 'faceLogin',
        mounted(){
            this.camera_open()
            // this.faceRec()    
        },
        
        methods:{
            camera_open(){

                var constraints = {
                    video:{
                        height: 480,
                        width: 640
                    }
                };
                // var vio = this.$refs.video;
                let vio = document.getElementById('video_cam');
                // console.info(vio);
                var promise = navigator.mediaDevices.getUserMedia(constraints);
                promise.then(
                    (MediaStream) => {
                        // console.info(MediaStream);
                        vio.srcObject = MediaStream;
                        vio.play();
                    }
                ).catch((error)=>{
                    console.info(error);
                });
                // 拍照截图，获得canvas对象
                setTimeout(
                    function(){
                        let canvas = document.getElementById('canvas');
                        // console.info(canvas);
                        canvas.getContext('2d').drawImage(vio,0,0);
                        
                        // 得到图片，格式base64
                        canvas = canvas.toDataURL("image/png");
                        // console.log(canvas)
                        // 去掉canvas编码后可能出现的头，只保留编码
                        imgFace = canvas.replace(/^data:image\/(png|jpg);base64,/,"");
                        // console.info(imgFace);
                    },1000);
            }, // camera_open

            faceRec(){
                this.camera_open()
    
                this.$axios.post('/loginWithFace',  //url
            {
                photo: imgFace,
                test:1,
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    "Content-Type": "application/json;charset=utf-8"
                }
            })
                .then(res => {
                    console.log(res.data)
                    if(res.data.code == 200){
                        // token处理
                        this.$store.commit('$_setToken',res.data.data.token)                      
                        alert("登陆成功，欢迎您")
                        this.beforeDestroy()
                        this.$router.push({path: '/home/first'})   
                        location.reload() 
                    }else{
                        alert("人脸登陆失败")
                    }
                }).catch(function (error){
                    console.log(error)
                })
            },

            onSubmit(){
                this.faceRec()
            },

            back(){
                this.beforeDestroy()
                this.$router.push('/login')
                location.reload() // 跳转然后刷新页面后实现摄像头关闭
            },
            // 关闭摄像头
            beforeDestroy(){
                this.closeVideo()
            },
            closeVideo(){
                this.MediaStreamTrack && this.MediaStreamTrack.stop();
            }

        }
    }
</script>

<style scoped>
    * {margin: 0; padding: 0;}
    /* .face{
        width: 100%;
        height: 100%;
        position: relative;
    } */

    .tip{
        margin-top: 2%;
        text-align: center;
    }

    #video_cam{
        
        height: 480px;
        width: 640px;
        margin-left: 28%;
        margin-top: 3%;
        align-items: center;
        justify-content: center;
        border: solid 1px;
    }
    
    #canvas{
        height: 480px;
        width: 640px;
        display: none;
    }

    button{
        color:rgb(89, 88, 88);
        height: 36px;
        width: 160px;
        margin-left: 44.5%;
        margin-top: 25px;
        border: solid 1px;
        border-color: rgb(90, 179, 251);
        border-radius: 8px;
        background: white;

    }
    button:hover{
        background: rgb(90, 179, 251);
        color: white;
    }

</style>