import Vue from "vue";
import VueRouter from "vue-router";
import StockDetails from "@/components/StockDetails";
import StockOverview from "@/components/StockOverview";
import AdminPage from "@/components/AdminPage";
import GroupPage from "@/components/GroupPage";
import Ping from "@/components/Ping";
Vue.use(VueRouter);

const routes = [
  {
    path: "/team/:group",
    name: "StockOverview",
    component: GroupPage,
    children: [
      {
        path: "",
        name: "Stockoverview",
        component: StockOverview,
      },
      {
        path: ":symbol",
        name: "Stockdetails",
        component: StockDetails,
      },
    ],
  },
  {
    path: "/admin/:token",
    name: "AdminPage",
    component: AdminPage,
    children: [
      {
        path: "",
        name: "Stockoverview",
        component: StockOverview,
      },
      {
        path: ":symbol",
        name: "Stockdetails",
        component: StockDetails,
      },
    ],
  },
  {
    path: "/viewer",
    name: "ViewerPage",
    component: AdminPage,
    children: [
      {
        path: "",
        name: "Stockoverview",
        component: StockOverview,
      },
      {
        path: ":symbol",
        name: "Stockdetails",
        component: StockDetails,
      },
    ],
  },
  {
    path: "/ping",
    name: "Ping",
    component: Ping,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
