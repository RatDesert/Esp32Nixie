<template>
  <div class="background">
    <div id="app">
      <h1 class="logo">NITON</h1>
      <HomeOptions class="home-options" />
    </div>
  </div>
</template>

<script>
import HomeOptions from "@/components/HomeOptions.vue";
import moment from "moment-timezone";
import EspAPI from "@/services/EspAPI.js";

export default {
  name: "App",
  components: {
    HomeOptions
  },

  created() {
    this.getActiveWifi();
    this.getLedColor();
    this.getClockState();
    setInterval(() => {
      this.getActiveWifi();
    }, 5000);
  },

  methods: {
    getActiveWifi() {
      this.$store.dispatch("getActiveWifi").catch(err => console.log(err));
    },
    getLedColor() {
      this.$store.dispatch("getLedColor").catch(err => console.log(err));
    },

    getClockState() {
      this.$store.dispatch("getAutoTimeState").catch(err => console.log(err));
      this.$store
        .dispatch("getFirstSetupState")
        .then(() => {
          if (this.$store.getters.getFirstSetupState) {
            this.firstSetup();
          }
        })
        .catch(err => console.log(err));
    },
    firstSetup() {
      this.setDeviceDate();
      this.$store
        .dispatch("postFirstSetupState", { first_setup: false })
        .catch(err => console.log(err));
    },

    setDeviceDate() {
      const m = moment();
      const date = {
        milliseconds: m.millisecond(),
        second: m.second(),
        minute: m.minute(),
        hour: m.hour(),
        weekday: m.day(),
        day: m.date(),
        month: m.month(),
        year: m.year()
      };
      EspAPI.postDate(date).catch(err => console.log(err));
    }
  }
};
</script>
<style>
@import "./assets/styles/global.css";
</style>
