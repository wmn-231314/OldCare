<!-- 护工信息表 -->
<template>
  <el-table
    :data="nurseData.filter(data => !search || data.id_card.toLowerCase().includes(search.toLowerCase()))"
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
    <!-- 手机号 -->
    <el-table-column
      align="center"
      width="150"
      label="手机号"
      prop="phone">
    </el-table-column>
    <!-- 是否在岗 -->
    <el-table-column
      align="center"
      width="150"
      label="是否在岗"
      prop="is_active">
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
        nurseData: [],
        search: ''
      }
    },
        mounted() {
      this.$axios({
        url:'/table_volunteer',
        method:'get',
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Content-Type": "application/json;charset=utf-8"
        }
      }).then(res => {
        if(res.status==200){
          if(res.data.code==200){
            this.nurseData =res.data.data
          }else if(res.data.code==-1){
            alert("查询失败！")
          }
        }else{
          alert(res.data.msg)
        }
      }).catch(err=>{
        console.log(err);
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