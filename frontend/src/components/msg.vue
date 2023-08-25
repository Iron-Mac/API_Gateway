<template>
<div class="msg-container">
    <span class="msg">{{ msg }}</span>
</div>
</template>

<script>
export default {
    props : ['msg'],
    mounted () {
    setTimeout(()=>{
        this.$emit('endmsg');
    },5000)
    }
}
</script>

<style>
.msg-container {
    position: fixed;
    bottom: 30px;
    left: 30px;
    background-color: #c91637;
    height: 30px;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0 1rem 1.5rem rgba(0, 0, 0, .5);
    animation: shake 300ms;
}

.msg {
    font-size: 20px;
    text-align: center;
    color: #FFFFFF;
}

@keyframes shake {
    25% {transform: translateX(11px);}
    50% {transform: translateX(-11px);}
    75% {transform: translateX(11px);}
}
</style>