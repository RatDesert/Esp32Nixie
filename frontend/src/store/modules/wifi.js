import EspAPI from "@/services/EspAPI.js";

export const state = {
  // wifi_list must update only if user not in form
  wifi_list: Array,
  active_wifi: Object,
  is_connecting: false
};

export const actions = {
  connectToWifi({ commit }, credentials) {
    commit("SET_CONN_STATUS", true);
    return new Promise((resolve, reject) => {


      EspAPI.postWifiAuth(credentials)
        .then(response => {
          commit("SET_ACTIVE_WIFI", response.data);

          commit("SET_CONN_STATUS", false);
          resolve(response);
        })
        .catch(err => {
          commit("SET_CONN_STATUS", false);
          reject(err);
        });
    });
  },

  fetchWifiList({ commit }) {
    return new Promise((resolve, reject) => {
      EspAPI.getWifiList()
        .then(response => {
          commit("SET_WIFI_LIST", response.data);
          resolve(response);
        })
        .catch(err => {
          reject(err);
        });
    });
  },


  getActiveWifi({ commit }) {
    return new Promise((resolve, reject) => {
      EspAPI.getActiveWifi()
        .then(response => {
          commit("SET_ACTIVE_WIFI", response.data);
          resolve(response);
        })
        .catch(err => {
          reject(err);
        });
    });
  }
};

export const mutations = {
  SET_WIFI_LIST: (state, wifiList) => {
    state.wifi_list = wifiList.sort((a, b) => (a.essid > b.essid ? 1 : -1));
  },

  SET_ACTIVE_WIFI: (state, activeWifi) => {
    state.active_wifi = activeWifi;
  },

  SET_CONN_STATUS: (state, isConnecting) => {
    state.is_connecting = isConnecting;
  }
};

export const getters = {
  getWifiList: state => {
    return state.wifi_list;
  },
  getActiveWifi: state => {
    return state.active_wifi;
  },
  isConnecting: state => {
    return state.is_connecting;
  }
};
