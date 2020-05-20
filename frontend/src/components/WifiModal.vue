<template>
  <div class="modal-backdrop" @click.self="close">
    <div class="loading" v-if="isWifiListEmpty"></div>
    <div v-else class="modal" >
      
      <div v-for="(wifi, index) in wifiList" :key="index">
        <WifiModalItem
          :wifi="wifi"
          :index="index"
          :isFormOpen="openFormMap[index]"
          :active="isWifiActive(wifi)"
          @show-form="showWifiForm"
          @close="close"
          @update-active="getActiveWifi"
        />
        
      </div>
      
    </div>
    
  </div>
</template>

<script>
import WifiModalItem from "@/components/WifiModalItem.vue";
export default {
  name: "WifiModal",
  components: { WifiModalItem },
  data() {
    return {
      openFormMap: [],
      polling: null,
      wifiList: []
    };
  },
  created() {
    this.fetchWifiList();
    this.polling = setInterval(() => {
      if (!this.openFormMap.find(element => element === true)) {
        this.fetchWifiList();
      }
    }, 5000);
  },

  methods: {
    close() {
      this.openFormMap = new Array(this.wifiList.length).fill(false);
      this.$emit("close");
    },

    showWifiForm(index, isFormOpen) {
      this.openFormMap.fill(false);
      this.openFormMap[index] = isFormOpen;
      this.$forceUpdate();
    },
    fetchWifiList() {
      this.$store
        .dispatch("fetchWifiList")
        .then(() => {
          this.updateWifiList();
        })
        .catch(err => console.log(err));
    },
    getActiveWifi() {
      this.$store.dispatch("getActiveWifi").catch(err => console.log(err));
    },
    isWifiActive(wifi) {
      return wifi["essid"] === this.$store.getters.getActiveWifi["essid"];
    },
    updateWifiList() {
      if (
        !this.openFormMap.find(element => element === true) &&
        !this.$store.getters.isConnecting
      ) {
        this.wifiList = this.$store.getters.getWifiList;
      }
    }
  },
  computed: {
    isWifiListEmpty(){
      return this.wifiList.length === 0 ? true : false
    }
  },
  beforeDestroy() {
    clearInterval(this.polling);
  }
};
</script>
<style scoped>
.loading  {
  justify-self: center;
  align-self: center;
  box-sizing: border-box;
  display: block;
  height: max(64px, min(2.5vmin, 128px));
  width: max(64px, min(2.5vmin, 128px));

  border:  max(3px, min(2.5vmin, 6px)) solid #fff;
  border-radius: 50%;
  animation: lds-ring 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
  border-color: #b0b3c0 transparent transparent transparent;
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
}</style>