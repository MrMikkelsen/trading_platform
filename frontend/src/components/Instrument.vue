<template>
  <div class="stocks stock-data" :class="`${symbol}`">
    <p class="stock-instrument" @click="goToStockDetails">{{ symbol }}</p>
    <p class="sell">{{ singleStock.bidMedian || (stockData === null ? "Closed" :"Closed" )}}</p>
    <p class="buy">{{ singleStock.askMedian || (stockData === null ? "Closed" :"Closed" )}}</p>
  </div>
</template>

<script>
import { Vue, Component, Prop, Watch } from "vue-property-decorator";

@Component
export default class Instrument extends Vue {
  @Prop() symbol;
  @Prop() stockData;
  singleStock = {};


  @Watch("stockData")
  onChange(newStockData) {

    
    this.singleStock =
      newStockData.filter((stock) => {
        //check if new number is higher or lower
        if (newStockData) {
          let stockIsOpen =
            this.singleStock.bidVolume != 0 && this.singleStock.askVolume != 0;
          if (stockIsOpen) {
            this.stockClosed(false);
            if (stock.askOpen > this.singleStock.askOpen) {
              document
                .querySelector(`.${this.symbol} .sell`)
                .classList.remove("red");
              document
                .querySelector(`.${this.symbol} .sell`)
                .classList.add("green");
            } else if (stock.askOpen < this.singleStock.askOpen) {
              document
                .querySelector(`.${this.symbol} .sell`)
                .classList.remove("green");
              document
                .querySelector(`.${this.symbol} .sell`)
                .classList.add("red");
            }
            if (stock.bidOpen > this.singleStock.bidOpen) {
              document
                .querySelector(`.${this.symbol} .buy`)
                .classList.remove("red");
              document
                .querySelector(`.${this.symbol} .buy`)
                .classList.add("green");
            } else if (stock.bidOpen < this.singleStock.bidOpen) {
              document
                .querySelector(`.${this.symbol} .buy`)
                .classList.remove("green");
              document
                .querySelector(`.${this.symbol} .buy`)
                .classList.add("red");
            }
          } else {
            this.stockClosed(true);
          }
        }
        return stock.symbol === this.symbol;
      })[0] || "";
  }

  goToStockDetails() {
    this.$router.push(`${this.$router.currentRoute.path}/${this.symbol}`);
  }

  stockClosed(closed) {
    if (closed) {
      document.querySelector(`.${this.symbol} .sell`).classList.add("grey");
      document.querySelector(`.${this.symbol} .buy`).classList.add("grey");
      document
        .querySelector(`.${this.symbol} .stock-instrument`)
        .classList.add("closed-stock");
    } else {
      document.querySelector(`.${this.symbol} .sell`).classList.remove("grey");
      document.querySelector(`.${this.symbol} .buy`).classList.remove("grey");
      document
        .querySelector(`.${this.symbol} .stock-instrument`)
        .classList.remove("closed-stock");
    }
  }

  async fetchSingleStock(symbol) {
    let res = await fetch(`api/public/${symbol}`);
    res = await res.json();
    res = res.result[0];
    this.updateStockData(res);
  }
}
</script>

<style scoped lang="scss">
.stock-instrument {
  cursor: pointer;
}
.green {
  color: rgb(82, 177, 114) !important;
}
.red {
  color: rgb(240, 81, 81);
}
.grey {
  color: rgb(58, 58, 58) !important;
  text-decoration: line-through;
}
.closed-stock {
  color: rgb(0, 0, 0) !important;
  font-style: oblique;
}
.closed-stock::after {
  content: " - Closed";
}
</style>
