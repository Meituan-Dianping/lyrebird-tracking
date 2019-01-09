<template>
    <div>
        <Row class="button-bar">
          <banner></banner>
        </Row>
        <Row>
            <i-col span="12">
                <tracking-list :trackingdata="allTrackingData"  @detail="getTrackingIndex" @content="getCurrentContent" class="tracking-left"></tracking-list>
            </i-col>
            <i-col span="12" v-if="currentTracking">
                <tracking-detail :trackingdetail="currentTracking" :trackingindex="currentIndex" :currentcontent="currentContent" :codedetail="codedetail" class="tracking-right"></tracking-detail>
            </i-col>
        </Row>
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

<style scoped>
  .button-bar {
      margin-bottom: 5px;
      height: 48px;
    }

  .tracking-left {
    margin-right: 5px;
  }

  .tracking-right {
    margin-left: 5px;
  }
</style>
