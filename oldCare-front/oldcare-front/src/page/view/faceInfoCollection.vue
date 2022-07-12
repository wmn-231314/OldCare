<template>
    
    <div class="face">
        <h2 class="tip" v-bind="msg"><b>{{msg}}</b></h2>
        <div class="videos" ref="videos">
            <video id="video_cam" autoplay="autoplay"></video>
            <canvas id="canvas"></canvas>
        </div>
    </div>
</template>

<script>
export default{
    data:{
        msg:''
    }
}
</script>