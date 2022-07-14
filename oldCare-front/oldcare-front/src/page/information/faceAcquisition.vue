<template>
    
    <div class="face">
        <h1 class="title"><b>人脸信息采集</b></h1>
        <div class="videos" ref="videos">
            <video id="video_cam" autoplay="autoplay"></video>
            <canvas id="canvas"></canvas>
        </div>
        <br>
        <h2 class="tips" v-if="a === -1"><b>请正对摄像头</b></h2>
        <h2 class="tips" v-if="a === 0"><b>请眨眼</b></h2>
        <h2 class="tips" v-if="a === 1"><b>请张嘴</b></h2>
        <h2 class="tips" v-if="a === 2"><b>请抬头</b></h2>
        <h2 class="tips" v-if="a === 3"><b>请低头</b></h2>
        <h2 class="tips" v-if="a === 4"><b>面朝左看左边</b></h2>
        <h2 class="tips" v-if="a === 5"><b>面朝右看右边</b></h2>
        <h2 class="tips" v-if="a === 6"><b>采集结束</b></h2>
        <br>
        <button @click="collect()">点击开始采集</button>
    </div>
</template>

<script>
export default{
    data:{
        base64Img:[],
        a:-1
    },
    methods:{
        camera_options(){
            k = 1;
            let _this = this;
            var constraints = {
                video: {
                    width: 400,
                    height: 600
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

            // 拍照截图，获得canvas对象(获取照片算法待修改)
            setTimeout(function() {
                for (var i = 1; i < 501; i++) {
                    setTimeout(function () {
                        k = k + 1;
                        console.log(this.a)
                        console.log(_this.a)
                        this.a=Math.floor(k/83);
                        let canvas = document.getElementById("canvas");
                        canvas.getContext('2d').drawImage(video, 0, 0, 640, 480);
                        canvas = canvas.toDataURL("image/png");
                        inner.push(canvas.substring());
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
                console.info(trans.length);
                alert('采集结束');
            },5000);

        },

        upload(){
            this.$axios({
                url:'',  // 此处可能要通过之前参数判断老人还是义工
                method:'post',
                data:{
                    img_array:trans
                },
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    "Content-Type": "application/json;charset=utf-8"
                }
            }).then(res => {
                if(res.data.code === 200){
                    alert("信息录入成功！")
                    this.$router.push('/olderInfomation') // 此处可能要通过之前参数判断
                }
            })
        },
        collect(){
            this.camera_options()
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

    .title{
        margin-top: 5%;
        text-align: center;
    }

    .tips{
        text-align: center;
    }

    #video_cam{
        
        height: 400px;
        width: 600px;
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