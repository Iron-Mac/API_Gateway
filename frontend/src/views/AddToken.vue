<template>
    <div class="regModContainer">
        <h1>فرم ثبت توکن</h1>
        <div class="login" id="loginFirst">
            <p class="text">عنوان</p>
            <input type="text" class="reg-input" id="title" v-model="title">
            <p class="text">توضیحات</p>
            <input type="text" class="reg-input" v-model="dis" id="dis">
            <p class="text">محدودیت زمانی</p>
            <input type="text" class="reg-input" v-model="time" id="time">
            <p class="text" v-if="out">توکن</p>
            <div class="copy-container" v-if="out">
                <input type="text" class="reg-input url-input copy-input" id="out" @click="copy" v-model="out">
                <button @click="copy" class="copy-but">copy</button>
            </div>
            <button class='submit' @click="submitRegister" v-if="!out">ثبت توکن</button>
        </div>
        <msg v-if="showMsg" @endmsg="endmsg" :msg="err"/>
    </div>
</template>

<script>
import axios from 'axios';
import msg from '../components/msg.vue'

export default {
    components : {msg},
    data() {
        return {
            title : '',
            dis : '',
            url : '',
            time : '',
            out : '',
            showMsg : false,
            err : ''
        }
    },
    methods : {
        copy() {
            var r = document.createRange();
            r.selectNode(document.getElementById("out"));
            window.getSelection().removeAllRanges();
            window.getSelection().addRange(r);
            document.execCommand('copy');
            window.getSelection().removeAllRanges();
        },
        endmsg() {
            this.showMsg = false
        },
        async submitRegister() {
            if (this.title && this.dis && this.time) {
                const data = {
                    title : this.title,
                    description : this.dis,
                    "expire_days" : parseInt(this.time)
                }
                console.log(data)
                await axios.post('http://localhost:8000/create_auth_tokens/',data,{headers : {
                    Authorization : `Bearer ${this.$store.state.accessToken}`
                }})
                .then(res => {
                    console.log(res.data);
                    this.out = res.data['token'];
                })
                .catch(err=> {
                    this.err = err.response.data.detail;
                    this.showMsg = true;
                    console.log(err)
                })
            }
        }
    },
        beforeMount() {
            document.title = "ثبت توکن";
        }
}
</script>

<style>
.regModContainer {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    position: fixed;
    top: 0;
    right: 10px;
    left: 0;
    bottom: 0;
}
.login {
    width: 516px;
    background: white;
    border-radius: 0 0 10px 10px;
    text-align: left;
    box-shadow: 0 .5rem 1rem rgba(0, 0, 0, .20);
}
.text {
    margin-top: 0;
    padding-top: 20px;
    margin-right: 40px;
    margin-bottom: 0;
    font-size: 20px;
    color: rgba(0, 0, 0, 0.63);
    text-align: right;
}
.reg-input {
    padding-left: 3%;
    margin-top: 16px;
    margin-left: 30px;
    width: 441px;
    height: 62px;
    border: 1px solid rgba(0, 0, 0, 0.38);
    direction: ltr;
    font-size: 20px;
    box-shadow: 0 .5rem 1rem rgba(0, 0, 0, .15);
    border-radius: 15px;
}
.copy-but {
    border-radius: 0 10px 10px 0;
    border: none;
    background-color: #1bb140;
    width: 75px;
    color: #EEEEEE;
    cursor: pointer;
    height: 66px;
}
.copy-input {
    border-radius: 10px 0 0 10px;
    cursor: not-allowed;
    width: 366px;
}
.copy-container {
    display: flex;
    justify-content: flex-start;
    align-items: flex-end;
    margin-bottom: 15px;
}
.submit {
    width: 306px;
    height: 67px;
    background: #009879;
    border-radius: 50px;
    border: none;
    margin: 28px 105px;
    color: white;
    font-weight: bold;
    font-size: 22px;
    box-shadow: 0 1rem 3rem rgb(0, 0, 0, 0.35);
    cursor: pointer;
}
.submit:hover {
    background-color:#095143;
}
</style>