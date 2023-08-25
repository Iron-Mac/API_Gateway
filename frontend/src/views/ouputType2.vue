<template>
  <div class="inputType2Container">
    <div class="out2">
        <div class="out2Header">
            شناسه ماژول - {{ this.$route.params.out2Code }}
        </div>
        <textarea type="text" class="inputType2" v-model="inputType"></textarea>
    </div>
    <button @click="post" class="post">ارسال</button>
    <div class="table" v-if="showTable">
        <div class="row" v-for="index,item in list" :key="index">
            <span class="num">{{index}}</span>
            <span>{{item[0]}}</span>
            <span class="sec">{{item[1]}}</span>
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
            inputType : '',
            showTable : false,
            list : [],
            showMsg : false,
            err : ''
        }
    },
    methods : {
        async post() {
            if (this.inputType) {
                const data = {
                    "module_id": this.$route.params.out2Code,
                    "input_data": this.inputType
                }
                await axios.post('http://localhost:8000/process-module',data,{headers : {
                    Authorization : `Bearer ${this.$store.state.accessToken}`
                }})
                .then(res => {
                    this.list = res.data['output_list']
                    this.showTable = true;
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
        document.title = "سرویس";
    }
}
</script>

<style scoped>
.inputType2Container {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
}
.inputType2 {
    margin:10px auto;
    height: 400px;
    width: 600px;
    border: 1px solid #353535;
    border-radius: 15px;
    resize: none;
    font-size: 22px;
    padding: 10px;
    outline: none;
}
.out2Header {
    margin-top: 30px;
    display: flex;
    justify-content: center;
    align-items: center;
}
.post {
    width: 200px;
    height: 45px;
    background: #1bb140;
    border-radius: 50px;
    border: none;
    margin-bottom: 30px;
    color: white;
    font-weight: bold;
    font-size: 22px;
    box-shadow: 0 1rem 3rem rgb(0, 0, 0, 0.35);
    cursor: pointer;
}
.submit:hover {
    background-color:#0edd42;
}
.table {
    border: 1px solid #0edd42;
    padding: 50px;
    resize: auto;
    max-height: 500px;
}
.row {
    display: flex;
}
.row span{
    display: block;
    border: 1px solid rgb(199, 199, 199);
    padding: 15px;
    width: 250px;
    text-align: center;
}
.sec {
    width: 250px !important;
}
.num {
    width: 50px !important;
}
</style>