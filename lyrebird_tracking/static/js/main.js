Vue.config.devtools = true;

iview.lang('en-US');

new Vue({
    el: '#app',
    data: {},
    components: {
        'tracking': httpVueLoader('/ui/plugin/tracking/static/component/main.vue')
    }
})