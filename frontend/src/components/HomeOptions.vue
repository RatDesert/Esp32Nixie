<template>
  <div>
    <div style="border-top-width: 0px" class="modal-option" @click="showModal('time')">
      <div class="text" v-text="currentTime"></div>
      <ClockOutlineIcon class="icon" />
    </div>

    <div class="modal-option" @click="showModal('wifi')">
      <div class="text">{{ activeWifi }}</div>
      <WifiIcon class="icon" />
    </div>
    <div class="modal-option" @click="showModal('led')">
      <div class="led" :style="ledColor">
        <SquareIcon class="icon" />
      </div>

      <LedOnIcon class="icon" />
    </div>
    <div class="modal-option" @click="turnServerOff">
      <div class="text">Kill server</div>
      <ServerOffIcon class="icon" />
    </div>
    <TimeModal v-if="isModalVisible['time']" @close="closeModal('time')" @show-modal="showModal" />
    <WifiModal v-if="isModalVisible['wifi']" @close="closeModal('wifi')" />
    <LedModal v-if="isModalVisible['led']" @close="closeModal('led')" />
  </div>
</template>

<script>
import WifiModal from "@/components/WifiModal.vue";
import TimeModal from "@/components/TimeModal.vue";
import LedModal from "@/components/LedModal.vue";
import moment from "moment-timezone";
import WifiIcon from "vue-material-design-icons/Wifi.vue";
import ServerOffIcon from "vue-material-design-icons/ServerOff.vue";
import ClockOutlineIcon from "vue-material-design-icons/ClockOutline.vue";
import LedOnIcon from "vue-material-design-icons/LedOn.vue";
import SquareIcon from "vue-material-design-icons/Square.vue";
import EspAPI from "@/services/EspAPI.js";

export default {
  name: "HomeOptions",
  components: {
    WifiModal,
    TimeModal,
    ClockOutlineIcon,
    WifiIcon,
    LedOnIcon,
    SquareIcon,
    LedModal,
    ServerOffIcon
  },
  created() {
    this.currentTime = moment().format("LTS");
    setInterval(() => this.updateCurrentTime(), 1000);
  },
  data() {
    return {
      isModalVisible: {
        wifi: false,
        led: false,
        time: false
      },
      currentTime: null
    };
  },
  watch: {
    isModalVisible: {
      deep: true,
      handler() {
        if (Object.values(this.isModalVisible).includes(true)) {
          document.documentElement.style.overflow = "hidden";
        } else {
          document.documentElement.style.overflow = "auto";
        }
      }
    }
  },
  methods: {
    showModal(modal) {
      this.isModalVisible[modal] = true;
    },
    closeModal(modal) {
      this.isModalVisible[modal] = false;
    },
    updateCurrentTime() {
      this.currentTime = moment().format("LTS");
    },
    turnServerOff() {
      EspAPI.turnServerOff();
      document.location.reload(true);
    }
  },
  computed: {
    activeWifi() {
      let activeWifi = this.$store.getters.getActiveWifi["essid"];
      return activeWifi ? activeWifi : "Not connected";
    },
    ledColor() {
      let color = this.$store.getters.ledColor;
      return { "--led-color": `rgb(${color.r}, ${color.g}, ${color.b})` };
    }
  }
};
</script>

<style scoped>
.modal-option {
  color: #d1d1d1;
  padding-left: 3%;
  padding-right: 3%;
  border-radius: min(1vmin, 5px);

}

.led {
  color: var(--led-color);
}

.icon {
  height: max(26px, min(3.5vmin, 30px));
  width: max(26px, min(3.5vmin, 30px));
}

.material-design-icon > .material-design-icon__svg {
  width: max(26px, min(3.5vmin, 30px));
  height: max(26px, min(3.5vmin, 30px));
}
.modal-option:hover{
  background-color: #d1d1d1;
  color:#0e1114;

}
</style>