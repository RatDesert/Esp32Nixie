import Vue from "vue";
import Vuex from "vuex";

import * as led from "@/store/modules/led.js";
import * as wifi from "@/store/modules/wifi.js"
import * as time from "@/store/modules/time.js"
import * as settings from "@/store/modules/settings.js"
Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    led,
    wifi,
    time,
    settings

  }
});
