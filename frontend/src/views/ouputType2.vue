<template>
  <div class="inputType2Container">
    <div class="out2">
        <div class="out2Header">
            نام ماژول - {{ title }}
        </div>
        <textarea type="text" class="inputType2" v-model="inputType"></textarea>
    </div>
    <button @click="post" class="post" v-if="!isLoading">ارسال</button>
    <button class="post" disabled v-if="isLoading">
        <div class="lds-ellipsis"><div></div><div></div><div></div><div></div></div>
    </button>
    <div class="table" v-if="showTable">
        <p class="outmodule">خروجی ماژول</p>
    <table class="styled-table">
    <thead>
      <tr>
        <th>Value</th>
        <th>Token</th>
        <th class="tdindex">Index</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="item,index in list" :key="index">
        <td class="tdindex">{{item[1]}}</td>
        <td>{{ item[0] }}</td>
        <td>{{index}}</td>
      </tr>
    </tbody>
    </table>
    </div>
    <div class="dis">
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
    data() {
        return {
            inputType : '',
            showTable : false,
            list : [],
            showMsg : false,
            err : '',
            title : '',
            dis : '',
            isLoading : false
        }
    },
    methods : {
        async post() {
            if (this.inputType) {
                this.isLoading = true;
                const data = {
                    "module_id": this.$route.params.out2Code,
                    "input_data": this.inputType
                }
                await axios.post('http://localhost:8000/process-module',data,{headers : {
                    Authorization : `Bearer ${this.$store.state.accessToken}`
                }})
                .then(res => {
                    this.isLoading = false;
                    this.list = res.data['output_list']
                    this.showTable = true;
                    console.log(res)
                })
                .catch(err => {
                    console.log(err)
                    this.err = err.response.data.detail;
                    this.showMsg = true;
                    this.isLoading = false;
                })
            }
        },
        endmsg() {
            this.showMsg = false
        },
    },
    async beforeMount() {
        document.title = "سرویس";
        await axios.get(`http://localhost:8000/retreive-module/${this.$route.params.out2Code}`,{headers : {
            Authorization : `Bearer ${this.$store.state.accessToken}`
        }})
        .then(res => {
            this.title = res.data.title
            this.dis = res.data.description
        })
        .catch(err => {
            console.log(err)
            this.err = err.response.data.detail;
            this.showMsg = true;
        })
    }
}
</script>

<style scoped>
.inputType2Container {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    direction: rtl;
}
.inputType2 {
    margin: 30px auto;
    height: 400px;
    width: 600px;
    border: 1px solid #cfcfcf;
    border-radius: 15px;
    resize: none;
    font-size: 22px;
    padding: 10px;
    outline: none;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
}
.out2Header {
    margin-top: 30px;
    display: flex;
    justify-content: center;
    align-items: center;
}
.dis {
    margin-top: 30px;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    width: 70%;
    margin-bottom: 50px;
    direction: rtl;
    font-size: x-large;
}
.dis p {
    font-weight: bold;
}
.post {
    width: 200px;
    height: 45px;
    background: #009879;
    border-radius: 50px;
    border: none;
    margin-bottom: 30px;
    color: white;
    font-weight: bold;
    font-size: 22px;
    box-shadow: 0 1rem 3rem rgb(0, 0, 0, 0.35);
    cursor: pointer;
}
.post:hover {
    background-color:#095143;
}
.table {
    padding: 15px;
    resize: auto;
    max-height: 500px;
}
.table p {
    border-bottom: 1px solid #cfcfcf;
    text-align: center;
}
.styled-table {
    border-collapse: collapse;
    margin: 25px 0;
    padding: 50px;
    font-size: 1.4em;
    max-height: 500px;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
}
.styled-table thead tr {
    background-color: #009879;
    color: #ffffff;
    text-align: left;
}
.styled-table th,
.styled-table td {
    padding: 15px 70px;
}
.styled-table tbody tr {
    border-bottom: 1px solid #dddddd;
}

.styled-table tbody tr:nth-of-type(even) {
    background-color: #f3f3f3;
}

.styled-table tbody tr:last-of-type {
    border-bottom: 2px solid #009879;
}

.tdindex{
    width: 50px !important;
}

.outmodule {
    font-size: x-large;
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

  .lds-ellipsis {
  display: inline-block;
  position: relative;
  width: 80px;
  height: 37px;
}
.lds-ellipsis div {
  position: absolute;
  top: 12px;
  width: 13px;
  height: 13px;
  border-radius: 50%;
  background: #fff;
  animation-timing-function: cubic-bezier(0, 1, 1, 0);
}
.lds-ellipsis div:nth-child(1) {
  left: 8px;
  animation: lds-ellipsis1 0.6s infinite;
}
.lds-ellipsis div:nth-child(2) {
  left: 8px;
  animation: lds-ellipsis2 0.6s infinite;
}
.lds-ellipsis div:nth-child(3) {
  left: 32px;
  animation: lds-ellipsis2 0.6s infinite;
}
.lds-ellipsis div:nth-child(4) {
  left: 56px;
  animation: lds-ellipsis3 0.6s infinite;
}
@keyframes lds-ellipsis1 {
  0% {
    transform: scale(0);
  }
  100% {
    transform: scale(1);
  }
}
@keyframes lds-ellipsis3 {
  0% {
    transform: scale(1);
  }
  100% {
    transform: scale(0);
  }
}
@keyframes lds-ellipsis2 {
  0% {
    transform: translate(0, 0);
  }
  100% {
    transform: translate(24px, 0);
  }
}
</style>