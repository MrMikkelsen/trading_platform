<template>
  <div>
    <div class="group-page">
      <TimeBlock id="time-block" />
      <UserSaldo id="saldo-block" />
      <router-view class="group-page-data-container" ></router-view>
      <UserOverview id="user-overview" class="group-page-data-container" />
    </div>
  </div>
</template>

<script>
import { Vue, Component } from "vue-property-decorator";
import TimeBlock from "./TimeBlock";
import UserSaldo from "./UserSaldo";
import StockOverview from "./StockOverview";
import StockDetails from "./StockDetails";
import UserOverview from "./UserOverview";


@Component({
  components: {
    TimeBlock,
    UserSaldo,
    StockOverview,
    StockDetails,
    UserOverview,
  },
})
export default class GroupPage extends Vue {}
</script>

<style scoped lang="scss">
.group-page {
  display: grid;
  grid-gap: 25px;
  grid-template-columns: 49% 49%;
  grid-template-rows: auto auto;
  grid-template-areas:
    "time saldo"
    "stocks data";
}

#time-block {
  grid-area: time;
}
#saldo-block {
  grid-area: saldo;
}
#stock-overview {
  grid-area: stocks;
}
.group-page-data-container{
  padding: 1.5em;
  background-color: white;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
  border-radius: 5px;
  min-height: 50vh!important;
}
</style>
