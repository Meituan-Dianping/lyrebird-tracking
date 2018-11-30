<template>
    <div>
        <banner></banner>
        <div class="row">
            <div class="col-md-6">
                <tracking-list :trackingdata="allTrackingData"  @detail="getTrackingIndex" @content="getCurrentContent"></tracking-list>
            </div>
            <div class="col-md-6" v-if="currentTracking">
                <tracking-detail :trackingdetail="currentTracking" :trackingindex="currentIndex" :currentcontent="currentContent" :codedetail="codedetail"></tracking-detail>
            </div>
        </div>
    </div>
</template>

<script>
//websocket namespace /tracking-plugin
let trackingIO = io("/tracking-plugin");

module.exports = {
  mounted: function() {
    // this.loadTrackingBase();
    this.loadTrackingList();
    loadTrackingList = this.loadTrackingList;
    trackingIO.on("update", function(msg) {
      loadTrackingList();
      console.log("update");
    });
  },
  data: function() {
    return {
      allTrackingData: [],
      showedTrackingData: [],
      currentIndex: null,
      currentTracking: null,
      targetContext: null,
      currentContent: {},
      codedetail: null
    };
  },
  methods: {
    getTrackingIndex: function(data, index) {
      this.currentTracking = data;
      this.currentIndex = index;
    },
    getCurrentContent: function(data) {
      this.currentContent = data;
      this.codedetail = data.content;
    },
    loadTrackingList: function() {
      this.$http.get("/ui/plugin/tracking/result").then(
        response => {
          this.allTrackingData = response.data.result;
        },
        error => {
          console.log("load tracking list failed!", error);
        }
      );
    },
    loadTrackingBase: function() {
      this.$http.get("/ui/plugin/tracking/init").then(response => {
        console.log("init msg successed");
        this.loadTrackingList();
      });
    }
  },
  components: {
    "tracking-list": httpVueLoader(
      "/ui/plugin/tracking/static/component/tracking-list.vue"
    ),
    "tracking-detail": httpVueLoader(
      "/ui/plugin/tracking/static/component/tracking-detail.vue"
    ),
    banner: httpVueLoader("/ui/plugin/tracking/static/component/banner.vue")
  }
};
</script>

<style>
</style>
