<template>
    <h1 class="listh1">
        <router-link to="/addToken"><span>افزودن</span></router-link>
        لیست توکن ها 
    </h1>
  <div class="listContainer">
    <p v-if="!list.length">موردی برای نمایش وجود ندارد</p>
    <div class="itemContainer" v-for="item,index in list" :key="index">
        <div class="itemContent">
            <span class="itemLeft">{{item.title}}</span>
            <span class="itemMid">{{item["expire_time"].split("T")[0]}}</span>
            <span class="itemRight">{{item.description}}</span>
        </div>
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
            showMsg : false,
            err : ''
        }
    },
    methods : {
        endmsg() {
            this.showMsg = false
        },
    },
    async beforeMount () {
        document.title = "لیست توکن ها";
        await axios.get('http://localhost:8000/get_auth_tokens/', {headers : {
            Authorization : `Bearer ${this.$store.state.accessToken}`
        }})
        .then (res => {
            console.log(res.data)
            this.list = res.data["user_tokens"];
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
    border-bottom: 1px solid #cecece;
    padding-bottom: 20px;
    display: flex;
    justify-content: space-between;
}
.listh1 span {
    cursor: pointer;
    background-color: #0da200;
    padding: 10px;
    border-radius: 20px;
    color: #fff;
    font-size: 16px;
    font-weight: normal;

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
    justify-content: space-between; /* Distribute content on both ends */
    align-items: center;
    width: 90%;
    margin: 5px auto;
    background-color: #dbffe8;
    border: 1px solid #0da200;
    padding: 10px;
    border-radius: 5px;
    box-shadow: 0 0 1px 0 #62e048;
}
.itemContent {
    display: flex; /* Use flex layout */
    align-items: center; /* Align items vertically in the center */
    flex-grow: 1; /* Expand to fill available space */
    justify-content: space-between; /* Distribute items evenly */
}
.itemLeft {
    padding: 5px; /* Add spacing between items */
    height: 20px;
    border-radius: 3px;
    background-color: #36ca86;
    margin-right: 10px;
    font-weight: bold;
    color: #fdfdfd;
    text-shadow: 1px 1px #85a06a;
}
.itemMid {
    flex-grow: 1; /* Equal width for all three items */
    padding-right: 30px; /* Add spacing between items */
}
.itemRight {
    color: #4b4b4b;
    font-size: 12px;
    padding: 5px; /* Add spacing between items */
}
.itemRR {
    font-size: 26px;
    cursor: pointer;
    padding-right: 10px; /* Add spacing between items */
    padding-left: 10px; /* Add spacing between items */

}
.display {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background: rgba(0, 0, 0, .50);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 5;
    z-index: 99;
}
.popup {
    z-index: 99;
    background: #dbffe8;
    padding: 50px;
    border-radius: 15px;
    opacity: 0; /* Start with 0 opacity */
    transform: translateY(-20px); /* Start slightly above its final position */
    animation: fadeAndSlide 0.5s ease-out forwards; /* Apply the animation */
}

@keyframes fadeAndSlide {
    to {
        opacity: 1; /* Fade in */
        transform: translateY(0); /* Slide down */
    }
}
</style>