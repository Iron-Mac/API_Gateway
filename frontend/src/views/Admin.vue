<template>
    <h1 class="listh1">لیست یوزر ها</h1>
  <div class="listContainer">
    <div class="itemContainer" v-for="item,index in list" :key="index" @click.self="redirectTo(item)">
        <span class="itemLeft">{{item.username}}</span>
        <span class="itemMid">{{item['phone_number']}}</span>
        <!-- <span class="itemRight">{{item.description}}</span> -->
    </div>
  </div>
  <msg v-if="showMsg" @endmsg="endmsg" :msg="err"/>
</template>

<script>
import axios from 'axios'
import msg from '../components/msg.vue'

export default {
    components : {msg},
    data () {
        return {
            list : [],
            user : '',
            userModels : {},
            showPopup : false,
            showMsg : false,
            err : ''
        }
    },
    methods : {
        endmsg() {
            this.showMsg = false
        },
        redirectTo(item) {
            window.location.href = `http://localhost:5173/editRule/${item.id}`
            console.log(item.id)
        }
    },
    async beforeMount () {
        document.title = "پنل ادمین";
        console.log(this.list)
        await axios.get('http://localhost:8000/all-user-list', {headers : {
            Authorization : `Bearer ${this.$store.state.accessToken}`
        }})
        .then (res => {
            console.log(res.data)
            this.list = res.data;
        })
        .catch (err => {
            console.log(err)
            this.err = err.response.data.detail;
            this.showMsg = true;
        })
    }

}
</script>

<style scoped>
.listh1 {
    width: 70%;
    margin: 50px auto;
    margin-top: 50px;
    text-align: center;
    border-bottom: 1px solid #9e9e9e;
    padding-bottom: 20px;
}
.listContainer {
    display: flex;
    direction: rtl;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    width: 70%;
    margin: 0 auto;
    background-color: #f5f5f5;
    padding: 50px 0;
    border-radius: 13px;
    box-shadow: 0 .5rem 1rem rgba(0, 0, 0, .10);
}
.itemContainer {
    margin-bottom: 15px;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    width: 90%;
    margin: 5px auto;
    background-color: #dbffe8;
    border: 1px solid #0da200;
    padding: 10px;
    border-radius: 5px;
    box-shadow: 0 0 1px 0 #62e048;
}
.itemLeft {
    padding: 10px;
    height: 20px;
    border-radius: 3px;
    background-color: #36ca86;
    margin-right: 10px;
    font-weight: bold;
    color: #fdfdfd;
    text-shadow: 1px 1px #85a06a;
}
.itemMid {
    margin-right: 20px;
}
.itemRight {
    color: #4b4b4b;
    font-size: 12px;
    padding-right: 15px;
}
.itemRR {
    justify-self: flex-end;
    font-size: 26px;
    cursor: pointer;
    margin-right: 50px;
}
</style>