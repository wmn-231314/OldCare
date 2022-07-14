<!-- 老人信息表 -->
<template>
  <el-table
    :data="olderData.filter(data => !search || data.id_card.toLowerCase().includes(search.toLowerCase()))"
    style="width: 100%" border>
    <!-- 姓名 -->
    <el-table-column
      align="center"
      fixed
      width="150"
      label="姓名"
      prop="username">
    </el-table-column>
    <!-- 图片 -->
    <el-table-column prop="photo" label="图片" width="200" align="center">
        <template slot-scope="scope">
            <img :src="scope.row.photo" style="height: 50px"/>
        </template>
    </el-table-column>
    <!-- 身份证号 -->
    <el-table-column
      align="center"
      width="200"
      label="身份证号"
      prop="id_card">
    </el-table-column>
    <!-- 性别 -->
    <el-table-column
      align="center"
      width="100"
      label="性别"
      prop="gender">
    </el-table-column>
    <!-- 房间号 -->
    <el-table-column
      align="center"
      width="150"
      label="房间号"
      prop="room_num">
    </el-table-column>
    <!-- 入住时间 -->
    <el-table-column
      align="center"
      width="150"
      label="入住时间"
      prop="checkin_date">
    </el-table-column>
    <!-- 搜索 -->
    <el-table-column
      width="200"
      fixed="right"
      align="right">
      <template slot="header" slot-scope="{}">
        <el-input
          v-model="search"
          size="mini"
          placeholder="请输入身份证号搜索"/>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
  export default {
    data() {
      return {
        olderData: [],
        search: ''
      }
    },
    mounted() {
      this.$axios({
        url:'/table_oldPerson',
        method:'get',
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Content-Type": "application/json;charset=utf-8"
        }
      }).then(res => {
        if(res.status==200){
          if(res.data.code==200){
            this.olderData =res.data.data
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