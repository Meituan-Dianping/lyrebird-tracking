<template>
    <Card :padding="5">           
        <button class="btn btn-warning" @click="clearResult">Clear</button>
        <button class="btn btn-info"  @click="saveReport">Save Report</button>
    </Card>          
</template>

<script>
module.exports = {
    mounted: function() {
        this.$Notice.config({
            top: 75
        });
    },
    data: function() {
        return {
        };
    },
    methods: {
        clearResult: function() {
            this.$http.get('/ui/plugin/tracking/clear')
            .then(response=>{
                console.log('Clear statistics list!');
                this.$Notice.success({
                    title: "Clear Success"
                });
            })
        },
        saveReport: function() {
            this.$http.get('/ui/plugin/tracking/report')
            .then(response=>{
                this.$Notice.success({
                    title: "Save Success",
                    render: h => {
                        return h('span', {style:{wordBreak:'break-all'}},'Save to \n "~/.lyrebird/plugins/lyrebird_tracking/report"')
                    }
                });
            })
        }
    },
    components: {}
};
</script>

<style>
</style>
