<template>
  <div>
    <div class="digit">
      <input
        :class="{ 'input-success' : showSuccess}"
        class="input-left"
        type="text"
        maxlength="1"
        v-model="inputValue.H"
        :placeholder="[[ inputPlaceholder.H ]]"
        ref="input_0"
        @keyup="changeInputFocus($event, 0)"
      />
      <input
        :class="{ 'input-success' : showSuccess}"
        class="input-right"
        type="text"
        maxlength="1"
        v-model="inputValue.h"
        :placeholder="[[ inputPlaceholder.h ]]"
        ref="input_1"
        @keyup="changeInputFocus($event, 1)"
      />
    </div>
    <div class="digit">
      <input
        :class="{ 'input-success' : showSuccess}"
        class="input-left"
        type="text"
        maxlength="1"
        v-model="inputValue.M"
        :placeholder="[[ inputPlaceholder.M ]]"
        ref="input_2"
        @keyup="changeInputFocus($event, 2)"
      />
      <input
        :class="{ 'input-success' : showSuccess}"
        class="input-right"
        type="text"
        maxlength="1"
        v-model="inputValue.m"
        :placeholder="[[ inputPlaceholder.m ]]"
        ref="input_3"
        @keyup="changeInputFocus($event, 3)"
      />
    </div>
    <div class="digit">
      <input
        :class="{ 'input-success' : showSuccess}"
        class="input-left"
        type="text"
        maxlength="1"
        v-model="inputValue.S"
        :placeholder="[[ inputPlaceholder.S ]]"
        ref="input_4"
        @keyup="changeInputFocus($event, 4)"
      />
      <input
        :class="{ 'input-success' : showSuccess}"
        class="input-right"
        type="text"
        maxlength="1"
        ref="input_5"
        v-model="inputValue.s"
        :placeholder="[[ inputPlaceholder.s ]]"
      />
    </div>
  </div>
</template>

<script>
import EspAPI from "@/services/EspAPI.js";

export default {
  data() {
    return {
      inputPlaceholder: {
        H: "",
        h: "",
        M: "",
        m: "",
        S: "",
        s: ""
      },
      inputValue: {
        H: "",
        h: "",
        M: "",
        m: "",
        S: "",
        s: ""
      },

      showSuccess: false,
      showSuccessTimeout: null
    };
  },

  created() {
    this.setInputPlaceholder();

  },
  watch: {
    "inputValue.H": function(val) {
      this.inputValue.H = val.replace(/[^0-2]/g, "");
      // should force false to showing success in case of "quick hands"
      if (this.inputValue.H) {
        this.showSuccess = false;
        this.showSuccessTimeout = null;
      }
    },
    "inputValue.h": function(val) {
      let reg = /[^0-9]/g;

      if (this.inputValue.H == 2) {
        reg = /[^0-3]/g;
      }
      this.inputValue.h = val.replace(reg, "");
    },
    "inputValue.M": function(val) {
      this.inputValue.M = val.replace(/[^0-5]/g, "");
    },
    "inputValue.m": function(val) {
      this.inputValue.m = val.replace(/[^0-9]/g, "");
    },
    "inputValue.S": function(val) {
      this.inputValue.S = val.replace(/[^0-5]/g, "");
    },
    "inputValue.s": function(val) {
      this.inputValue.s = val.replace(/[^0-9]/g, "");
      if (this.inputValue.s) {
        this.postTime();
        Object.keys(this.inputValue).forEach(v => (this.inputValue[v] = ""));
        this.showSuccess = true;

        this.showSuccessTimeout = setTimeout(function() {
          this.showSuccess = false;
        }, 1000);

        this.setInputPlaceholder();
        this.$refs["input_5"].blur();
      }
    }
  },
  methods: {
    setInputPlaceholder() {
      this.$store
        .dispatch("getClockDate")
        .then(() => {
          const clockDate = this.$store.getters.getClockDate;

          const hour = clockDate.hour;
          const minute = clockDate.minute;
          const second = clockDate.second;

          this.inputPlaceholder = {
            H: Math.floor(hour / 10),
            h: hour % 10,
            M: Math.floor(minute / 10),
            m: minute % 10,
            S: Math.floor(second / 10),
            s: second % 10
          };
        })
        .catch(err => console.log(err));
    },
    changeInputFocus(event, index) {
      if (event.target.value) {
        this.$refs["input_" + (index + 1)].focus();
      }
    },
    postTime() {
      const time = {
        hour: this.inputValue.H + this.inputValue.h,
        minute: this.inputValue.M + this.inputValue.m,
        second: this.inputValue.S + this.inputValue.s
      };
      EspAPI.postTime(time).catch(err => console.log(err));
    }
  }
};
</script>

<style scoped>
.digit {
  display: flex;

  height: 57%;
  width: 30%;
}
input {
  height: 100%;
  width: 100%;
  box-sizing: border-box;
  -moz-box-sizing: border-box;
  cursor: pointer;
  border: none;
  -webkit-appearance: none;
  border-radius: 0;
  -webkit-border-radius: 0;
}

.input-success {
  background-color: #ffffff;
  animation: colorchange 1s;
  -webkit-animation: colorchange 1s;
}

@keyframes colorchange {
  0% {
    background: #ffffff;
  }

  50% {
    background: #00bb70;
  }
  100% {
    background: #ffffff;
  }
}

.input-left {
  border-right-width: 1px;
  border-right-color: #1b1b1b2c;
  border-right-style: solid;

  border-bottom-left-radius: 4px;
  border-top-left-radius: 4px;
}
.input-right {
  border-bottom-right-radius: 4px;
  border-top-right-radius: 4px;
}
</style>