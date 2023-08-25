<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <header class="header">
    <span class="headerLeft">Logo</span>
    <span class="titlesite">NLP Tasks</span>
    <span class="headerRight">X</span>
  </header>
  <div class="leftSideBar" id="sidebar">
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
  // methods : {
  //   toggleSidebar() {
  //     document.getElementById('sidebar').style.width = '200px'
  //   }
  // },
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
  background-color: #efede6;
}
.header {
  position: sticky;
  top: 0;
  right: 90px;
  left: 0;
  background: #fefff9;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 80px;
  z-index: 100;
  width: 100%;
  border-bottom: 1px solid #dfdfdf;
}
.headerLeft {
  text-align: left;
  margin-left: 50px;
}
.headerRight {
  margin-right: 50px;
  width: 115px;
  text-align: right;
}

.titlesite {
  margin-left: 70px;
}
.leftSideBar {
  position: fixed;
  top: 80px;
  right: 0;
  bottom: 0;
  background-color: #fefff9;
  width: 50px;
  display: flex;
  flex-direction: column;
  padding: 50px 20px;
  align-items: flex-end;
  border: 1px solid #dfdfdf;
  z-index: 100;
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
