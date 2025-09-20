<template>
  <div class="overlay" @click="close">
    <div id="reset-datastream" @click.stop>
      <h3>Reset data stream</h3>
      <datepicker
        placeholder="Choose date"
        :monday-first="true"
        @selected="selectDate"
      />

      <button class="button--main" @click="reset">Reset</button>
    </div>
  </div>
</template>

<script>
import { Vue, Component } from "vue-property-decorator";
import Datepicker from "vuejs-datepicker";

@Component({
  components: {
    Datepicker,
  },
})
export default class ResetTeamHistoryPopup extends Vue {
  date = null;

  close() {
    this.$emit("close");
  }

  selectDate(date) {
    this.date = new Date(date);
  }

  async reset() {
    let adminToken = this.$store.state.user.token;

    try {
      if (this.date) {
        await fetch(`time/reset`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ date: this.date, api_key: adminToken }),
        });
      } else {
        await fetch(`time/reset`, {
          method: "POST",
        });
      }

      alert("Data stream has been reset.");
    } catch (e) {
      console.log(e);
      alert("Something went wrong, could'nt reset data stream.");
    }
  }
}
</script>

<style scoped land="scss">
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.1);
  z-index: 100;
}

#reset-datastream {
  position: absolute;
  top: 25%;
  left: 50%;
  transform: translateX(-50%);
  background-color: white;
  padding: 1rem;
  color: var(--darker-blue);
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
  border-radius: 5px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

#reset-datastream > *:not(:last-child) {
  margin-bottom: 1.6rem;
}
</style>
