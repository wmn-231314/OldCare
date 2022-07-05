<!-- 闯入表 -->
<template>
  <div>
    <div class="list">
      <!-- 搜索栏 -->
      <el-form :inline="true" class="demo-form-inline">
        <el-form-item>
          <el-input v-model="search" class="search_time" size="mini" placeholder="输入时间查询"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="text" @click="onSearch()" class="el-icon-search">查询</el-button>
        </el-form-item>
      </el-form>

      <!-- 表格 -->
      <el-table
        :data="needPlanS"
        style="width: 100%"
        highlight-current-row
        border
        @current-change="handleCurrentsChange"
      >

        <el-table-column label="地点" prop="customer"></el-table-column>

        <el-table-column label="时间" prop="beginTime"></el-table-column>

        <el-table-column label="图片" prop="username"></el-table-column>
      </el-table>
      <!-- 分页 -->
      <div class="page">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[5, 10, 20, 40]"
          :page-size="pagesize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
        ></el-pagination>
      </div>
    </div>
  </div>
</template>

<script>

</script>

<style>
.el-table-column {
  text-align: center;
}
.list {
  position: relative;
}

.popContainer {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 500;
}
</style>
