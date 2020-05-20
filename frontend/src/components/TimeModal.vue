<template>
  <div class="modal-backdrop" @click.self="close">
    <div class="modal">
      <div class="modal-option" @click="toggleAutoTime">
        <div class="text" >Auto</div>
        <toggle-button
          class="toggle"
          :value="enableAutoTime"
          :disabled="!isConnected"
          :sync='true'
        />
      </div>

      <TimeModalManualSet class="modal-option" v-if="!enableAutoTime" />
    </div>
  </div>
</template>

<script>
import { ToggleButton } from "vue-js-toggle-button";
import TimeModalManualSet from "@/components/TimeModalManualSet.vue";
export default {
  components: {
    ToggleButton,
    TimeModalManualSet
  },

  methods: {
    close() {
      this.$emit("close");
    },

    toggleAutoTime() {

      if (this.isConnected) {
        this.$store
          .dispatch("postAutoTimeState", { auto_time: !this.enableAutoTime })
          .then(()=> {
            console.log(this.enableAutoTime);
          })
          .catch(err => console.log(err));
        
      } 
      else {
         this.$emit("show-modal", 'wifi');

         
      }
    },


  },
  computed: {
    enableAutoTime() {
      return this.$store.getters.getAutoTimeState;
    },
    isConnected() {
      return this.$store.getters.getActiveWifi["essid"];
    }
  }
};
</script>

<style scoped>

.time {
  height: max(36px, min(3.5vmin, 44px));
  font-size: max(36px, min(3.5vmin, 44px));
}
.toggle {
  -webkit-tap-highlight-color: transparent;
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}
</style>
