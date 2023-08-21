import { createStore } from 'vuex';

export default createStore({
  state: {
    accessToken : '',
    refreshToken : ''
  },
  mutations: {
    saveAccessToken(state) {
        const parsed = JSON.stringify(state.accessToken);
        localStorage.setItem('accessToken', parsed);
    },
    saveRefreshToken(state) {
        const parsed = JSON.stringify(state.refreshToken);
        localStorage.setItem('refreshToken', parsed);
    },
    getAccessToken(state) {
        state.accessToken = JSON.parse(localStorage.getItem('accessToken'))
    }
  },
  actions: {},
  modules: {}
})