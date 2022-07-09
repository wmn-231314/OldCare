import Vue from 'vue';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import axios from'axios'

Vue.use(ElementUI);

Vue.prototype.$axios=axios;

Vue.prototype.$loginIdUrl="https://l4159b2312.imdo.co";
Vue.prototype.$loginFaceUrl="https://l4159b2312.imdo.co";