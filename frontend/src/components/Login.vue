<template>
  <div id="login">
    <div class="logo">
      <img src="../assets/linc-logo-hq.png" alt="" width="500" />
    </div>
    <p class="welcome-text">Welcome to LINC Hackathon!</p>
    <form class="login-block" @submit.prevent="login">
      <input
        type="text"
        id="token"
        name="token"
        class="input-box"
        placeholder="Enter token"
        v-model="token"
      />

      <button class="input-box" id="submit">Login</button>
      
      <!--
      <button class="input-box btn-viewer" @click="this.continueAsViewer">
        Continue as viewer
      </button>
      -->
    </form>
  </div>
</template>

<script>
import { Vue, Component } from "vue-property-decorator";

@Component
export default class Login extends Vue {
  token = "";

  async login() {
    if (this.token !== "") {
      this.$store.dispatch("login", this.token).then(this.redirect());
    }
  }
  async continueAsViewer() {
    this.$store.dispatch("continueAsViewer").then(this.redirect());
  }
  redirect() {
    let token = this.$store.state.user.token;
    if (this.$store.state.user.role === "admin") {
      this.$router.push(`/admin/${token}`);
    } else if (this.$store.state.user.role === "viewer") {
      this.$router.push("/viewer");
    } else {
      this.$router.push(`/group/${token}`);
    }
  }
}
</script>

<style scoped lang="scss">
.btn-viewer {
  background-color: #e2e6ed;
  border-radius: 5px;
  border: none;
   padding: 6px;
  box-shadow: 1px 1px 1px #00000028;
  color: #15416b;
  margin-top: 0.5rem !important;
  font-size: 1.5rem;
  cursor: pointer;
  
}

#login {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #15416b;
}
.logo {
  transform: scale(1.5);
  margin-bottom: 2rem;
}
.welcome-text {
  margin: 0 0 2rem;
  text-align: center;
  color: white;
  font-size: 1.5rem;
}
input {
  border: none;
  display: flex;
  padding: 1rem;
}
textarea:focus,
input:focus {
  padding-left: 1rem;
  border: none !important;
  outline: none !important;
}
input::placeholder {
  font-style: italic;
  color: #15416b54;
}
.login-block {
  width: 40vw;
  height: auto;
  border-radius: 5px;
  background-color: #e2e6ed;
  box-shadow: 5px 5px 5px #00000028;
  padding: 3rem 0;
  text-align: center;
}
.input-box {
  width: 35vw;
  height: 50px;
  margin: 0 auto;

  background-color: white;
  border-radius: 5px;
}
#username {
  margin: 0 auto 1rem;
}

#submit {
  margin: 2rem auto 0;
  padding: 6px;
  height: 3rem;
  background-color: #15416b;
  text-align: center;
  color: white;
  align-items: center;
  font-size: 1.5rem;
  cursor: pointer;
}
</style>
