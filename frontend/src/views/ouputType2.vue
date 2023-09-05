<template>
  <div class="inputType2Container">
    <div class="out2">
        <div class="out2Header">
            نام ماژول - {{ title }}
        </div>
        <textarea type="text" class="inputType2" v-model="inputType"></textarea>
    </div>
    <button @click="post" class="post">ارسال</button>
    <div class="table" v-if="showTable">
        <p>خروجی ماژول</p>
    <table class="styled-table">
    <thead>
      <tr>
        <th class="tdindex">Index</th>
        <th>Value</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="index,item in list" :key="index">
        <td class="tdindex">{{item}}</td>
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
            dis : ''
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