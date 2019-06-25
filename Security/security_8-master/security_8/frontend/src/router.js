import Vue from "vue";
import Router from "vue-router";
import Login from "./views/Login.vue";
import Chat from "@/views/Chat.vue";
import SignUp from "@/views/SignUp.vue";
import Mainpage from "@/views/Mainpage.vue";
import SignUpResult from "@/views/SignUpResult.vue"

Vue.use(Router);

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/",
      name: "Login",
      component: Login
    },
    {
      path: "/chat",
      name: "Chat",
      component: Chat,
      props: true,
      beforeEnter: (to, from, next) => {
        if (to.params.name) {
          next();
        } else {
          next({ name: "Login" });
        }
      }
    },
    {
      path: "/signup",
      name: "SignUp",
      component: SignUp
    },
    {
      path: "/mainpage",
      name: "Mainpage",
      component: Mainpage
    },
    {
      path: "/signupresult",
      name: "SignUpResult",
      component: SignUpResult
    }

  ]
});
