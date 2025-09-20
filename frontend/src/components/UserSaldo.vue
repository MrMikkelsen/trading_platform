<template>
  <div class="saldo-overview">
    <div class="saldo">
      <p>BALANCE</p>
      <h3>{{ swedishPriceFormat($store.state.groupData.data.balance)}} </h3>
    </div>
    <div class="saldo">
      <p>PROFIT / LOSS</p>
      <h3>{{ swedishPriceFormat($store.state.groupData.data.profit)}} </h3>
    </div>
     <div class="saldo">
      <p>TOTAL VALUE</p>
      <h3>{{ swedishPriceFormat($store.state.groupData.data.current_portfolio_value + $store.state.groupData.data.balance)}} </h3>
    </div>
  </div>
</template>

<script>
import { Vue, Component } from "vue-property-decorator";

@Component
export default class UserSaldo extends Vue {

  swedishPriceFormat(number) {
      return new Intl.NumberFormat('sv-SE', {style: 'currency', currency: 'SEK'}).format(number);
  }
  
}
</script>

<style scoped lang="scss">
.saldo-overview {
  border-radius: 5px;
  padding: 1.5em;
  background-color: white;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
}
.saldo{
    display: inline-block;
  width: calc(100% / 3);
  text-align: left;
}

.sek {
  font-size: 11px;
}
p {
  color: var(--saldo-color);
  font-size: 1em;
}
h3 {
  color: var(--darker-blue);
  font-size: 1.6rem;
  font-weight: 500;
}
</style>
