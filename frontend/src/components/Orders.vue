<template>
  <div class="user-history">
    <div id="bought">
      <div class="all-history">
        <div class="history">
          <p class="instrument">Symbol</p>
          <p class="amount">Amount</p>
          <p class="price">Price</p>
          <p class="total-price">Total price</p>
          <p class="type">Type</p>
          <p class="status">Status</p>
        </div>
        <div v-for="(order, i) in orders" :key="i">
          <div class="history history-data" :class="`${order.order_type}`">
            <p class="instrument">{{ order.symbol }}</p>
            <p class="amount">{{ order.amount }}</p>
            <p class="price">{{  (order.price).toFixed(2) }}</p>
            <p class="total-price">{{ (order.amount * order.price).toFixed(2) }}</p>
            <p class="type">{{order.order_type}}</p>
            <p class="status">{{ order.order_status }} </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Vue, Component, Prop, Watch } from "vue-property-decorator";

@Component
export default class Orders extends Vue {
  @Prop() orders
  @Prop() renderVersion
  activeOrders = [];

  @Watch("renderVersion")
    onStopLossesChange(){
      this.updateData()
    }


    updateData(){
      this.activeOrders = this.orders;
    }
  
  created() {
    this.updateData()
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
  grid-template-columns: 16.6% 16.6% 16.6% 16.6% 16.6% 16.6%;
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
.total-price {
  grid-column: 4/5;
}
.type {
  grid-column: 5/6;
}
.status{
  grid-column: 6/7;
}
.history-data {
  font-size: 16px;
  font-weight: 400;
  padding: 10px 0;
}
.active {
  color: var(--darker-blue);
  font-weight: 500;
}
.completed {
  color: var(--saldo-color);
}
</style>
