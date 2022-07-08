<template>
  <div class="first">
    <div class="message">
      <el-row :gutter="20">
        <!-- 老人数量 -->
        <el-col :span="6">
          <div>
            <el-card style="position: relative;height: 230px;" class="elcard1">
              <span class="title">累计老人数</span><br>
              <span class="data" >{{oldNum}}人</span>
              <br>
              <br>
              <el-divider></el-divider>
              <span class="title">今日增加</span>&nbsp;<br>
              <span class="data">{{newOldNum}}人</span>
            </el-card>
          </div>
        </el-col>
        <!-- 男女老人占比 -->
        <el-col :span="6">
          <div>
            <el-card style="position: relative;height: 230px;" class="elcard1">
              <span class="title" >男女老人占比</span><br>
              <span class="data">{{rate}}%</span><br><br>
              <!-- 记得要画个图表 -->
              <div id="main1" style="height: 160% ;width: 100%"></div>
            </el-card>
          </div>
        </el-col>
        <!-- 累计护工数 -->
        <el-col :span="6">
          <div>
            <el-card style="position: relative;height: 230px;" class="elcard1">
              <span class="title">累计护工数</span><br>
              <span class="data" >{{volNum}}人</span>
              <br>
              <br>
              <el-divider></el-divider>
              <span class="title">今日到岗</span>&nbsp;<br>
              <span class="data">{{newVolNum}}人</span>
            </el-card>
          </div>
        </el-col>
        <!-- 今日情绪占比 -->
        <el-col :span="6">
          <div>
            <el-card style="position: relative;height: 230px;" class="elcard1">
              <span class="title">今日情绪占比</span>
              <div id="main3" style="height: 230%;width: 100%"></div>
            </el-card>
          </div>
        </el-col>
      </el-row>
    </div>
    <!-- 日报警闯入统计 -->
    <!-- 微笑排行榜 -->
    <!-- 老人护工交互记录 -->

  </div>
</template>

<script>
var female,male,new_old_num,new_vol_num,old_num,vol_num;
export default {
  data() {
    return {

    };
  },
  components: {},
  created() {
  },
  computed: {},
  methods: {
                connect() {
                this.$axios({
                    url: '/home/first',
                    method: 'get',
                    headers: {
                        "Access-Control-Allow-Origin": "*",
                        "Content-Type": "application/json;charset=utf-8"
                    }
                }).then(res => {
                    console.info(res.data)
                    if (res.status == 200) {
                        if (res.data.code == 0) {
                            female = res.data.data[0]["female"];
                            male = res.data.data[0]["male"]
                            old_num = res.data.data[0]["old_num"]
                            new_old_num = res.data.data[0]["new_old_num"]
                            vol_num = res.data.data[0]["vol_num"]
                            new_vol_num = res.data.data[0]["new_vol_num"]
                            this.oldNum = old_num
                            this.newOldNum = new_old_num
                            this.volNum = vol_num
                            this.newVolNum = new_vol_num
                            this.rate = male * 100 / (female + male)}}

                })
            },
  },
  mounted() {

  }
};
</script>

<style>
.title{
  font-size: 15px;
  font-style: italic;
}
.data{
  font-size: 20px;
  font-weight: bold;
}

</style>