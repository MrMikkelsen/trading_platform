<template>
  <div id="app">
    <div v-if="isUserLoggedIn" id="home-screen">
      <MainHeader />
      <router-view id="router-block" />
    </div>

    <div v-else id="login-screen">
      <!--<router-view id="router-block" /> If we have router view element here we can localhost/ping and see the ping message-->
      <Login />
    </div>
  </div>
</template>

<script>
import { Vue, Component } from "vue-property-decorator";
import MainHeader from "./components/MainHeader";
import Login from "./components/Login";

@Component({
  components: {
    MainHeader,
    Login,
  },
})
export default class App extends Vue {
  get isUserLoggedIn() {
    if (this.$store.state.user.role === "group") {
      this.$router.push(`/team/${this.$store.state.user.token}`);
      return true;
    }
    if (this.$store.state.user.role === "admin") {
      this.$router.push(`/admin/${this.$store.state.user.token}`);
      return true;
    }

    if(this.$store.state.user.role === "viewer"){
       this.$router.push(`/viewer`);
      return true;
    }
    return false;
  }

  created() {}
}
</script>

<style lang="scss">
#router-block {
  grid-area: router;
  margin: 2rem;
}

</style>
