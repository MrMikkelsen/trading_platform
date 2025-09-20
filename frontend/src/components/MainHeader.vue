<template>
  <div id="main-header">
    <div class="logo"><img src="../assets/linc-logo.png" alt="" /></div>
    <p v-if="this.$route.path === '/viewer'">VIEWER PAGE</p>
    <p v-else-if="this.$route.path.includes('admin')">ADMIN PAGE</p>
    <p v-else>TEAM PAGE</p>
    <button v-if="isAdmin === 'admin'" id="home" @click="goToHome()">Home</button>
    <button id="logout" @click="logout">Logout</button>
  </div>
</template>

<script>
import { Vue, Component } from "vue-property-decorator";

@Component
export default class MainHeader extends Vue {
  isAdmin = this.$store.state.user.role;

  goToAllStocks() {
    if (this.$route.path !== "/") {
      this.$router.push("/");
    }
  }
  goToHistory() {
    if (this.$route.path !== "/history") {
      this.$router.push("/history");
    }
  }

  goToHome() {
        if (this.$route.path !== `/admin/${this.$store.state.user.token}`) {
      this.$router.push(`/admin/${this.$store.state.user.token}`);
    }
  }

  logout() {
    this.$store.dispatch('logout');
    this.$router.push('/');
  }

  get username() {
    if (this.$store.state.loggedInToken !== undefined) {
      //return this.$store.state.loggedInToken.email.slice(0,5).toUpperCase();
      return this.$store.state.loggedInToken.email;
    } else {
      return "";
    }
  }
}
</script>

<style scoped>
#main-header {
  display: grid;
  padding: 1rem 2rem;
  grid-template-columns: 10% 1fr 8% 8%;
  align-items: center;
  text-align: center;
  background-color: var(--darker-blue);
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1), 0 3px 10px 0 rgba(0, 0, 0, 0.1);
}
#main-header-items > * {
  display: inline-block;
}
.logo {
  align-items: left;
}
p {
  color: white;
  font-size: 30px;
  font-weight: 0;
}

h3 {
  color: white;
  text-align: right;
  font-weight: 100;
}
#all-stocks {
  padding-right: 10px;
  font-weight: 500;
  cursor: pointer;
}
#history {
  padding-left: 10px;
  cursor: pointer;
}
#userName {
  padding-left: 20px;
  cursor: pointer;
}
#home, #logout {
  padding: 0.2rem 0.5rem;
  cursor: pointer;
  margin-left: 5px;
}
</style>
