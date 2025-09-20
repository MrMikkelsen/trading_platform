import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import "./globalStyles.scss";

Vue.config.productionTip = false

store.dispatch("login", sessionStorage.getItem('LINC-hackathon-token'))

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
