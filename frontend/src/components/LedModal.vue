<template>
  <div class="modal-backdrop" @click.self="close">
    <ColorPicker
      class="color-wheel"
      :key="pickerKey"
      :width="pickerSize"
      :height="pickerSize"
      :disabled="false"
      :startColor="defaultLedColor"
      @color-change="onColorChange"
    ></ColorPicker>
  </div>
</template>

<script>
import ColorPicker from "vue-color-picker-wheel";

export default {
  name: "LedModal",
  components: {
    ColorPicker,
  },
  data() {
    return {
      color: {
        r: 0,
        g: 0,
        b: 0,
      },
      polling: null,
      userSetColor: false,
      pickerSize: (this.$parent.$el.offsetWidth * 3) / 4,
      pickerKey: 0,
      startColor: "#ff0000",
    };
  },
  created() {
    this.changeLedColor();
    window.addEventListener("resize", this.changePickerSize);
  },

  beforeDestroy() {
    clearInterval(this.polling);
  },

  methods: {
    onColorChange(color) {
      color = color.substr(1);
      var values = color.split("");
      this.color.r = parseInt(values[0].toString() + values[1].toString(), 16);
      this.color.g = parseInt(values[2].toString() + values[3].toString(), 16);
      this.color.b = parseInt(values[4].toString() + values[5].toString(), 16);
      this.userSetColor = true;
    },
    changeLedColor() {
      this.polling = setInterval(() => {
        if (this.userSetColor == true) {
          let color = this.color;
          this.userSetColor = false;
          this.$store
            .dispatch("changeLedColor", color)
            .catch((err) => console.log(err));
        }
      }, 300);
    },
    changePickerSize() {
      this.pickerSize = (this.$parent.$el.offsetWidth * 3) / 4;
      this.pickerKey += 1;
    },
    close() {
      this.$emit("close");
    },
    colorToHex(color) {
      var hex = color.toString(16);
      return hex.length == 1 ? "0" + hex : hex;
    },
  },
  computed: {
    defaultLedColor() {
      let color = this.$store.getters.ledColor;
      return (
        "#" +
        this.colorToHex(color.r) +
        this.colorToHex(color.g) +
        this.colorToHex(color.b)
      );
    },
  },
};
</script>
<style scoped>
.color-wheel {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
