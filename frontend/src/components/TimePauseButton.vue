<template>
  <button :class="buttonClass" @click="togglePauseResume">
    {{ buttonLabel }}
  </button>
</template>

<script>
import { Vue, Component } from "vue-property-decorator";

@Component
export default class TimePauseButton extends Vue {
  isPaused = false;
  buttonLabel = "Pause";

  get buttonClass() {
    return this.isPaused ? "resume" : "pause";
  }

  async togglePauseResume() {
    if (this.isPaused) {
      await this.resumeTime();
    } else {
      await this.pauseTime();
    }
    this.isPaused = !this.isPaused;
    this.updateButtonLabel();
  }

  async pauseTime() {
    console.log("pauseTime function called");
    await fetch("time/pauseTime", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ api_key: this.$route.params.token }),
    });
  }

  async resumeTime() {
    console.log("resumeTime function called");
    await fetch("time/resumeTime", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ api_key: this.$route.params.token }),
    });
  }

  updateButtonLabel() {
    this.buttonLabel = this.isPaused ? "Resume" : "Pause";
  }
}
</script>

<style scoped>
.pause {
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
  padding-top: 10px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

.resume {
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  padding-top: 10px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}
</style>
