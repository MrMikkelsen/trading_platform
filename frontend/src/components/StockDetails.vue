<template>
  <div id="company-details">
    <p class="back" @click="goBack()">Back</p>
    <TradingVue
      id="chart-area"
      :title-txt="this.getSymbol()"
      :data="this.chart"
      :width="this.width"
      :color-back="this.colorBack"
      :color-grid="this.colorGrid"
      :color-text="this.colorText"
      :color-title="this.colorText"
      :color-cross="this.colorText"
      :color-candle-dw="this.colorCandleDown"
      :color-wick-dw="this.colorCandleDown"
      :color-candle-up="this.colorCandleUp"
      :color-wick-up="this.colorCandleUp"
      :color-vol-up="this.colorVolUp"
      :color-vol-dw="this.colorVolDown"
    />
  </div>
</template>

<script>
import { Vue, Component } from "vue-property-decorator";
import TradingVue from "trading-vue-js";
@Component({
  components: {
    TradingVue,
  },
})
export default class StockDetails extends Vue {
  chart = { chart: { type: "Candles", data: [] } };
  width = window.innerWidth / 2 - 200;
  height = 200;
  colorBack = "#fff";
  colorGrid = "#d4e0ec"; // --broken-white
  colorText = "#15416b"; // --darker-blue
  colorCandleUp = "#15416b";
  colorVolUp = "rgba(21, 65, 107, 0.25)";
  colorCandleDown = "#8aa9c5";
  colorVolDown = "rgba(138, 169, 197, 0.25)";

  interval = null;

  goBack() {
    this.$router.back();
  }

  getSymbol() {
    return this.$router.history.current.params.symbol;
  }

  // FROM BACKEND TO THE CHART
  // result = result.map((o : any) => {
  //   o.time = new Date(o.time);
  //   o.time.setHours(o.time.getHours() + 2);
  //   let arr = [o.time, o.askOpen, o.askHigh, o.askLow, o.askClose, o.askVolume];
  //   return arr;
  // });

  // let chart = {
  //   chart: {
  //     type: "Candles",
  //     data: result,
  //     indexBased: true,
  //     tf: "1m",
  //     name: req.params.symbol, // Or template, e.g. "RSI, $length"
  //   },
  async fetchStocksFromLastWeek(daysBack = 30) {
    // ${this.getSymbol()}/${daysBack}/forChart

    let data = await fetch(`api/public/${this.getSymbol()}/${daysBack}/forChart`);

    if (data.ok) {
      const json = await data.json();
      this.chart = json;
    }
  }

  created() {
    this.fetchStocksFromLastWeek();
  }
}
</script>

<style scoped land="scss">
#company-details {
  padding: 1.5em;
  background-color: white;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
  border-radius: 5px;
}
h1 {
  margin: 2rem 2rem 0;
  color: var(--darker-blue);
}
p {
  margin: 1rem 2rem;
  color: var(--darker-blue);
}
#chart-area {
  margin: 2rem;
  padding: 2rem;
  box-sizing: border-box;
}
.back {
  font-weight: 800;
  text-align: right;
}

.back:hover {
  cursor: pointer;
}
</style>
