<template>
  <div class="informationBox">
    <el-form ref="form" :model="form" label-width="100px">
        <el-form-item label="入住房间号">
            <el-input v-model="form.roomnum" name="roomnum" style="width:100%;"></el-input>
        </el-form-item>
        <el-form-item label="电话号码">
            <el-input v-model="form.phone" name="phone" style="width:100%;"></el-input>
        </el-form-item>
        <el-form-item label="入住时间">
          <el-date-picker type="date" placeholder="选择日期" format="yyyy-MM-dd" value-format="yyyy-MM-dd" v-model="form.checkin_date" style="width: 100%;"></el-date-picker>
        </el-form-item>
        <el-form-item label="预计离院时间">
          <el-date-picker type="date" placeholder="选择日期" format="yyyy-MM-dd" value-format="yyyy-MM-dd" v-model="form.checkout_date" style="width: 100%;"></el-date-picker>
        </el-form-item>
        <el-form-item label="身份证照片">
          <el-upload
            class="avatar-uploader"
            action=""
            :show-file-list="false"
            :before-upload="beforeupload"
            :on-change="handleChangeUpload"
            :limit="1"
            list-type="picture">
            <img v-if="src" :src="src" class="avatar">
            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
           </el-upload>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="onSubmit">下一步</el-button>
            <el-button type="primary" @click="cancle">取消</el-button>
        </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      // 房间号+入住时间
      form: {
        roomnum: '',
        checkin_date:'',
        checkout_date:'',
        phone:'',
        photo:''
      },
      src:"",
    };
  },
  methods: {
    //取消自动上传
    beforeupload(file) {
      console.log(file);
      var windowURL = window.URL || window.webkitURL;
      this.src=windowURL.createObjectURL(file);
      return false;
    },
    handleChangeUpload(file) {
      let testFile = file.name.substring(file.name.lastIndexOf('.') + 1).toLowerCase()

      const extension = testFile === 'png' || testFile === 'jpg';

      const isLt2M = (file.size / 1024 / 1024 < 2);
      if (!extension) {
        this.$message({
          message: '上传文件只能是png/jpg!',
          type: 'warning'
        });
        this.fileUploadList = []
        return false;
      }
      if (!isLt2M) {
        this.$message({
          message: "文件大小不可以超过2M",
          type: 'warning'
        });
        this.fileUploadList = []
        return false;
      }
      this.getBase64(file.raw).then(res1 => {
        this.photo =res1;
      });
      return (extension) && isLt2M;
    },
    getBase64(file) {
      return new Promise(function(resolve, reject) {
        let reader = new FileReader();
        let imgResult = "";
      reader.readAsDataURL(file);
      reader.onload = function() {
      imgResult = reader.result;
      };
      reader.onerror = function(error) {
        reject(error);
      };
      reader.onloadend = function() {
        resolve(imgResult);
      };
      });
            },
    onSubmit(){
    this.$axios
    .post('/addOldPersonInfo',
    {
      room_number:this.form.roomnum,
      phone:this.form.phone,
      checkin_date:this.form.checkin_date,
      checkout_date:this.form.checkout_date,
      idCard_photo_base64:this.photo
     }
     )
     .then(
         successResponse => {
         if (successResponse.data.code == 200) {
             alert("成功录入信息！")
            //  this.$router.push('/home/faceAcquisition')
         }else if(successResponse.data.code == 412){
          alert("信息已存在！")
         }else{
             console.log(successResponse.data.code );
             alert("录入信息失败！")
         }
     })
     .catch(failResponse => {
     })
    },
    cancle(){
      this.$router.push('/home/first')
    }
  }
}
</script>
<style>
.informationBox{
  height: 300px;
  width: 400px;
  position: absolute;
  top: -100px;
  bottom: 0;
  left: 0;
  right: 0;
  margin: auto;
  text-align: center;
}
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.avatar-uploader .el-upload:hover {
    border-color: #409EFF;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  line-height: 100px;
  text-align: center;
}
.avatar {
  width: 100px;
  height: 100px;
  display: block;
}
</style>