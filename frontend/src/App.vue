<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="leftSideBar">
    <router-link to="/auth">
      <div class="circle">
          A
      </div>
    </router-link>
    <router-link to="/">
      <div class="circle">
          S
      </div>
    </router-link>
    <router-link to="/list">
      <div class="circle">
          L
      </div>
    </router-link>
    <router-link to="/registerModule">
      <div class="circle">
        X
      </div>
    </router-link>
  </div>
  <RouterView />
</template>
<script>
export default {
  beforeMount() {
    this.$store.commit('getAccessToken')
  }
}
</script>

<style>
@font-face {
    font-family: Sahel;
    src: url(./assets/Sahel-FD.ttf);
}
* {
    font-family: Sahel;
}
body {
  margin: 0;
  padding: 0;
}
.leftSideBar {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  background-color: #d0f9da;
  width: 50px;
  display: flex;
  flex-direction: column;
  padding: 50px 10px;
  align-items: center;
  border: 1px solid #89db82;
}
.circle {
  width: 50px;
  height: 50px;
  border-radius: 25px;
  background-color: #8affa2;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
  cursor: pointer;
  border: 1px solid #0da200;
  box-shadow: 0 0 7px 0px #70d056;
}
a {
  all: unset;
}
</style>
