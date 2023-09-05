<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <header class="header">
    <span class="headerLeft">Logo</span>
    <span class="titlesite">NLP Tasks</span>
    <router-link to="/auth">
      <span class="headerRight">X</span>
    </router-link>
  </header>
  <div class="leftSideBar" id="sidebar">
    <router-link to="/admin" v-if="isAdmin">
      <div class="circle" title="پنل ادمین">
        A
      </div>
    </router-link>
    <router-link to="/">
      <div class="circle" title="خلاصه ساز">
          S
      </div>
    </router-link>
    <router-link to="/list" v-if="this.$store.state.accessToken">
      <div class="circle" title="لیست سرویس ها">
        L
      </div>
    </router-link>
    <router-link to="/registerModule" v-if="isRegistered">
      <div class="circle" title="ثبت ماژول جدید">
        X
      </div>
    </router-link>
    <router-link to="/tokenList">
      <div class="circle" title="لیست توکن ها">
        T
      </div>
    </router-link>
    <a href="https://github.com/Iron-Mac/znu-nlp">
      <div class="circle" title="کتابخانه پایتونی">
        G
      </div>
    </a>
  </div>
  <RouterView />
</template>
<script>
import axios from 'axios'

export default {
  data() {
    return {
      isRegistered : false,
      isAdmin : false
    }
  },
  methods : {

  },
  async beforeMount() {
    this.$store.commit('getAccessToken');
    await axios.get('http://localhost:8000/retreive-user', {headers : {
        Authorization : `Bearer ${this.$store.state.accessToken}`
    }})
    .then (res => {
        console.log(res.data)
        this.isRegistered = res.data.registerer;
        this.isAdmin = res.data.admin;
    })
    .catch (err => {
        console.log(err)
        this.err = err.response.data.detail;
        this.showMsg = true;
    })
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
  cursor: pointer;
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
  width: 40px;
  display: flex;
  flex-direction: column;
  padding: 50px 20px;
  align-items: flex-end;
  border: 1px solid #dfdfdf;
  z-index: 100;
}
.circle {
  width: 40px;
  height: 40px;
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
