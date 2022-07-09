<template>
    
    <div class="face">
        <h2 class="tip"><b>请面向摄像头</b></h2>
        <div class="videos" ref="videos">
            <video id="video_cam" autoplay="autoplay"></video>
            <canvas id="canvas"></canvas>
        </div>
    </div>
</template>

<script>
    import "../api/api";
    // var imgFace;
    export default{
        name: 'faceLogin',
        mounted(){
            this.camera_open()
            // this.faceRec()    // 该方法连接后端后测试
        },
        methods:{
            camera_open(){

                var constraints = {
                    video:{
                        height: 400,
                        width: 600
                    }
                };
                // var vio = this.$refs.video;
                let vio = document.getElementById('video_cam');
                console.info(vio);
                var promise = navigator.mediaDevices.getUserMedia(constraints);
                promise.then(
                    (MediaStream) => {
                        console.info(MediaStream);
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
                        console.info(canvas);
                        canvas.getContext('2d').drawImage(vio,0,0,640,480);
                        // console.info(typeof vio);
                        // console.info(canvas.getContext('2d').drawImage(vio, 0, 0,640, 480));
                        // 得到图片，格式base64
                        let imgFace = canvas.toDataURL("image/png");
                        // imgFace = canvas.subString();
                        console.info(imgFace);
                    },1000
                );
            }, // camera_open

            faceRec(){
                this.camera_open()
                this.$axios({
                    url:this.$loginFaceUrl,
                    method:'post',
                    Credentials:"include",
                    data:{
                        photo: imgFace
                    },
                    headers: {
                        // "Access-Control-Allow-Origin": "*",
                        // "Content-Type": "application/json;charset=utf-8"
                    }
                }).then(res => {
                    if(res.status == 200){
                        if(res.data.code == 0){
                            alert("登陆成功，欢迎您")
                            this.$router.push({path: '/home'})
                        }else if(res.data.code == -1){
                            alert("人脸登陆失败")
                        }
                    }else{
                        alert(res.data.msg)
                    }
                })
            }

        }
    }
</script>

<style>
    * {margin: 0; padding: 0;}
    /* .face{
        width: 100%;
        height: 100%;
        position: relative;
    } */

    .tip{
        margin-top: 5%;
        text-align: center;
    }

    #video_cam{
        
        /* height: 300px;
        width: 400px; */
        margin-left: 30%;
        margin-top: 5%;
        align-items: center;
        justify-content: center;
        border: solid 1px;
    }
    
    #canvas{
        height: 400px;
        width: 600px;
        display: none;
    }

</style>