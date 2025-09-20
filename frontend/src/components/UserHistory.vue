<template>
  <div class="user-history">
    <div id="bought">
      <div class="all-history">
        <div class="history">
          <p class="instrument">Ticker</p>
          <p class="amount">Amount</p>
          <p class="price">Price</p>
          <p class="type">Type</p>
        </div>
        <div v-for="(history, i) in history" :key="i">
          <div class="history history-data" :class="`${history.type}`">
            <p class="instrument">{{ history.symbol }}</p>
            <p class="amount">{{ history.amount }}</p>
            <p class="price">{{ history.price.toFixed(2) }}</p>
            <p class="type">{{ history.order_type }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Vue, Component } from "vue-property-decorator";

@Component
export default class UserHistory extends Vue {
  history = [];

  created() {
    this.history = this.$store.state.groupData.history;
  }
}
</script>

<style scoped lang="scss">
.all-history {
  padding: 1em;
  background-color: white;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
  border-radius: 5px;
}

.history {
  display: grid;
  padding: 0.5em;
  border-bottom: 1px solid var(--main-bg-color);
  grid-template-columns: 25% 25% 25% 25%;
  text-align: center;
  font-size: 18px;
  font-weight: 500;
  max-width: 80%;
  margin: 0 auto;
}
.instrument {
  grid-column: 1/2;
}
.amount {
  grid-column: 2/3;
}
.price {
  grid-column: 3/4;
}
.type {
  grid-column: 4/5;
}
.history-data {
  font-size: 16px;
  font-weight: 400;
  padding: 10px 0;
}
.purchase {
  color: var(--darker-blue);
  font-weight: 500;
}
.sale {
  color: var(--saldo-color);
}
</style>
