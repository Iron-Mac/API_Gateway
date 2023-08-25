<template>
<div class="regModContainer">
    <div class="login" id="loginFirst">
        <p class="text">عنوان</p>
        <input type="text" class="reg-input" id="title" v-model="title">
        <p class="text">توضیحات</p>
        <input type="text" class="reg-input" v-model="dis" id="dis">
        <p class="text">URL</p>
        <input type="text" class="reg-input" v-model="url" id="url">
        <p class="text">نوع خروجی</p>
        <input type="text" class="reg-input" v-model="out" id="out">
        <button class='submit' @click="submitRegister">ارسال</button>
    </div>
</div>

</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            title : '',
            dis : '',
            url : '',
            out : ''
        }
    },
    methods : {
        async submitRegister() {
            if (this.title && this.dis && this.url && this.out) {
                const data = {
                    title :this.title,
                    description :this.dis,
                    url :this.url,
                    limit : 20,
                    "output_type" :parseInt(this.out),
                }
                console.log(data)
                await axios.post('http://localhost:8000/create-module',data,{headers : {
                    Authorization : `Bearer ${this.$store.state.accessToken}`
                }})
                .then(res => {
                    console.log(res);
                    window.location.href = "http://localhost:5173/"
                })
                .catch(err=> {
                    console.log(err)
                })
            }
        }
    }
}
</script>

<style scoped>
.regModContainer {
    display: flex;
    justify-content: center;
    align-content: center;
    position: fixed;
    top: 0;
    right: 70px;
    left: 0;
    bottom: 0;
}
.login {
    width: 516px;
    background: white;
    border-radius: 0 0 10px 10px;
    text-align: left;
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
    border-radius: 10px;
    direction: ltr;
    font-size: 20px;
    box-shadow: 0 .5rem 1rem rgba(0, 0, 0, .15);
}
.submit {
    width: 306px;
    height: 67px;
    background: #1bb140;
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
    background-color:#0edd42;
}
</style>