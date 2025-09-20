<template>
  <section class="cumulative-returns">
    <h3>Cumulative returns per team</h3>
    <ul class="teams">
      <li v-for="team in this.data" :key="team.name" :class="team.className">
        {{ team.name }}
      </li>
    </ul>
    <TrendChart
    v-if="!this.loading"
      id="trend-chart-graph"
      :datasets="this.data"
      :labels="{
        xLabels: this.xLabels,
      
        yLabels: 5,
        yLabelsTextFormatter: (val) => `${val.toFixed(2)}%`,
      }"
      :grid="{
        verticalLines: true,
        verticalLinesNumber: 1,
        horizontalLines: true,
        horizontalLinesNumber: 1,
      }"
    >
    </TrendChart>
  </section>
</template>

<script>
import { Vue, Component } from "vue-property-decorator";
import TrendChart from "vue-trend-chart";
Vue.use(TrendChart);

@Component
export default class TeamsCumulativeReturns extends Vue {
  loading = true;
  xLabels = [];
  data = [];
  monthsShort = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
  ];
  interval = undefined;

  created() {
    this.Timer();
  }

  beforeDestroy() {
  if(this.interval) {
    clearInterval(this.interval);
  }
}

  Timer() {
    this.interval = setInterval(async () => {
      try {
        const response = await fetch('api/feed/cumulativeData');
        if (response.status === 204) {
          return;
        }
        const data = await response.json();
        this.data = Object.entries(data.data).map((teamData, idx) => {
          return {
            name: teamData[0],
            data: teamData[1],
            smooth: true,
            className: `team-${idx}`,
          };
        });

        let tempXLabels = data.labels.map((label) => {
          const date = new Date(label);
          return date.getDate() + ' ' + this.monthsShort[date.getMonth()];
        });

        // show every 'interval' label and data point including 
        // end points so that the graph dont overflow om the x axis
        if (tempXLabels.length > 5) {
          const interval = Math.floor(tempXLabels.length / 5);
          tempXLabels = tempXLabels.filter(
            (_, idx) => idx % interval === 0 || idx === 0 || idx === tempXLabels.length - 1
          );
        }

        this.loading = false;
        this.xLabels = tempXLabels;
      } catch (err) {
        console.error(err);
      }
    }, 10000);
  }
}
</script>

<style lang="scss">
.teams {
  display: flex;
  list-style-type: none;
  margin: 1em;
}
.teams > * {
  margin-right: 2.4rem;
  font-weight: bolder;
}



.teams li{
  position: relative;
}
.teams li:before {
  content: "";  /* Add content: \2022 is the CSS Code/unicode for a bullet */
  width: 1em; /* Also needed for space (tweak if needed) */
  height: 1em;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  left: -1.2em;
  border-radius: 1em;
}

.team-0 .stroke,
.team-0:before {
  stroke: hsl(359, 100%, 50%);
  background:hsl(359, 100%, 50%);
  stroke-width: 2;
}
.team-1 .stroke,
.team-1:before {
  stroke: hsl(30, 100%, 50%);
  background:   hsl(30, 100%, 50%);
  stroke-width: 2;
}
.team-2 .stroke,
.team-2:before {
  stroke: hsl(57, 94%, 42%);
  background:   hsl(57, 90%, 42%);
  stroke-width: 2;
}
.team-3 .stroke,
.team-3::before{
  stroke: hsl(144, 96%, 41%);
  background:   hsl(144, 96%, 41%);
  stroke-width: 2;
}
.team-4 .stroke,
.team-4::before{
  
   stroke: hsl(204, 96%, 44%);
  background:   hsl(204, 96%, 44%);
  stroke-width: 2;
}
.team-5 .stroke, .team-5::before {
stroke: hsl(172, 94%, 39%);
  background:   hsl(172, 94%, 39%);
  stroke-width: 2;
}
.team-6 .stroke, .team-6::before {
  stroke: hsl(227, 100%, 50%);
  background:   hsl(227, 100%, 50%);
  stroke-width: 2;
}
.team-7 .stroke, .team-7::before {
  stroke: hsl(277, 100%, 50%);
  background:   hsl(277, 100%, 50%);
  stroke-width: 2;
}

.team-8 .stroke,
.team-8::before {
  stroke: hsl(297, 95%, 45%);
  background:   hsl(297, 95%, 45%);
  stroke-width: 2;
}
.team-9 .stroke,
.team-9:before {
  stroke: hsl(338, 100%, 50%);
  background:   hsl(338, 100%, 50%);
  stroke-width: 2;
}
.team-10 .stroke,
.team-10::before {
  stroke: black;
  background:   black;
  stroke-width: 2;
}
.team-11 .stroke,
.team-11::before {
  stroke: rgb(92, 134, 92);
  background:   rgb(92, 134, 92);
  stroke-width: 2;
}
.team-12 .stroke,
.team-12::before {
  stroke: maroon;
  background:   maroon;
  stroke-width: 2;
}
.team-13 .stroke,
.team-13:before {
  stroke: navy;
  background:   navy;
  stroke-width: 2;
}
.team-14 .stroke,
.team-14:before {
  stroke: burlywood;
  background:   burlywood;
  stroke-width: 2;
}

</style>

<style scoped lang="scss">
h2 {
  color: var(--darker-blue);
  margin: 1rem 0;
}

.cumulative-returns {
  background-color: white;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
  padding: 1em;
  border-radius: 5px;
}

#trend-chart-options-container {
  margin-bottom: 30px;
  margin-top: 30px;
}

#trend-chart-graph {
  height: 300px !important;
}

#trend-chart-details {
  margin-bottom: 30px;
  margin-top: 30px;
}
</style>
