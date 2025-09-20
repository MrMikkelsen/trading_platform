<template>
  <div class="all-stocks">
    <div class="stocks">
      <p class="instrument">Ticker</p>
      <p class="sell">Bid</p>
      <p class="buy">Ask</p>
    </div>

    <div v-if="this.allStockData !== null">
      <div v-for="type in Object.keys(allStockData)" :key="type">
        <h3 class="type">{{ type }}s</h3>
        <Instrument
          v-for="(stock, i) in allStockData[type]"
          :key="i"
          :symbol="stock.symbol"
          :stockData="allStockData[type]"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { Vue, Component, Watch } from "vue-property-decorator";
import Instrument from "./Instrument";

@Component({
  components: {
    Instrument,
  },
})
export default class StockOverview extends Vue {
  allStockData = null;

  interval = null;

  get symbols() {
    return this.$store.state.allSymbols;
  }

  @Watch("allStockData")
  onChange(newVal) {
    this.allStockData = newVal;

  }

  created() {
    if (this.$store.state.stockData) {
      this.allStockData = this.$store.state.stockData;
    }

    this.dataTimer();
  }

  dataTimer() {
  this.interval = setInterval(async () => {
    await fetch(`api/data/stocks`, {
      method: "GET",
      headers: {"Content-Type": "application/json"},
    })
    .then(res => {
      if (res.status === 204) {
        this.allStockData = {};
          for (const symbol of this.symbols) {
            this.allStockData[symbol] = [{ bidMedian: null, askMedian: null }];
          }
          return;
      }
      return res.json();
    })
    .then(data => {
      if (!data) {
        return;
      }
      const allStockDataTemp = {};
      for (const stock of data.data) {
        if (allStockDataTemp[stock.symbol]) {
          allStockDataTemp[stock.symbol] = [
            ...allStockDataTemp[stock.symbol],
            stock,
          ];
        } else {
          allStockDataTemp[stock.symbol] = [stock];
        }
      }
      this.allStockData = allStockDataTemp;
    })
    .catch();
  }, 3000)
}

  beforeDestroy() {
    this.$store.commit("setStockData", this.allStockData);
    if (this.interval) {
      clearInterval(this.interval);
    }
  }
}
</script>

<style scoped lang="scss">
.all-stocks {
  padding: 1em;
  background-color: white;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
  border-radius: 5px;
}
.type{
  text-align: center;
  text-transform: capitalize;
  margin: 0.5rem 0;
  color: var(--darker-blue);

}
.stocks {
  display: grid;
  padding: 0.5em;
  border-bottom: 1px solid var(--main-bg-color);
  grid-template-columns: 30% 30% 30%;
  text-align: center;
  font-size: 18px;
  font-weight: 500;
}
.instrument {
  grid-column: 1/2;
}
.sell {
  grid-column: 2/3;
}
.buy {
  grid-column: 3/4;
}
.stock-data {
  font-size: 16px;
  font-weight: 400;
  padding: 10px 0;
}
</style>
