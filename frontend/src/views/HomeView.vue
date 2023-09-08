<template>
    <div class="appContainer">
        <div class="sumContainer">
            <div class="summarizerSection">
                <div class="sumHeader">
                    {{ this.$route.params.out1Code == 'defult' ? 'خلاسه ساز متن' : 'کامیونیتی ماژول'}}
                </div>
                <div class="sumBody">
                    <div class="inputContainer">
                        <textarea name="input" id="input" placeholder="متن مورد نظر را وارد کنید"></textarea>
                        <button @click="summarize">خلاصه‌ نویسی</button>
                    </div>
                    <div class="outputContainer" @click="copy">
                        <textarea name="output" id="output" disabled >نتیجه</textarea>
                        <p>{{ `تعداد: ${jomle} جمله - ${klme} کلمه`}}</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="introContainer" v-if="isHome">
            <div class="introSection">
                <p>معرفی سامانه خلاصه‌سازی

خسته از غرق شدن در دریایی از متون و مقالات؟ آیا به دنبال راهی سریع و موثر برای خلاصه کردن محتواها و مطالب مختلف هستید؟ ما با افتخار به شما سامانه خلاصه‌سازی را معرفی می‌کنیم!

سامانه خلاصه‌سازی، یک ابزار هوش مصنوعی پیشرفته است که به شما کمک می‌کند تا با سرعت و دقت بالا، اطلاعات کلیدی متون را استخراج کرده و به صورت خلاصه و مختصری ارائه دهید. با استفاده از تکنیک‌های پردازش زبان طبیعی، این سامانه قادر است به طور خودکار مفاهیم اصلی و اهمیت‌های مختلف متون را تشخیص داده و در قالب یک خلاصه قابل فهم ارائه نماید.</p>
                <div class="table">
                    <div class="row">
                        <span>test</span>
                        <span class="sec">test</span>
                    </div>
                    <div class="row">
                        <span>test</span>
                        <span class="sec">test</span>
                    </div>
                    <div class="row">
                        <span>test</span>
                        <span class="sec">test</span>
                    </div>
                    <div class="row">
                        <span>test</span>
                        <span class="sec">test</span>
                    </div>
                </div>
            </div>
        </div>
        <div class="dis" v-if="!isHome">
            <p>توضیحات :</p>
            {{ dis }}
        </div>
    </div>
    <msg v-if="showMsg" @endmsg="endmsg" :msg="err"/>
</template>

<script>
import axios from 'axios';
import msg from '../components/msg.vue'

export default {
    components : {msg},
    data () {
        return {
            list : [],
            showMsg : false,
            err : '',
            isHome : this.$route.params.out1Code == 'defult' ? true : false,
            klme : 0,
            jomle : 0
        }
    },
    methods : {
        copy() {
            console.log('m')
            var r = document.createRange();
            r.selectNode(document.getElementById("output"));
            window.getSelection().removeAllRanges();
            window.getSelection().addRange(r);
            document.execCommand('copy');
            window.getSelection().removeAllRanges();
        },
        async summarize() {
            let outputElement = document.getElementById('output')
            if(this.$route.params.out1Code == 'defult') {
                await axios.post('http://localhost:8000/mock1',{'input_data' : document.getElementById('input').value},{ headers : {
                    Authorization : `Bearer ${this.$store.state.accessToken}`
                }
                })
                .then(res=> {
                    outputElement.value = res.data.result
                    this.klme = res.data.result.split(" ").length;
                    this.jomle = res.data.result.split(".").length;
                })
                .catch(err=> {
                    console.log(err)
                    this.err = err.response.data.detail;
                    this.showMsg = true;
                })
            } else {
                let outputElement = document.getElementById('output')
                const data = {
                    "module_id": this.$route.params.out1Code,
                    "input_data": document.getElementById('input').value
                }
                await axios.post('http://localhost:8000/process-module',data,{headers : {
                    Authorization : `Bearer ${this.$store.state.accessToken}`
                }})
                .then(res => {
                    outputElement.value = res.data.result;
                    this.dis = res.data.description;
                    console.log(res)
                })
                .catch(err => {
                    console.log(err)
                    this.err = err.response.data.detail;
                    this.showMsg = true;
                })
            }
        },
        endmsg() {
            this.showMsg = false
        },

    },
    beforeMount() {
        document.title = "خلاصه ساز";
    }
}
</script>

<style scoped>
.sumContainer {
    width: 100%;
    background-color: rgb(228, 242, 231);
    display: flex;
    justify-content: center;
    align-items: center;
    padding-bottom: 100px;
}
.summarizerSection {
    margin-top: 50px;
    width: 70%;
}
.sumHeader {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 52px;
    border-radius: 25px 25px 0 0;
    background-color: #fff;
    font-weight:bold;
}
.sumHeader button {
    background: #009879;
    color: rgb(255, 255, 255);
    border-radius: 24px;
    padding: 8px 16px;
    height: 32px;
    border: none;
    outline: none;
    margin: 10px;
}
.sumBody {
    width: 100%;
    display: flex;
}
.inputContainer {
    width: 50%;
    display: flex;
    flex-direction: column;
    background-color: #fff;
    box-shadow: 0 .5rem 1rem rgba(0, 0, 0, .1);
}
.outputContainer {
    width: 50%;
    display: flex;
    flex-direction: column;
    background-color: #fff;
    box-shadow: 0 .5rem 1rem rgba(0, 0, 0, .1);
}
.inputContainer textarea,
.outputContainer textarea {
    height: 400px;
    resize: none;
    border: none;
    border-top: 1px solid rgb(199, 199, 199);
    font-size: 22px;
    padding: 10px;
    outline: none;
}
.inputContainer {
    border-radius: 0 0 0 25px;
    border-right: 1px solid rgb(199, 199, 199);
}
.inputContainer button {
    background: #009879;
    color: rgb(255, 255, 255);
    border-radius: 24px;
    padding: 8px 16px;
    height: 40px;
    border: none;
    outline: none;
    width: 105px;
    align-self: flex-end;
    margin: 10px;
    cursor: pointer;
}
.inputContainer button:hover {
    background: #095143;
}
.outputContainer {
    border-radius: 0 0 25px 0;
}
.outputContainer textarea:disabled {
    background-color: #fff;
}
.outputContainer p{ 
    margin: 18px;
}
.introContainer {
    direction: rtl;
    width: 100%;
    background-color: rgb(238, 238, 238);
}
.introSection {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    padding-top: 100px;
    padding-bottom: 100px;
    margin: auto;
    width: 60%;
}
.introSection p {
    margin-bottom: 60px;
}
.row {
    display: flex;

}
.row span{
    display: block;
    border: 1px solid rgb(199, 199, 199);
    padding: 15px;
    width: 150px;
    text-align: center;
}
.sec {
    width: 350px !important;
}
.dis {
    margin-top: 30px;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    margin-bottom: 50px;
    direction: rtl;
}
.dis p {
    font-weight: bold;
}
</style>