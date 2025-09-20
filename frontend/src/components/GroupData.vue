<template>
  <div class="groups">
    <p class="group" @click="goToGroupPage(group.token)">{{ this.group.name }}</p>
    <p class="numberoftrades">{{ group.data.numberOfTrades || 0 }}</p>
    <p class="balance" @click="changeSaldo">{{ this.swedishPriceFormat(this.group.data.balance) || 0 }}</p>
    <div>
      <p class="numberofstocks">{{ this.group.data.numberOfStocks || 0 }}</p>
    </div>
    <p class="pc">{{ swedishPriceFormat(group.PL) }}</p>
    <div id="goodwill-handler">
      <div v-if="!editGoodwill" class="goodwill-container">
       <p> {{ group.data.goodwill || 0 }}</p>
       <p v-if="this.$store.state.user.role === 'admin'" class="pointer" @click="() => {this.editGoodwill = !this.editGoodwill}">Edit</p>
      </div>
      <div v-if="editGoodwill" class="goodwill-container">
        <input type="number" v-model="amount" placeholder="Amount" id="goodwill-inputfield"/>
        <p class="pointer"  @click="() => this.handleGoodwillRequest()">Save</p>
        <p class="pointer" @click="() => this.editGoodwill = !this.editGoodwill ">Cancel</p>
      </div>
    </div>
    <p class="rollingAvg">{{this.group.uniqueTrades}}</p>
    <p class="tradeLengthAvg"> {{this.group.avgTradeLength.toFixed(2)}}  </p>
    <p class="sdReturns"> {{this.group.stdPL.toFixed(2)}}</p>
    <p class="skewnessPl"> {{this.group.skewnessPL.toFixed(2)}} </p>
             
  </div>
</template>

<script>
import { Vue, Component, Prop } from "vue-property-decorator";

@Component
export default class GroupData extends Vue {
  @Prop() group;
  editGoodwill = false;
  amount = null;

  goToGroupPage(token) {
    this.$router.push({
      path: `/team/${token}`,
    });
  }

  async handleGoodwillRequest() {
    if (this.amount === null) return;

    let adminToken = this.$store.state.user.token;
    let groupToken = this.group.token;
    let amount = this.amount;

    await fetch(`api/account/add_goodwill/${groupToken}/${amount}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({"api_key": adminToken}),
    });

    this.editGoodwill = !this.editGoodwill;
    this.amount = null;
}

  swedishPriceFormat(number) {
      return new Intl.NumberFormat('sv-SE', {style: 'currency', currency: 'SEK'}).format(number);
  }

  changeSaldo() {
    console.log("TODO");
  }
}
</script>

<style scoped lang="scss">
.group,
.balance {
  cursor: pointer;
}

.goodwill-container{
  display: flex;
  justify-content: space-around;
}

input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
#goodwill-inputfield{
  width: 35%;
}

.group:hover,
.balance:hover {
  background-color: #e7eef5;
}

.group-data > * {
  background-color: white;
  padding: 5% 10%;
  margin: 0 0;
  color: var(--darker-blue);
  text-align: center;
  justify-content: center;
  font-weight: 0;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
}
</style>
