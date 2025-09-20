<template>
  <div class="overlay" @click="close">
    <div id="reset-team-history" @click.stop>
      <h3>Reset team's history</h3>
      <select class="select-teams" @change="this.changeTeam">
        <option value="">Choose team</option>
        <option v-for="team in allGroups" :key="team.name" :value="team.token">
          {{ team.name }}
        </option>
      </select>
      <button class="button--main" @click="reset">Reset</button>
    </div>
  </div>
</template>

<script>
import { Vue, Component, Prop } from "vue-property-decorator";

@Component({
  components: {},
})
export default class ResetTeamHistoryPopup extends Vue {
  @Prop() allGroups;
  team = null;

  changeTeam(event) {
    if (event.target.value) {
      this.team = event.target.value;
    }
  }

  close() {
    this.$emit("close");
  }

  async reset() {
    if (this.team) {
      try {
        let adminToken = this.$store.state.user.token;
        await fetch(`api/private/admin/${adminToken}/resetHistory`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ token: this.team }),
        });
        alert("Team's data has been reset.");
      } catch (e) {
        console.log(e);
          alert("Something went wrong, could'nt reset team's data")
      }
    } else {
      alert("Choose a team");
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
}
#reset-team-history {
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
  z-index: 100;
}

#reset-team-history > *:not(:last-child) {
  margin-bottom: 1.6rem;
}
</style>
