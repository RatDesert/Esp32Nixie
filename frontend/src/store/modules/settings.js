import EspAPI from "@/services/EspAPI.js";

export const state = () => ({
  first_setup: Boolean,
  auto_time: Boolean,
});

export const getters = {
  getAutoTimeState: (state) => {
    return state.auto_time;
  },
  getFirstSetupState: (state) => {
    return state.first_setup;
  },
};

export const mutations = {
  SET_AUTOTIME_STATE: (state, payload) => {
    state.auto_time = payload['auto_time'];
  },
  SET_FIRSTSETUP_STATE: (state, payload) => {
    state.first_setup = payload['first_setup'];
  },
};

export const actions = {
  getAutoTimeState({ commit }) {
    return new Promise((resolve, reject) => {
      EspAPI.getAutoTimeState()
        .then((response) => {
          commit("SET_AUTOTIME_STATE", response.data);
          resolve(response);
        })
        .catch((err) => {
          reject(err);
        });
    });
  },

  postAutoTimeState({ commit }, autoTime) {
    return new Promise((resolve, reject) => {
      EspAPI.postAutoTimeState(autoTime)
        .then((response) => {
          commit("SET_AUTOTIME_STATE", response.data);
          resolve(response);
        })
        .catch((err) => {
          reject(err);
        });
    });
  },

  getFirstSetupState({ commit }) {
    return new Promise((resolve, reject) => {
      EspAPI.getFirstSetupState()
        .then((response) => {
          commit("SET_FIRSTSETUP_STATE", response.data);
          resolve(response);
        })
        .catch((err) => {
          reject(err);
        });
    });
  },
  postFirstSetupState({ commit }, firstSetup) {
    return new Promise((resolve, reject) => {
      EspAPI.postFirstSetupState(firstSetup)
        .then((response) => {
          commit("SET_FIRSTSETUP_STATE", response.data);
          resolve(response);
        })
        .catch((err) => {
          reject(err);
        });
    });
  },
};
