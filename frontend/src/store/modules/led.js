import EspAPI from "@/services/EspAPI.js";

export const state = {
  color: Object,
};

export const actions = {
  changeLedColor({ commit }, data) {
    return new Promise((resolve, reject) => {
      EspAPI.postLedColor(data)
        .then((response) => {
          let color = response.data;
          commit("change_led_color", color);
          resolve(response);
        })
        .catch((err) => {
          reject(err);
        });
    });
  },
  getLedColor({ commit }) {
    return new Promise((resolve, reject) => {
      EspAPI.getLedColor()
        .then((response) => {
          let color = response.data;
          commit("change_led_color", color);
          resolve(response);
        })
        .catch((err) => {
          reject(err);
        });
    });
  },
};

export const mutations = {
  change_led_color(state, color) {
    state.color = color;
  },
};

export const getters = {
  ledColor: (state) => {
    return state.color;
  },
};
