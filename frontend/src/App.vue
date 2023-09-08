<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <header class="header">
    <span class="headerLeft"><img src="./assets/nlp.png" alt=""></span>
    <span class="titlesite">NLP Tasks</span>
    <router-link to="/auth">
      <span v-if="this.$store.state.accessToken" class="usrname">{{ userName }}</span>
      <span class="headerRight"><img src="./assets/user.png" alt=""></span>
    </router-link>
  </header>
  <div class="leftSideBar" id="sidebar">
    <router-link to="/admin" v-if="isAdmin">
      <div class="circle" title="پنل ادمین">
        <img src="./assets/admin.png" alt="">
      </div>
    </router-link>
    <router-link to="/">
      <div class="circle" title="خلاصه ساز">
          <img src="./assets/compose.png" alt="">
      </div>
    </router-link>
    <router-link to="/list" v-if="this.$store.state.accessToken">
      <div class="circle" title="لیست سرویس ها">
        <img src="./assets/list.png" alt="">
      </div>
    </router-link>
    <router-link to="/registerModule" v-if="isRegistered">
      <div class="circle" title="ثبت ماژول جدید">
        <img src="./assets/module.png" alt="">
      </div>
    </router-link>
    <router-link to="/tokenList">
      <div class="circle" title="لیست توکن ها">
        <img src="./assets/chip.png" alt="">
      </div>
    </router-link>
    <a href="https://github.com/Iron-Mac/znu-nlp">
      <div class="circle" title="کتابخانه پایتونی">
        <img src="./assets/python.png" alt="">
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
      isAdmin : false,
      userName : ''
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
        this.userName = res.data.username;
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
.usrname {
  color: rgb(139, 139, 139);
  margin-right: 10px;
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
  margin-right: 5px;
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
.circle img {
  width: 30px;
  height: 30px;
}
a {
  all: unset;
}
</style>
