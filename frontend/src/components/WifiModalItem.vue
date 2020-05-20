<template>
  <div
    class="item-container"
    v-on="
      !isConnecting && !active
        ? wifi.security === 1
          ? {
              click: () => {
                closeForm();
                connectToWifi();
              }
            }
          : { click: () => showForm() }
        : null
    "
    :class="{ 'info-container-active': active }"
  >
    <div class="info-container" v-if="!isFormOpen && !showConnecting">
      <div class="info-text">
        <div class="text">{{ wifi.essid }}</div>
      </div>
      <div class="info-icon">
        <CheckBoldIcon class="icon" v-if="active"></CheckBoldIcon>
      </div>
      <div class="info-icon">
        <LockIcon class="icon" v-if="wifi.security > 1" />
      </div>
      <div class="info-icon">
        <WifiStrength4Icon class="icon" v-if="wifi.rssi > -50" />
        <WifiStrength3Icon
          class="icon"
          v-if="wifi.rssi <= -50 && wifi.rssi > -60"
        />
        <WifiStrength2Icon
          class="icon"
          v-if="wifi.rssi <= -60 && wifi.rssi > -70"
        />
        <WifiStrength1Icon class="icon" v-if="wifi.rssi <= -70" />
      </div>
    </div>

    <div class="form-container" v-if="isFormOpen && !showConnecting">
      <form class="form" @submit.prevent="connectToWifi">
        <input
          class="input"
          required
          v-model="password"
          type="password"
          placeholder="Password"
        />
        <button class="button" type="submit">Join</button>
      </form>
    </div>

    <div v-if="showConnecting" class="loading-container">
      <div class="text">{{ wifi.essid }}</div>
      <div class="loading" :style="connectingStyle"></div>
    </div>
  </div>
</template>

<script>
import CheckBoldIcon from "vue-material-design-icons/CheckBold.vue";
import LockIcon from "vue-material-design-icons/Lock.vue";
import WifiStrength4Icon from "vue-material-design-icons/WifiStrength4.vue";
import WifiStrength3Icon from "vue-material-design-icons/WifiStrength3.vue";
import WifiStrength2Icon from "vue-material-design-icons/WifiStrength2.vue";
import WifiStrength1Icon from "vue-material-design-icons/WifiStrength1.vue";

export default {
  name: "WifiModalItem",
  props: ["wifi", "index", "isFormOpen", "active"],
  components: {
    LockIcon,
    WifiStrength4Icon,
    WifiStrength3Icon,
    WifiStrength2Icon,
    WifiStrength1Icon,
    CheckBoldIcon
  },

  data() {
    return {
      password: "",
      showConnecting: false,
      showConnectingErr: false,
      showConnectingSuccess: false
    };
  },

  methods: {
    connectToWifi() {
      const credentials = {
        essid: this.wifi.essid,
        password: this.password
      };
      this.showConnecting = true;
      this.$store
        .dispatch("connectToWifi", credentials)
        .then(() => {
          this.closeForm();
          this.showConnectingSuccess = true;

          setTimeout(() => {
            this.showConnecting = false;
            this.showConnectingSuccess = false;
          }, 500);
        })
        .catch(err => {
          this.showConnectingErr = true;

          setTimeout(() => {
            this.showConnecting = false;
            this.showConnectingErr = false;
          }, 1500);

          console.log(err);
        });
      this.password = "";
    },
    showForm() {
      this.$emit("show-form", this.index, true);
    },

    closeForm() {
      this.$emit("show-form", this.index, false);
    }
  },

  computed: {
    isConnecting() {
      return this.$store.getters.isConnecting;
    },
    connectingStyle() {
      if (this.showConnectingSuccess) {
        return {
          "--border-color": "#00bb70 transparent transparent transparent"
        };
      } else {
        if (this.showConnectingErr) {
          return {
            "--border-color": "#D8000C transparent transparent transparent"
          };
        } else {
          return {
            "--border-color": "#b0b3c0 transparent transparent transparent"
          };
        }
      }
    }
  }
};
</script>

<style scoped>
.item-container {
  letter-spacing: 1px;
  border-top-color: #181818;
  border-top-style: solid;
  border-top-width: 1px;
  padding-right: 6%;
  padding-left: 6%;
}

.info-container {
  height: max(60px, min(10vh, 75px));
  width: 100%;
  display: flex;
  align-items: center;
}
.info-container-active {
  color: #0e1638;
  background-color: #00bb70;
  animation: colorchange .3s;
  -webkit-animation: colorchange .3s;
}

@keyframes colorchange {
  0% {
    background: #0e1114;
    color:#b0b3c0
  }

  100% {
    background: #00bb70;
    color:#0e1638;
  }
}

@-webkit-keyframes colorchange {
  0% {
    background: #0e1114;
    color:#b0b3c0
  }

  100% {
    background: #00bb70;
    color:#0e1638;
  }
}

.info-text,
.info-icon {
  display: flex;
  align-items: center;
  height: 75%;
}

.info-text {
  width: 80%;
}
.info-icon {
  justify-content: flex-end;
  width: 15%;
}

.icon {
  height: max(22px, min(3.5vmin, 26px));
  width: max(22px, min(3.5vmin, 26px));
}

.material-design-icon > .material-design-icon__svg {
  height: max(22px, min(3.5vmin, 26px));
  width: max(22px, min(3.5vmin, 26px));
}

.form-container {
  display: flex;
  align-items: center;
  height: max(60px, min(10vh, 75px));
  width: 100%;
  animation: resize 100ms ease forwards;
}

.form {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 57%;
  width: 100%;
}

.button,
.input {
  height: 100%;
  box-sizing: border-box;
  -moz-box-sizing: border-box;
  border-radius: 4px;
  cursor: pointer;
  border: none;
}

.input {
  width: 71%;
  background-color: rgb(209, 216, 218);
}

.button {
  font-family: "Roboto", sans-serif;
  width: 23%;
  justify-content: flex-end;
  color: rgb(255, 255, 255);
  background-color: rgb(255, 255, 255);
  box-shadow: 0px 1px 2px rgba(0, 0, 0, 0.1);
  background-color: #00bb70;
}

.loading-container {
  display: flex;

  align-items: center;
  justify-content: space-between;
  height: max(60px, min(10vh, 75px));
  width: 100%;

}

@keyframes resize {
  0% {
    padding: 0px;
  }

  100% {
    padding: max(15px, min(1vh, 30px)) 0px max(15px, min(1vh, 30px)) 0px;
  }
} 

.loading  {
  box-sizing: border-box;
  display: block;
  height: max(32px, min(2.5vmin, 64px));
  width: max(32px, min(2.5vmin, 64px));

  border:  max(3px, min(2.5vmin, 6px)) solid #fff;
  border-radius: 50%;
  animation: lds-ring 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
  border-color: var(--border-color);
}
.loading:nth-child(1) {
  animation-delay: -0.45s;
}
.loading:nth-child(2) {
  animation-delay: -0.3s;
}
.loading:nth-child(3) {
  animation-delay: -0.15s;
}
@keyframes lds-ring {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.button:hover {
  background-color: #00f090;
  color: blanchedalmond;
}
::placeholder {
  font-family: "Roboto", sans-serif;
  color: rgba(0, 0, 0, 0.226);
}
</style>
