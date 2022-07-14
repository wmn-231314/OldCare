<template>
  <div class="first" style="height:auto">
    <div class="message">
      <el-row :gutter="20">
        <!-- 累计老人数量 -->
        <el-col :span="6">
          <div>
            <el-card style="position: relative;height: 100px;">
              <span class="title">累计老人人数</span><br><br>
              <span class="data" >{{number_oldPeople}}人</span>
            </el-card>
          </div>
        </el-col>
        <!-- 今日新增老人数量 -->
        <el-col :span="6">
          <div>
            <el-card style="position: relative;height: 100px;">
              <span class="title">今日增加</span>&nbsp;<br><br>
              <span class="data">{{newOldNum}}人</span>
            </el-card>
          </div>
        </el-col>
        <!-- 累计护工数 -->
        <el-col :span="6">
          <div>
            <el-card style="position: relative;height: 100px;">
              <span class="title">累计护工数</span><br><br>
              <span class="data" >{{volNum}}人</span>
            </el-card>
          </div>
        </el-col>
        <!-- 今日到岗护工数 -->
        <el-col :span="6">
          <div>
            <el-card style="position: relative;height: 100px;" >
              <span class="title">今日到岗</span><br><br>
              <span class="data">{{newVolNum}}人</span>
            </el-card>
          </div>
        </el-col>

      </el-row>
      <br><br>
      <el-row :gutter="20">
        <!-- 老人性别比例 -->
        <el-col :span="12">
          <div>
            <el-card style="position: relative;height: 230px;">
              <span class="title" >老人性别比例</span><br>
              <span class="data">{{rate}}%</span><br><br>
              <div id="genderRate" style="height: 160% ;width: 100%"></div>
            </el-card>
          </div>
        </el-col>
        <!-- 今日情绪占比 -->
        <el-col :span="12">
          <div>
            <el-card style="position: relative;height: 230px;">
              <span class="title">今日情绪占比</span>
              <div id="emotion" style="height: 230%;width: 100%"></div>
            </el-card>
          </div>
        </el-col>
      </el-row>
    </div>
    <br><br>
    <!-- 日报警闯入统计 -->
    <el-row>
      <div>
        <el-card style="position: relative;height: 430px;">
          <span class="title">日报警、闯入统计</span>
          <br>
          <div id="alert" style="height: 430%;width: 100%" align="center"></div>
        </el-card>
      </div>
    </el-row>
  </div>
</template>

<script>
import echarts from 'echarts'
// 老人男女人数，新入住老人人数，在岗护工人数，老人累计人数，护工人数
var female_OldPeople,male_OldPeople,numberOfNew_oldPeople,numberOfActive_volunteer,number_oldPeople,number_volunteer;
// 摔倒报警数
var fall=new Array();
// 闯入数
var breakIn=new Array();
// 情绪数据
var emotion=new Array();
// 老人男女占比
var genderRateChart,emotionChart,alertChart;
export default {
  data() {
    return {
      number_oldPeople:0,
      newOldNum:0,
      volNum:0,
      newVolNum:0,
      rate:0,
    };
  },
  components: {},
  created() {
  },
  computed: {},
  methods: {
    connect() {
      this.$axios({
        url: '/homePage_data',
        method: 'get',
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Content-Type": "application/json;charset=utf-8"
          }
          }).then(res => {
            
            console.info(res.data)
            if (res.status == 200) {
              if (res.data.code ==200) {
                female_OldPeople = res.data.data.female_OldPeople
                console.log('res.data.data.female_OldPeople')
                male_OldPeople = res.data.data.male_OldPeople
                console.log(male_OldPeople)
                number_oldPeople = res.data.data.number_oldPeople
                numberOfNew_oldPeople = res.data.data.numberOfNew_oldPeople
                number_volunteer = res.data.data.number_volunteer
                numberOfActive_volunteer = res.data.data.numberOfActive_volunteer
                // 累计老人数
                this.number_oldPeople = number_oldPeople
                // 新入住老人数
                this.newOldNum = numberOfNew_oldPeople
                // 老人男女比例
                this.rate = male_OldPeople * 100 / (female_OldPeople + male_OldPeople)
                // 累计护工数
                this.volNum = number_volunteer
                // 在岗护工数
                this.newVolNum = numberOfActive_volunteer
                // 情绪数据
                emotion[0]=res.data.data.emotion.anger
                console.log("anger"+res.data.data.emotion.anger)
                emotion[1]=res.data.data.emotion.disgust
                emotion[2]=res.data.data.emotion.fear
                emotion[3]=res.data.data.emotion.happiness
                emotion[4]=res.data.data.emotion.neutral
                emotion[5]=res.data.data.emotion.sadness
                emotion[6]=res.data.data.emotion.surprise
                // 摔倒报警
                fall[0]=res.data.data.fall.within_four_days
                fall[1]=res.data.data.fall.within_five_days
                fall[2]=res.data.data.fall.within_six_days
                fall[3]=res.data.data.fall.within_seven_days
                fall[4]=res.data.data.fall.within_eight_days
                fall[5]=res.data.data.fall.within_nine_days
                fall[6]=res.data.data.fall.within_ten_days
                fall[7]=res.data.data.fall.within_eleven_days
                fall[8]=res.data.data.fall.within_twelve_days
                fall[9]=res.data.data.fall.within_thirteen_days
                // 闯入
                breakIn[0]=res.data.data.intrusion.within_four_days
                breakIn[1]=res.data.data.intrusion.within_five_days
                breakIn[2]=res.data.data.intrusion.within_six_days
                breakIn[3]=res.data.data.intrusion.within_seven_days
                breakIn[4]=res.data.data.intrusion.within_eight_days
                breakIn[5]=res.data.data.intrusion.within_nine_days
                breakIn[6]=res.data.data.intrusion.within_ten_days
                breakIn[7]=res.data.data.intrusion.within_eleven_days
                breakIn[8]=res.data.data.intrusion.within_twelve_days
                breakIn[9]=res.data.data.intrusion.within_thirteen_days
                // 老人性别比例图
                genderRateChart.setOption({
                  series:{
                    data:[   //饼图数据——每个模块的名字和值
                      {value:male_OldPeople,name:'男性'},
                      {value:female_OldPeople,name:'女性'}
                    ],
                  }
                })
                // 情绪图
                emotionChart.setOption({
                  series: [
                    {
                      type: 'bar',
                      name: '愤怒',
                      data: [
                        {value:emotion[0],name:'愤怒'}
                      ],
                      barMaxHeight: 20,
                      label: {
                        show: true,
                        position: 'inside'
                      },
                    },
                    {
                      type: 'bar',
                      name: '厌恶',
                      data: [
                        {value:emotion[1],name:'厌恶'}
                      ],
                      barMaxWidth: 20,
                      label: {
                        show: true,
                        position: 'inside'
                      },
                    },
                    {
                      type: 'bar',
                      name: '恐慌',
                    data: [
                      {value:emotion[2],name:'恐慌'}
                      ],
                      barMaxWidth: 20,
                      label: {
                        show: true,
                        position: 'inside'
                      },
                    },
                    {
                      type: 'bar',
                      name: '高兴',
                      data: [
                        {value:emotion[3],name:'高兴'}
                      ],
                      barMaxWidth: 20,
                      label: {
                        show: true,
                        position: 'inside'
                      },
                    },
                    {
                      type: 'bar',
                      name: '平静',
                      data: [
                      {value:emotion[4],name:'平静'}
                    ],
                    barMaxWidth: 20,
                    label: {
                      show: true,
                      position: 'inside'
                    },
                  },
                  {
                    type: 'bar',
                    name: '伤心',
                    data: [
                    {value:emotion[5],name:'伤心'}
                    ],
                    barMaxWidth: 20,
                    label: {
                      show: true,
                      position: 'inside'
                    },
                  },
                  {
                    type: 'bar',
                    name: '惊讶',
                    data: [
                      {value:emotion[6],name:'惊讶'}
                    ],
                    barMaxWidth: 20,
                    label: {
                      show: true,
                      position: 'inside'
                    },
                  },
                ],
                })
                // 摔倒闯入
                alertChart.setOption({
                  series: [
                    {
                      type: 'bar',
                      name:'摔倒报警',
                      show:true,
                      data: fall,
                      barGap: '100%',
                      barCategoryGap: '40%'
                    },
                    {
                      type: 'line',
                      name:'闯入报警',
                      show:true,
                      data: breakIn,
                      barGap: '100%',
                      barCategoryGap: '40%',
                      symbolSize: 10,
                      itemStyle: {
                        normal: {
                          lineStyle: {
                            width:5
                          },
                        }
                      }
                    },
                  ],})
              }
            }

          })
    },
    // 绘制老人性别比例图——饼图
    initGenderRateCharts() {
      genderRateChart = echarts.init(document.getElementById('genderRate'));
      // 绘制图表
       genderRateChart.setOption({
        // 饼图数据
        series:{
          name:'老人性别比例',
          type: 'pie',   //echarts图的类型   pie代表饼图
          eight: 100,
          weight: 100,
          radius: '70%',   //饼图中饼状部分的大小所占整个父元素的百分比
          center: ['50%', '50%'],   //整个饼图在整个父元素中的位置

          itemStyle: {
            normal: {
              label: {
                show: true,//饼图上是否出现标注文字 标注各模块代表什么  默认是true
                position: 'inner',//控制饼图上标注文字相对于饼图的位置  默认位置在饼图外
              },
              labelLine: {
                show: true//官网demo里外部标注上的小细线的显示隐藏    默认显示
              }
            }
            },
        },
        //饼图中各模块的颜色
        color: ['#7cb5ec', '#FF9999'],
        // 标题
        title: {
          x: 'center',//x轴方向对齐方式
        },
        //鼠标划过时饼状图上显示的数据
        tooltip: {
          trigger: 'item',
          formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        // 图例 标注各种颜色代表的模块
        legend: {
          data: ['男性', '女性'],
          left:'10%',
          orient: 'vertical',
          top: 'center',
          icon: 'circle',
          show: true,
          itemGap: 20,
          right: -10,
          textStyle: {
            color: '#4d488e',
            fontWeight: 'normal',
            fontFamily: '宋体',
            rich: {
              a: {
                width: 200,
              },
              b: {
                width: 20,
                align: 'right'
              },
            },
          },
        },
      })
    },
    // 绘制情绪状况图
    initEmotionCharts() {
      emotionChart = echarts.init(document.getElementById('emotion'));
      emotionChart.setOption({
        legend: {
          orient: 'horizontal',
          left: 0,
          right: 0,
          height: 30,
          weight: 40,
          icon: 'circle',
          data: ['愤怒', '厌恶', '恐慌', '高兴', '平静', '伤心', '惊讶'],
          show: true
        },
        color: ['#d95850', '#a092f1', '#2e4783', '#ff6347', '#a4d8c2', '#82b6e9', '#fad860'],
        tooltip: {},
        xAxis: {
          type: 'value',
          show: false
        },
        yAxis: {
          how: false,
          type: 'category'
        },
        grid: {
          left: 6,
          top: 40,   
        },
      });
    },
    // 绘制摔倒和闯入信息图
    initAlertCharts() {
      alertChart = echarts.init(document.getElementById('alert'));
      alertChart.setOption({
        tooltip: {
        },
        color: [ '#7bd9a5','#8fd3e8'],
        xAxis: {
          data: ['4日', '5日', '6日', '7日', '8日', '9日', '10日', '11日', '12日', '13日'],
          splitNumber: 10,
          axisTick: {
            show: true,
            alignWithLabel: true
          }
        },
        legend: {
          data: ['报警数', '闯入数']
        },
        yAxis: [
          {
            name: '报警数',
            type: 'value',
            min: 0,
            max: 15,
            interval: 1,
            show: true,
            axisTick: {
              show: false,
              alignWithLabel: true
            }
          },
          {
            name: '闯入数',
            type: 'value',
            min: 0,
            max: 15,
            interval: 1,
            show: true,
            xisTick: {
              show: false,
              alignWithLabel: true
            }
          },
        ],
        grid: {
          right: '15%',
          left: '15%',
          top: '15%',
          bottom: '15%',
        },
      });
    },
  },
  mounted() {
    // 初始化并获取数据
    this.connect()
    // 绘制老人性别比例图
    this.initGenderRateCharts()
    // 绘制老人情绪状况图
    this.initEmotionCharts()
    // 绘制摔倒报警和闯入信息图
    this.initAlertCharts()
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