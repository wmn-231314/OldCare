import Vue from 'vue';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import axios from'axios'

Vue.use(ElementUI);

Vue.prototype.$axios=axios;

Vue.prototype.$loginUrl="http://127.0.0.1:9656/login";