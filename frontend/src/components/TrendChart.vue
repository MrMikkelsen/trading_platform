<template>
  <div id="trend-chart-options-container">
    <span class="pointer" @click="setTimeView(7)"> 7 Days </span> |
    <span class="pointer" @click="setTimeView(30)"> 30 Days </span> |
    <span class="pointer" @click="setTimeView(90)"> 90 Days </span> |
    <span class="pointer" @click="setTimeView(0)"> Since start </span>
    <div id="trend-chart-graph-container">
      <TrendChart
        id="trend-chart-graph"
        :datasets="[
          {
            data: groupData,
            smooth: true,
            fill: false
          }
        ]"
        :labels="{
          xLabels: xLabels,
          yLabels: 5,
          yLabelsTextFormatter: (val) => {
            if(val){
              return `${val.toFixed(2)}%`;
            }
          }
        }"
        :grid="{
          verticalLines: true,
          verticalLinesNumber: 1,
          horizontalLines: true,
          horizontalLinesNumber: 1
        }"
      />
      <h3 id="trend-chart-details">
        {{ -percentage.toFixed(2) }} % | {{ swedishPriceFormat(-currency) }} | {{ daysDisplayed }} Days
      </h3>
    </div>
  </div>
</template>

<script>
import { Vue, Component, Prop, Watch } from "vue-property-decorator";
import TrendChart from "vue-trend-chart";
Vue.use(TrendChart);

@Component
export default class MyTrendChart extends Vue {
  @Prop() trendData;
  groupData = [];
  xLabels = [];
  render = false;
  startView = 0;
  percentage = 0;
  currency = 0;
  daysDisplayed = 0;
  monthsShort = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
  ];

  @Watch("trendData.length")
  onTrendDataChange() {
    this.setTimeView(this.daysDisplayed);
  }

  updateData() {
    let tempArr = [];
    let tempLabels = [];
    let originalInvestment = false;
    if (!this.daysDisplayed) {
      this.daysDisplayed = Math.ceil(this.trendData.length);
    }
    if (this.floatingDays) {
      this.daysDisplayed++;
    }
    for (let i = this.startView; i < this.trendData.length; i++) {
      if (i >= this.startView && tempArr.length < this.daysDisplayed) {
        tempArr.push(this.trendData[i]["profit_percentage"]);
        if (!originalInvestment && this.trendData[i]["profit_percentage"] !== 0) {
          originalInvestment =
            (this.trendData[i]["profit_currency"] / this.trendData[i]["profit_percentage"]) * 100;
        }
        const date = new Date(this.trendData[i]["gmtTime"]);
        tempLabels.push(date.getDate() + " " + this.monthsShort[date.getMonth()]);
      } else {
        break;
      }
    }
    let currentProfit = this.trendData[this.trendData.length - 1]["profit_currency"];
    let lastKnowProfit = this.trendData[this.startView ? this.startView - 1 : 0]["profit_currency"];
    this.currency = (currentProfit - lastKnowProfit) * -1;
    if (!parseFloat((this.currency / originalInvestment) * 100)) {
      this.percentage = 0;
    } else {
      this.percentage = parseFloat((this.currency / originalInvestment) * 100);
    }
    // Reduce the number of labels/data points if too many.
    if (tempLabels.length > 5) {
      const interval = Math.floor(tempLabels.length / 5);
      tempLabels = tempLabels.filter((_, idx) => idx % interval === 0 || idx === 0 || idx === tempLabels.length - 1);
      tempArr = tempArr.filter((_, idx) => idx % interval === 0 || idx === 0 || idx === tempArr.length - 1);
    }
    this.groupData = tempArr;
    this.xLabels = tempLabels;
    this.render = true;
  }

  swedishPriceFormat(number) {
    return new Intl.NumberFormat("sv-SE", {
      style: "currency",
      currency: "SEK",
    }).format(number);
  }

  /**
   * Updates startView which is where in trendData to start when retrieving values for the graph.
   * if days === 0, we start from the beginning and show all the data.
   * Otherwise, we show the last 'days' of data.
   */
  setTimeView(days) {
    if (days === 0) {
      this.startView = 0;
      this.floatingDays = true;
    } else {
      this.floatingDays = false;
      this.startView = days > this.trendData.length ? 0 : this.trendData.length - days;
    }
    this.daysDisplayed = days;
    this.updateData();
  }

  created() {
    this.render = true;
    this.updateData();
  }
}
</script>

<style scoped lang="scss">
#trend-chart-options-container {
  margin-bottom: 30px;
  margin-top: 30px;
}

#trend-chart-graph path {
  fill: none !important;
}

#trend-chart-graph {
  height: 255px !important;
}

#trend-chart-details {
  margin-bottom: 30px;
  margin-top: 30px;
}

.stroke {
  stroke: var(--darker-blue);
  stroke-width: 2;
}
</style>
