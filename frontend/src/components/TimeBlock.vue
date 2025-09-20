<template>
  <div id="time-block">
    <p>{{ time }} <span class="gmt">GMT</span></p>
  </div>
</template>

<script>
import { Vue, Component } from "vue-property-decorator";

@Component
export default class TimeBlock extends Vue {
  time = "";
  interval = undefined;

  // get time (){
  //   return this.$store.state.stocksAndTime ? this.$store.state.stocksAndTime.time : "";
  // }

  created() {
    this.timeTimer();
    /*
    this.eventSource = new EventSource(`/feed/time`);
    this.eventSource.addEventListener("message", (e) => {
      this.time = JSON.parse(e.data);
    });
    */
  }

  timeTimer() {
    this.interval = setInterval(async () => {
      await fetch("time/currentTime")
        .then((res) => res.json())
        .then((data) => {
          this.time = data.data;
        })
        .catch();
    }, 1000);
  }

  beforeDestroy() {
    if (this.interval) clearInterval(this.interval);
  }
}
</script>

<style scoped lang="scss">
#time-block {
  padding: 1.5em;
  background-color: white;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
  border-radius: 5px;
}
p {
  text-align: center;
  font-size: 40px;
  color: var(--darker-blue);
}
.gmt {
  color: var(--saldo-color);
}
</style>
