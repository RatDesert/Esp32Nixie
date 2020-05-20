import EspAPI from "@/services/EspAPI.js";

export const state = () => ({
  clock_date: {
    milliseconds: Number,
    second: Number,
    minute: Number,
    hour: Number,
    weekday: Number,
    day: Number,
    month: Number,
    year: Number,
  },
});

export const getters = {
  getClockDate: (state) => {
    return state.clock_date;
  },
};

export const mutations = {
  SET_CLOCK_DATE: (state, payload) => {
    state.clock_date = payload;
  },
};

export const actions = {
  getClockDate({ commit }) {
    return new Promise((resolve, reject) => {
      EspAPI.getDate()
        .then((response) => {
          commit("SET_CLOCK_DATE", response.data);
          resolve(response);
        })
        .catch((err) => {
          reject(err);
        });
    });
  },
};
