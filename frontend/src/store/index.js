import Vue from "vue";
import Vuex from "vuex";
// import io from "socket.io-client";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    // socket: io.connect("http://localhost:3000"),
    allSymbols: [
      "STOCK1",
      "STOCK2",
      "STOCK3",
      "STOCK4",
      "STOCK5",
      "STOCK6",
      "STOCK7",
      "STOCK8",
      "STOCK9",
      "STOCK10",
    ],
    stockData: null,
    groupData: {
      data: {
        balance: 0,
        profit: 0,
      },
      stocks: [],
    },
    user: {
      token: null,
      role: null,
    },
    timeAcceleration: 1,
    borderColorsPieChart: [
      "rgba(255, 0, 0, 1)",
      "rgba(255, 0, 128, 1)",
      "rgba(255, 0, 255, 1)",
      "rgba(0, 0, 255 , 1)",
      "rgba(0, 255, 128, 1)",
      "rgba(0, 255, 0, 1)",
      "rgba(128, 255, 0, 1)",
      "rgba(255, 255, 0, 1)",
      "rgba(255, 128, 0, 1)",
    ],
    backgroundColorsPieChart: [
      "rgba(255, 0, 0, 1)",
      "rgba(255, 0, 128, 1)",
      "rgba(255, 0, 255, 1)",
      "rgba(0, 0, 255 , 1)",
      "rgba(0, 255, 128, 1)",
      "rgba(0, 255, 0, 1)",
      "rgba(128, 255, 0, 1)",
      "rgba(255, 255, 0, 1)",
      "rgba(255, 128, 0, 1)",
      "rgba(255, 255, 128, 1)",
    ],
    startingAmount: 5000,
  },
  mutations: {
    setUser(state, value) {
      state.user.token = value.token;
      state.user.role = value.role;
    },
    setStockData(state, value) {
      state.stockData = value;
    },
    setTimeAcceleration(state, value) {
      state.timeAcceleration = value;
    },
    setGroupData(state, value) {
      state.groupData = value;
    },
  },
  actions: {
    async login({ commit }, token) {
      if (token === "viewer") {
        sessionStorage.setItem("LINC-hackathon-token", "viewer");
        commit("setUser", { token: "viewer", role: "viewer" });
      } else {
        let res = await fetch(`/api/auth/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ api_key: token }),
        });

        res = await res.json();
        sessionStorage.setItem("LINC-hackathon-token", res.token);
        commit("setUser", res);
      }
    },
    async continueAsViewer({ commit }) {
      sessionStorage.setItem("LINC-hackathon-token", "viewer");
      commit("setUser", { token: "viewer", role: "viewer" });
    },
    async updateGroupData({ commit }, payload) {
      commit("setGroupData", { ...payload, history: payload.pastSales });
    },
    async logout({ commit }) {
      sessionStorage.setItem("LINC-hackathon-token", null);
      sessionStorage.setItem("LINC-hackathon-token", null);
      commit("setUser", { token: null, role: null });
    },
  },
  modules: {},
});
