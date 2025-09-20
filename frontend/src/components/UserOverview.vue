<template>
  <div>
      <div class="navbar">
        <span @click="toggleShowGroupHistory('OVERVIEW')" class="pointer"> OVERVIEW </span>
        <span @click="toggleShowGroupHistory('HISTORY')" class="pointer"> GROUP HISTORY </span>
        <span @click="toggleShowGroupHistory('TRENDCHART')" class="pointer"> PROFIT GRAPH </span>
        <span @click="toggleShowGroupHistory('STOPLOSS')" class="pointer"> STOPLOSSES </span>
        <span @click="toggleShowGroupHistory('ORDER')" class="pointer"> ORDERS </span>
        <span @click="toggleShowGroupHistory('PORTFOLIO')" class="pointer"> PORTFOLIO </span>
        <div v-if="this.showInterface === 'OVERVIEW'">
          <pie-chart v-if="renderPieChart" :chartData="chartData" :pieChartRenderVersion="pieChartRenderVersion" :options="options"></pie-chart>
        </div>
        <TrendChart v-if="this.showInterface === 'TRENDCHART'" :trendData="profitHistory" ></TrendChart>
        <UserHistory v-if="this.showInterface === 'HISTORY'" />
        <UserHistory v-if="this.showInterface === 'STOPLOSSANDORDERS'" />
        <UserPortfolio v-if="this.showInterface === 'PORTFOLIO'" :portfolio="this.$store.state.groupData.portfolio"/>
        <Stoplosses :stopLosses="stopLosses" :renderVersion="renderVersion" v-if="this.showInterface === 'STOPLOSS'" />
        <Orders :orders="orders" :renderVersion="renderVersion" v-if="this.showInterface === 'ORDER'" />

      </div>
    </div>
</template>

<script>
import { Vue, Component, Watch } from "vue-property-decorator";
import PieChart from "./PieChart";
import UserHistory from "./UserHistory";
import UserPortfolio from "./UserPortfolio";
import TrendChart from "./TrendChart";
import Stoplosses from "./Stoplosses";
import Orders from "./Orders";

@Component({
  components: {
    PieChart,
    UserHistory,
    UserPortfolio,
    TrendChart,
    Stoplosses,
    Orders,
  },
})
export default class UserOverview extends Vue {
  renderPieChart = false;
  showInterface = 'OVERVIEW'
  pieData = [];
  profitHistory = [];
  pieChartRenderVersion = 0;
  lastChartUpdate = 0;
  stopLosses = [];
  renderVersion = 0;
  portfolio = [];
  interval = undefined;

  chartData = {
    labels: null,
    datasets: [
      {
        borderWidth: 1,
        borderColor: this.$store.state.borderColorsPieChart,
        backgroundColor: this.$store.state.backgroundColorsPieChart,
        data: [],
      },
    ],
  };
  options = {
    legend: {
      display: true,
    },
    responsive: true,
    maintainAspectRatio: false,
  };

  toggleShowGroupHistory(action) {
    this.showInterface = action;
  }

  @Watch("pieData")
  onPieDataChange(val, oldVal) {
    this.chartData.labels = val.map((e) => e?.symbol);
  
    this.chartData.datasets[0].data = val.map((e) => {
      if(e.currentValue){
        return (e.currentValue).toFixed(2)}
      else{
        return 0
      }});
      
    this.renderPieChart = val.length;
    for(let i = 0 ; i < val.length ; i++){
      if(val[i].numberOfStocks !== oldVal[i]?.numberOfStocks  
        && (this.lastChartUpdate + 10000) < Date.now() ){
        this.pieChartRenderVersion++;
        this.lastChartUpdate = Date.now();
      }
      if(oldVal.length !== val.length || val[i].symbol !== oldVal[i]?.symbol  
        || (this.lastChartUpdate + 100000) < Date.now() ){
        this.pieChartRenderVersion++;
        this.lastChartUpdate = Date.now();
      }
    }
  }

  created() {
    this.Timer();
  }

  Timer() {
  this.interval = setInterval(async () => {
    await fetch(`api/feed/token=${this.$route.params.group}/groupData`)
      .then((res) => {
        if (res.status === 204) {
          // No content, skip update and wait for next interval
          return;
        }
        return res.json();
      })
      .then((data) => {
        if (data) {
          // Update component state with new data
          this.$store.dispatch("updateGroupData", data);
          this.pieData = this.$store.state.groupData.stocks;
          this.portfolio = this.$store.state.groupData.portfolio;
          this.profitHistory = this.$store.state.groupData.profit_history;
          this.orders = this.$store.state.groupData.orders;
          this.stopLosses = this.$store.state.groupData.stopLosses;
          this.renderVersion++;
        }
      })
      .catch();
  }, 3000);
}


  filterArr(array){
    return array.filter( (el) => {
      if(el.status === 'active') return el
    })
  }

  beforeDestroy() {
    if (this.interval) clearInterval(this.interval);
  }

}
</script>

<style scoped lang="scss">

.navbar {
  text-align: center;
}
span {
  margin-right: 10px;
}
</style>
