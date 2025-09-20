<template>
  <table id="portfolio">
    <thead>
        <tr>
      <th>Name</th>
      <th>Amount</th>
      <th>1 day %</th>
      <th>Since purchase</th>
      <th>Since purchase %</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="stock in this.portfolio" :key="stock.symbol">
        <td>{{ stock.symbol }}</td>
        <td>{{ stock.amount }}</td>
        <td>{{ (stock.diff_day ? stock.diff_day : "N/A") }}</td>
        <td>{{ (stock.since_purchase ? stock.since_purchase.toFixed(2) : "N/A") }}</td>
        <td>{{ (stock.since_purchase_percentage ? stock.since_purchase_percentage.toFixed(2) : "N/A")}}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import { Vue, Component, Prop } from "vue-property-decorator";

@Component
export default class UserPortfolio extends Vue {
  stocks = [];
  @Prop() portfolio;

}
</script>

<style scoped lang="scss">

#portfolio{
    margin: 16px 0;
    width: 100%;
    border-collapse: collapse;
}

tbody tr:nth-child(odd){
    background-color: var(--broken-white);
}

td, th{
    padding: 7.5px 0px;
}


</style>
