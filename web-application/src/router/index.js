import { route } from "quasar/wrappers";
import {
  createRouter,
  createMemoryHistory,
  createWebHistory,
  createWebHashHistory,
} from "vue-router";
import routes from "./routes";

// - AMPLIFY -
import { Amplify } from "aws-amplify";
import { fetchUserAttributes, fetchAuthSession } from "aws-amplify/auth";
import { AmplifyConfig } from "../config/amplify-config"; // NO TOUCHY
Amplify.configure(AmplifyConfig);

console.log(Amplify.getConfig());

// fetchUserAttributes().then((res) =>
//   console.log("fetch User Attributes: ", res)
// );
// fetchAuthSession().then((res) => console.log("fetch auth session: ", res));

export default route(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : process.env.VUE_ROUTER_MODE === "history"
    ? createWebHistory
    : createWebHashHistory;

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,
    history: createHistory(process.env.VUE_ROUTER_BASE),
  });

  return Router;
});
