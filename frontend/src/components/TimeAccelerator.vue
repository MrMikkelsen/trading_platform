<template>
  <div id="time-accelerator">
    <form @submit.prevent="submit">
      <input
        v-model="acceleration"
        class="acceleration-input"
        required
        placeholder="Enter amount of acceleration in minutes"
      />
      <input
        type="submit"
        value="Submit"
        :click="submit"
        class="acceleration-submit"
      />
      <span class="result-text"
        >Current time speed is {{ timeSpeed }} minute(s) per second.</span
      >
    </form>
    <!--           <span class="explanation-text"
        >1 = (default - 1 minute per second) | 60 = 1 hour </span
      > -->
  </div>
</template>

<script>
import { Vue, Component } from "vue-property-decorator";

@Component()
export default class TimeAccelerator extends Vue {
  acceleration = "";
  timeSpeed = 60;

  submit() {
    if (this.acceleration === "0") {
      alert("Ratio cannot be zero, please use the Pause button.");
      return;
    }

    this.$store.commit("setTimeAcceleration", this.acceleration);
    let fileToSubmit = { ratio: this.acceleration };
    this.accelerateTime(fileToSubmit, this.$store.state.loggedInToken);
  }

  async accelerateTime(ratio) {
    let adminToken = this.$route.params.token;
    await fetch(`time/setTimeAcc`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ratio, api_key: adminToken }),
    });

    this.timeSpeed = this.acceleration;
  }
}
</script>

<style scoped lang="scss">
#time-accelerator {
  display: flexbox;
  padding: 0 1em 0 0;
  margin: 1em 0 0 0;
  border-radius: 5px;
}

.acceleration-input {
  padding: 5px;
  margin: 0 0 0 0;
  width: 35%;
}
.acceleration-submit {
  padding: 5px;
  padding-bottom: 5px;
  margin: 0 0 0 5px;
}
.result-text {
  font-size: 12px;
  font-style: italic;
  margin: 0 0 0 5px;
  color: rgba(45, 45, 87, 0.555);
}

.explanation-text {
  font-size: 11px;
  margin: 0 0 0 5px;
  color: rgba(45, 45, 87, 0.555);
}
</style>
