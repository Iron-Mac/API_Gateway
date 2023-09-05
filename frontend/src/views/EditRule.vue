<template>
  <h1 class="listh1">ویرایش کاربر - {{ userNmae }}</h1>
  <div class="listContainer">
    <div class="moduleContainer">
        <div class="itemContainer" v-for="item,index in list" :key="index">
            <span class="itemLeft">{{item.title}}</span>
            <span class="itemMid">{{item.url}}</span>
            <span class="itemRight">{{item.description}}</span>
            <span class="itemRR" @click="addModule(item)">+</span>
            <!-- <span class="itemRR" @click="removeModule(item)" v-if="!showPlus">-</span> -->
        </div>
    </div>
    <label>نرخ محدودیت</label>
    <input type="number" class="rateLimit" v-model="rateLimit">
    <label>تاریخ</label>
    <input type="text " class="date" v-model="date" placeholder="1402-08-06 12:45:09">
    <button class="showPopUp" @click="togglePopup">تنظیمات بیشتر</button>
    <div class="display" v-if="showPopup" @click.self="togglePopup">
        <div class="popup">
            <div>
                <label>دسترسی ادمین</label>
                <input type="checkbox" v-model="isAdmin">
            </div>
            <div>
                <label>اجازه ثبت ماژول</label>
                <input type="checkbox" v-model="isRegister">
            </div>
            <button @click="submit" class="submit">ثبت</button>
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
            editID : this.$route.params.editID,
            list : [],
            user : '',
            userModels : {},
            showPopup : false,
            // showPlus : false,
            showMsg : false,
            err : '',
            rateLimit : "",
            date : "",
            isAdmin : false,
            isRegister : false,
            userNmae : ''
        }
    },
    methods : {
        togglePopup() {
            this.showPopup = !this.showPopup
        },
        endmsg() {
            this.showMsg = false
        },
        redirectTo(item) {
            window.location.href = `http://localhost:5173/editRule/${item.id}`
        },
        async addModule(item) {
            const data = {
                "username": this.userNmae,
                "module_id": item.id,
                "limit": parseInt(this.rateLimit),    
                "expire_time": this.date
            }
            await axios.post('http://localhost:8000/set-rate-limit', data , {headers : {
                Authorization : `Bearer ${this.$store.state.accessToken}`
            }})
            .then (res => {
                console.log(res.data)
            })
            .catch (err => {
                console.log(err)
                this.err = err.response.data.detail;
                this.showMsg = true;
            })
        },
        async submit () {
            const data = {
                "username": this.userNmae,
                "is_admin": this.isAdmin,
                "is_registerer": this.isRegister
            }
            await axios.post('http://localhost:8000/edit-user-role', data , {headers : {
                Authorization : `Bearer ${this.$store.state.accessToken}`
            }})
            .then (res => {
                console.log(res.data)
                this.showPopup = false
            })
            .catch (err => {
                console.log(err)
                this.err = err.response.data.detail;
                this.showMsg = true;
            })
        }
    },
    async beforeMount () {
        document.title = "خانه";
        await axios.get('http://localhost:8000/all-module-list', {headers : {
            Authorization : `Bearer ${this.$store.state.accessToken}`
        }})
        .then (res => {
            console.log(res.data)
            this.list = res.data;
            // this.userModels = res.data["user_models"][0]
            // this.user = res.data.user;
        })
        .catch (err => {
            console.log(err)
            this.err = err.response.data.detail;
            this.showMsg = true;
        })

        await axios.get('http://localhost:8000/retreive-user', {headers : {
            Authorization : `Bearer ${this.$store.state.accessToken}`
        }})
        .then (res => {
            console.log(res.data)
            this.userNmae = res.data.username;
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
.moduleContainer {
    display: flex;
    direction: rtl;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    background-color: #dadada;
    padding: 10px 0;
    border-radius: 13px;
    width: 50%;
    height: 100px;
    resize: horizontal;
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
    padding: 0;
    border-radius: 5px;
    box-shadow: 0 0 1px 0 #62e048;
    height: 25px;
}
.itemLeft {
    padding: 5px;
    height: 10px;
    border-radius: 3px;
    background-color: #36ca86;
    margin-right: 10px;
    font-weight: bold;
    color: #fdfdfd;
    text-shadow: 1px 1px #85a06a;
    font-size: 12px;
}
.itemMid {
    padding: 0;
    margin: 0;
    margin-right: 20px;
    font-size: 12px;
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
    background: #fff;
    padding: 50px;
    border-radius: 15px;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
}
.popup button {
    margin-top: 10px;
}
</style>