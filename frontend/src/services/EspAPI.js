import axios from "axios";

const EspApi = axios.create({
  baseURL: "http://192.168.4.1:80",
  // baseURL: "http://192.168.1.104:8000",
  headers: {
    "Content-Type": "application/json",
  },
});
export default {
  postLedColor(color) {
    let url = "/led/";
    return EspApi.post(url, color);
  },

  getLedColor() {
    let url = "/led/";
    return EspApi.get(url);
  },

  postWifiAuth(credentials) {
    let url = "/wifi/";
    return EspApi.post(url, credentials);
  },

  getWifiList() {
    let url = "/wifi/";
    return EspApi.get(url);
  },

  getActiveWifi() {
    let url = "/wifi/active/";
    return EspApi.get(url);
  },

  getAutoTimeState() {
    let url = "/settings/autotime/";
    return EspApi.get(url);
  },

  postAutoTimeState(state) {
    let url = "/settings/autotime/";
    return EspApi.post(url, state);
  },
  getFirstSetupState(){
    let url = "/settings/firstsetup/";
    return EspApi.get(url);
  },
  
  postFirstSetupState(state){
    let url = "/settings/firstsetup/";
    return EspApi.post(url, state);
  },

  postDate(date) {
    let url = "/date/";
    return new Promise((resolve, reject) => {
      EspApi.post(url, date)
        .then((response) => {
          resolve(response);
        })
        .catch((err) => {
          reject(err);
        });
    });
  },

  getDate() {
    let url = "/date/";
    return EspApi.get(url)
  },
  postTime(time){
    let url = "/date/time/";
    return new Promise((resolve, reject) => {
      EspApi.post(url, time)
        .then((response) => {
          resolve(response);
        })
        .catch((err) => {
          reject(err);
        });
    });
  },
  turnServerOff(){
    let url = "/server/off/";
    return new Promise((resolve, reject) => {
      EspApi.get(url)
        .then((response) => {
          resolve(response);
        })
        .catch((err) => {
          reject(err);
        });
    });
  }
};
