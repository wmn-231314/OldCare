import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

// const actions = {}
// const mutations = {
//     handleUserName: (state, user_name) => {
//         state.user_name = user_name
//         localStorage.setItem('user_name', user_name)
//         console.log(user_name)
//     },
//     login:(state,n) => {
//         //传入登录状态islogin
//         let islogin = JSON.parse(n);
//         localStorage.setItem('islogin',JSON.stringify(islogin));
//         console.log(islogin);
//         state.islogin = islogin;
//     },

      
    
// }

// const state = {
//     user_name: '' || localStorage.getItem('user_name'),
//     islogin:'0',
//     ser: null,
//     // token
//     token:localStorage.getItem('token') ? localStorage.getItem('token'):'',
    
// }
// const getters = {
//     userName: (state) => state.user_name
// }

// const store = new Vuex.Store({
//     actions,
//     mutations,
//     state,
//     getters
// })
// export default  store 

const state = {
    isLogin:'0',
    user_name:'' || localStorage.getItem('user_name'),
    ser: null,
    // token
    token:localStorage.getItem('token') ? localStorage.getItem('token'):'',
};
export default new Vuex.Store({
    state,
    getters:{ // 监听数据变化
        getStorage(state){ // 获取本地存储登陆信息
            if(!state.token){
                state.token = JSON.parse(localStorage.getItem('token'))
            }
            return state.token
        },
        userName: (state) => state.user_name
    },
    mutations:{
        $_setToken(state,value){        // 设置存储token
            state.token = value
            localStorage.setItem('token',value)
            // console.log(token)
        },
        $_removeStorage(state,value){   // 删除token
            localStorage.removeItem('token')
        },
        handleUsername:(state,value) => {
            state.user_name = value
            localStorage.setItem('user_name',value)
            console.log(user_name)
        }
    }
})
