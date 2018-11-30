<template>
    <div class="box box-solid">
        <div class="box-body">
            <div class="row">
                <div class="col-lg-6">
                    <!-- <label class="btn btn-primary btn-file" style="backgroud-color:#1874CD;">
                        Import<input id="load-file" type="file" name="filer_key_file" @change="upload">
                    </label> -->
                    <button class="btn btn-warning" @click="clearResult">Clear</button>
                    <button class="btn btn-info"  @click="saveReport">Save Report</button>
                </div><!-- /.col-lg-6 -->
                <!-- <div class="col-lg-2">
                    <div class="input-group">
                        <input v-model="targetContext" type="text" class="form-control input-sm" placeholder="Search..." @keyup.enter="popTargetContext(targetContext)">
                        <span class="input-group-btn">
                            <button class="btn btn-primary btn-sm" type="button" @click="popTargetContext(targetContext)">Search</button>
                        </span>
                    </div>
                </div> -->
            </div>
        </div>
    </div>
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
                    title: "Clear Success ：）"
                });
            })
        },
        saveReport: function() {
            this.$http.get('/ui/plugin/tracking/report')
            .then(response=>{
                this.$Notice.success({
                    title: "Save Success :-D",
                    render: h => {
                        return h('span', {style:{wordBreak:'break-all'}},'Save Report at \n "~/.lyrebird/plugins/lyrebird_tracking/report"')
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
