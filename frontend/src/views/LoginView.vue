<template>
    <div class="register-container">
        <div class="container">
            <div class="tabs">
                <button id="loginTab" class="loginTab" @click="toggleLogin">ورود</button>
                <button id="signupTab" class="signupTab border-bottom" @click="toggleSignup">ثبت نام</button>
            </div>
            <div class="cart-container">
                <div class="register">
                    <div class="login" id="loginFirst">
                        <p class="text">نام کاربری</p>
                        <input type="text" class="reg-input" id="login-username" v-model="username">
                        <p class="text">شماره تلفن</p>
                        <input type="text" class="reg-input" v-model="email" id="login-email">
                        <p class="text">گذرواژه</p>
                        <input type="text" class="reg-input" v-model="pass" id="login-pass">
                        <button class='submit' @click="submitRegister">ارسال کد</button>
                    </div>
                    <div class="login none" id="loginsec">
                        <p class="text">کد</p>
                        <input type="text" class="reg-input" id="login-username" v-model="code">
                        <button class='submit' @click="submitCode">تایید کد</button>
                    </div>
                </div>
                <div class="auth none">
                    <div class="login">
                        <p class="text">نام کاربری</p>
                        <input type="text" class="reg-input" v-model="username" id="signup-username">
                        <p class="text">گذرواژه</p>
                        <input type="text" class="reg-input" v-model="pass" id="signup-pass">
                        <button class='submit' @click="submitAuth">ورود</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <msg v-if="showMsg" @endmsg="endmsg" :msg="err"/>
</template>

<script>
import axios from 'axios';
import msg from '../components/msg.vue'

export default {
    components : {msg},
    data() {
        return {
            username : '',
            email : '',
            pass : '',
            code : '',
            accessToken : '',
            showMsg : false,
            err : ''
        }
    },
    methods : {
        endmsg() {
            this.showMsg = false
        },
        toggleSignup() {
            document.getElementById('loginTab').classList.remove('border-bottom');
            document.getElementById('signupTab').classList.add('border-bottom');
            document.getElementsByClassName('register')[0].classList.remove('none');
            document.getElementsByClassName('auth')[0].classList.add('none');
            
        },
        toggleLogin() {
            document.getElementById('loginTab').classList.add('border-bottom');
            document.getElementById('signupTab').classList.remove('border-bottom');
            document.getElementsByClassName('auth')[0].classList.remove('none');
            document.getElementsByClassName('register')[0].classList.add('none');
            
        },
        async submitRegister() {
            if (this.username && this.email && this.pass ) {
                const data = {
                    "username": this.username,
                    "password": this.pass,
                    "phone_number": this.email
                }
                console.log(data)
                await axios.post('http://localhost:8000/register',data)
                .then(res => {
                    console.log(res.data)
                    document.getElementById('loginsec').classList.remove('none');
                    document.getElementById('loginFirst').classList.add('none');
                    document.getElementById('loginsec').classList.remove('none');
                    document.getElementById('loginFirst').classList.add('none');
                })
                .catch(err=> {
                    this.err = err.response.data.detail;
                    this.showMsg = true;
                    console.log(err)
                })
            }
        },
        async submitCode() {
            const data = {
                "username" : this.username,
                "verification_code" : this.code
            }
            console.log(data)
            await axios.post('http://localhost:8000/verify-user',data)
            .then(res => {
                console.log(res.data);
                window.location.href = "http://localhost:5173/";
            })
            .catch(err=> {
                this.err = err.response.data.detail;
                this.showMsg = true;
                console.log(err)
            })
        },
        async submitAuth() {
            const data = {
                "username": this.username,
                "password": this.pass
            }
            console.log(data)
            await axios.post('http://localhost:8000/login',data)
            .then(res => {
                console.log(res.data)
                this.$store.state.accessToken = res.data['access_token']
                this.$store.state.refreshToken = res.data['refresh_token']
                this.$store.commit('saveAccessToken',this.$store.state.accessToken);
                this.$store.commit('saveRefreshToken',this.$store.state.refreshToken);
                window.location.href = "http://localhost:5173/list"
            })
            .catch(err=> {
                console.log(err)
                this.err = err.response.data.detail;
                this.showMsg = true;
            })
        }
    },
    beforeMount() {
        document.title = "ورود/ثبت نام";
    }
    
}
</script>

<style scoped >
.container {
    display: flex;
    flex-direction: column;
    justify-content: stretch;
}

.tabs {
    display: flex;
    flex-direction: row;
    justify-content: stretch;
    margin: 0;
    flex-grow: 1;
}

.loginTab,
.signupTab {
    flex-grow: 1;
    border: none;
    border-radius:none ;
    height: 62px;
    background-color: #FFFFFF;
    cursor: pointer;
    font-size: 20px;
    border-radius: 10px 0 0 0;
}

.signupTab {
    border-radius:  0 10px 0 0;
}

.border-bottom {
    border-bottom: solid 2px #1bb140;
}

.cart-container {
    margin: 0;
    padding: 0;
    box-shadow: 0 .5rem 1rem rgba(0, 0, 0, .20);
}

.login {
    width: 516px;
    background: white;
    border-radius: 0 0 10px 10px;
    text-align: left;
}


.auth,
.register {
    display: block;
}

.none {
    display: none !important;
}
.register-container {
    position: fixed;
    top: 0;
    right: 70px;
    left: 0;
    bottom: 0;
    background-color: #efede6;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 35px 0;
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

.msg {
    margin-top: 18px;
    margin-right: 8.5%;
}

.ivalid-input {
    border: 2px solid rgba(223, 15, 15, 0.38);
    animation: shake 300ms;
}

@keyframes shake {
    25% {transform: translateX(6px);}
    50% {transform: translateX(-6px);}
    75% {transform: translateX(6px);}
}

</style>