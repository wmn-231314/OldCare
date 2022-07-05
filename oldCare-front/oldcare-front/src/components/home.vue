<template>
  <div class="home">
    <head-side></head-side>
    <side-bar></side-bar>
  </div>
</template>

<script>
import headSide from "./headSide.vue";
import sideBar from "./sideBar.vue";
export default {
  data() {
    return {
    };
  },
  components: {
    headSide,
    sideBar,
},
  mounted() {},
  methods: {
  },
  created() {
  },
  computed: {},
  watch: {}
};
</script>

<style>
html,
body {
  margin: 0;
  padding: 0;
  font-family: sans-serif;
  background-color: #fff;
  height: 100%;
}

</style>
