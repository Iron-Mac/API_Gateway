<template>
  <div class="listContainer">
    <div class="itemContainer" v-for="item,index in list" :key="index" @click="redirectTo(item)">
        <span class="itemLeft">{{item.title}}</span>
        <span class="itemMid">{{item.url}}</span>
        <span class="itemRight">{{item.description}}</span>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
    data () {
        return {
            list : [],
            user : ''
        }
    },
    methods : {
        redirectTo(item) {
            if (item["output_type"] == 1) {
                window.location.href = "http://localhost:5173/"
            } else if (item["output_type"] == 2) {
                window.location.href = `http://localhost:5173/output3/${item["id"]}`
            } else if (item["output_type"] == 3) {
                window.location.href = `http://localhost:5173/output2/${item["id"]}`
            }
        }
    },
    async beforeMount () {
        console.log(this.$store.state.accessToken)
        console.log(this.list)
        await axios.get('http://localhost:8000/user-modules', {headers : {
            Authorization : `Bearer ${this.$store.state.accessToken}`
        }})
        .then (res => {
            console.log(res.data)
            this.list = res.data.modules;
            this.user = res.data.user;
        })
        .catch (err => {
            console.log(err)
        })
    }

}
</script>

<style scoped>
.listContainer {
    display: flex;
    direction: rtl;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    width: 70%;
    margin: 100px auto;
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
</style>