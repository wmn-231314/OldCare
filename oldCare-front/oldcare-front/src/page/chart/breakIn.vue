<!-- 闯入表 -->
<template>
  <el-table
    :data="breakInData.filter(data => !search || data.eventLocation.toLowerCase().includes(search.toLowerCase()))"
    style="width: 100%" border>
    <!-- 地点 -->
    <el-table-column
      align="center"
      label="地点"
      prop="eventLocation">
    </el-table-column>
    <!-- 时间 -->
    <el-table-column
      align="center"
      label="时间"
      prop="eventDate">
    </el-table-column>
    <!-- 图片 -->
    <el-table-column prop="eventPhoto" label="图片" align="center">
        <template slot-scope="scope">
            <img :src="scope.row.eventPhoto" style="height: 50px"/>
        </template>
    </el-table-column>
    <!-- 搜索 -->
    <el-table-column
      align="right">
      <template slot="header" slot-scope="{}">
        <el-input
          v-model="search"
          size="mini"
          placeholder="请输入地点搜索"/>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
  export default {
    data() {
      return {
       breakInData : [],
        search: ''
      }
    },
        mounted() {
      this.$axios({
        url:'/table_instrusion',
        method:'get',
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Content-Type": "application/json;charset=utf-8"
        },
        params: {
          eventType: 4 ,}
      }).then(res => {
        if(res.status==200){
          if(res.data.code==200){
            this.breakInData =res.data.data
          }else if(res.data.code==-1){
            alert("查询失败！")
          }
        }else{
          alert(res.data.msg)
        }
      })
    },
    methods: {
      handleEdit(index, row) {
        console.log(index, row);
      },
      handleDelete(index, row) {
        console.log(index, row);
      }
    },
  }
</script>