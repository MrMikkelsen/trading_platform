<template>
  <div id="admin-page">
    <!-- <h1>{{ username.slice(0, 5).toUpperCase() }} OVERVIEW</h1> -->
    <header>
      <h2>Current time: {{ this.time }}</h2>
      <div class="controls">
        <select class="filter" @change="this.changeOffset">
          <option value="0">Since start</option>
          <option value="1">Daily</option>
          <option value="7">Weekly</option>
          <option value="31">Monthly</option>
        </select>

        <button7
          v-if="this.$store.state.user.role === 'admin'"
          @click="openResetTeamHistoryPopup"
          class="button--main"
        >
          Reset team's history
        </button7>
        <button
          v-if="this.$store.state.user.role === 'admin'"
          @click="openResetDatastreamPopup"
          class="button--main"
        >
          Reset data stream
        </button>

        <ResetTeamHistoryPopup
          v-if="showResetTeamHistoryPopup"
          :allGroups="allGroups"
          @close="closePopup"
        />
        <ResetDatastreamPopup
          v-if="showResetDatastreamPopup"
          @close="closePopup"
        />
      </div>
    </header>

    <div class="groups-wrapper">
      <div class="groups">
        <p class="group">GROUP</p>
        <p class="numberoftrades"># OF TRADES</p>
        <p class="balance">BALANCE</p>
        <p class="numberofstocks"># OF SECURITIES TRADED</p>
        <p class="pl">P/L</p>
        <p class="goodwill">GOODWILL</p>
        <p class="rollingAvg">ROLLING NUMBER OF TRADES</p>
        <p class="tradeLengthAvg">AVG. LENGTH OF TRADE (DAYS)</p>
        <p class="sdReturns">ROLLING SD ON RETURNS</p>
        <p class="skewnessPl">SKEWNESS OF P/L</p>
      </div>
      <div>
        <GroupData
          class="group-data"
          v-for="(group, i) in allGroups"
          :key="i"
          :group="group"
        />
      </div>
    </div>
    <section class="more-data-section">
      <router-view class="group-page-data-container"></router-view>
      <TeamsCumulativeReturns />
    </section>
    <TimeAccelerator v-if="this.$store.state.user.role === 'admin'" />
    <TimePauseButton v-if="this.$store.state.user.role === 'admin'" />
  </div>
</template>

<script>
import { Vue, Component } from "vue-property-decorator";
import GroupData from "./GroupData";
import TimeAccelerator from "./TimeAccelerator";
import TimePauseButton from "./TimePauseButton.vue";
import TeamsCumulativeReturns from "./TeamsCumulativeReturns.vue";
import ResetTeamHistoryPopup from "./ResetTeamHistoryPopup.vue";
import ResetDatastreamPopup from "./ResetDatastreamPopup.vue";
import StockOverview from "./StockOverview";
import StockDetails from "./StockDetails";

@Component({
  components: {
    GroupData,
    TimeAccelerator,
    TimePauseButton,
    TeamsCumulativeReturns,
    ResetDatastreamPopup,
    ResetTeamHistoryPopup,
    StockOverview,
    StockDetails,
  },
})
export default class AdminPage extends Vue {
  groupInterval = null;
  allGroups = {};
  filter = "Daily";
  showResetTeamHistoryPopup = false;
  showResetDatastreamPopup = false;
  time = null;
  offset = "0";

  created() {
    this.groupTimer();
    this.timeTimer();
  }

  beforeDestroy() {
    if (this.groupInterval) clearInterval(this.groupInterval);
  }

  closePopup() {
    this.showResetTeamHistoryPopup = false;
    this.showResetDatastreamPopup = false;
  }

  openResetDatastreamPopup() {
    this.showResetDatastreamPopup = true;
  }

  openResetTeamHistoryPopup() {
    this.showResetTeamHistoryPopup = true;
  }

  groupTimer() {
    this.groupInterval = setInterval(async () => {
      await fetch(
        `api/feed/groupData${
          this.offset === "0" ? "" : `/offset=${this.offset}`
        }`
      )
        .then((res) => {
          if (res.status === 204) {
            return Promise.reject("No Content");
          }
          return res.json();
        })
        .then((data) => {
          this.allGroups = data;
        })
        .catch((e) => {
          if (e !== "No Content") {
            console.log(e);
          }
        });
    }, 10000);
  }

  timeTimer() {
    setInterval(async () => {
      await fetch("time/currentTime")
        .then((res) => {
          if (res.status === 204) {
            return Promise.reject("No Content");
          }
          return res.json();
        })
        .then((data) => {
          this.time = data.data;
        })
        .catch((e) => {
          if (e !== "No Content") {
            console.log(e);
          }
        });
    }, 2000);
  }

  changeOffset(event) {
    this.offset = event.target.value;

    clearInterval(this.groupInterval); // clear current interval

    this.groupInterval = setInterval(async () => {
      // start new interval with updated offset value
      await fetch(
        `api/feed/groupData${
          this.offset === "0" ? "" : `/offset=${this.offset}`
        }`
      )
        .then((res) => {
          if (res.status === 204) {
            return Promise.reject("No Content");
          }
          return res.json();
        })
        .then((data) => {
          this.allGroups = data;
        })
        .catch((e) => {
          if (e !== "No Content") {
            console.log(e);
          }
        });
    }, 10000);
  }
}
</script>

<style lang="scss">
h2 {
  color: var(--darker-blue);
  margin: 1rem 0;
}
header {
  display: flex;
  justify-content: space-between;
}
.button--main {
  background-color: var(--darker-blue);
  color: #fff;
  border: none;
  padding: 10px;
  text-transform: uppercase;
  font-weight: 700;
  box-shadow: 1px 1px 2px 0 var(--darker-blue);
  margin: 0 10px;
  border-radius: 5px;
}
.button--main:hover {
  background-color: var(--darker-blue-light);
  box-shadow: 1px 1px 2px 0 var(--darker-blue-light);
  cursor: pointer;
}
</style>

<style scoped lang="scss">
.controls {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 16px;
}

.filter {
  border: none;
  box-shadow: 1px 1px 2px 0 rgba(0, 0, 0, 0.25);
  border-radius: 5px;
  outline-color: var(--darker-blue);
  margin: 0 10px;
}

.groups-wrapper {
  overflow-x: auto;
}
.groups {
  display: grid;
  grid-gap: 1%;
  border-bottom: 0.5px solid var(--main-bg-color);
  grid-template-columns: repeat(10, 16vw);
}

.group {
  grid-column: 1/2;
}
.numberoftrades {
  grid-column: 2/3;
}
.balance {
  grid-column: 3/4;
}
.numberofstocks {
  grid-column: 4/5;
}
.pl {
  grid-column: 5/6;
}
.goodwill {
  grid-column: 6/7;
}

.rollingAvg {
  grid-column: 7/8;
}
.tradeLengthAvg {
  grid-column: 8/9;
}
.sdReturns {
  grid-column: 9/10;
}
.skewnessPl {
  grid-column: 10/11;
}
.groups > * {
  background-color: white;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
  padding: 5% 10%;
  border-radius: 5px 5px 0 0;
  color: var(--darker-blue);
  font-size: 15px;
  font-weight: 700;
  text-align: center;
}

.group-page-data-container {
  background-color: white;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
  border-radius: 5px;
}

.more-data-section {
  width: 100%;
  margin: 2.4rem 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-gap: 2.4rem;
}
</style>
