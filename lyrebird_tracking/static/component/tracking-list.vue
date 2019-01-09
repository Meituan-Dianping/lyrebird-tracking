<template>
    <Card>
       <div class="tracking-list">
            <filter-tag @filterchange="filterList"></filter-tag>
            <br/>
            <!-- <div style="max-height: 550px; overflow-y: auto;"> -->
              <i-table highlight-row  :columns="columns" :data="displayedData" @on-row-click="handleRowSelect" class="data-table"></i-table>
            <!-- </div> -->
        </div>
    </Card>
</template>

<script>
module.exports = {
  props: ["trackingdata"],
  mounted: function() {},
  data: function() {
    return {
      filter_rules: [],
      selectDetail: {},
      columns: [
        {
          title: "Case",
          key: "name",
          sortable: true
        },
        {
          title: "Result",
          key: "result",
          width: 100,
          sortable: true,
          render: (h, params) => {
            if (params.row.result === "pass") {
              return h(
                "i-button",
                {
                  props: { size: "small", type: "success" },
                  style: { width: "50px" }
                },
                "Pass"
              );
            } else if (params.row.result === "fail") {
              return h(
                "i-button",
                {
                  props: { size: "small", type: "error" },
                  style: { width: "50px" }
                },
                "Fail"
              );
            } else {
              return h(
                "i-button",
                {
                  props: { size: "small", type: "default"},
                  style: { width: "50px" }
                },
                "N/A"
              );
            }
          }
        }
      ]
    };
  },
  methods: {
    setTrackingName: function(selectedItem) {
      this.selectedRow = selectedItem;
      this.$emit("popdata", selectedItem);
    },
    setResult: function(item) {
      if (item.result.toLowerCase() === "pass") {
        item.result = "FAIL";
      } else if (item.result.toLowerCase() === "fail") {
        item.result = "PASS";
      } else {
        item.result = "null";
      }
    },
    setResultClass: function(item) {
      if (item.result.toLowerCase() === "pass") {
        return "btn-success";
      } else if (item.result.toLowerCase() === "fail") {
        return "btn-danger";
      } else {
        item.result = "null";
        return "btn-default";
      }
    },
    classSelected: function(item) {
      return item === this.selectedRow;
    },
    handleRowSelect: function(row, index) {
      this.$emit("detail", row, index);
      this.viewDetail(row.id);
      this.$emit("content", this.selectDetail);
    },
    viewDetail: function(id) {
      this.$http.get("/ui/plugin/tracking/content/" + id).then(
        response => {
          this.selectDetail = response.data;
          this.$emit("content", this.selectDetail);
        },
        error => {
          console.log("load tracking list failed!", error);
        }
      );
    },
    filterList: function(grouplist) {
      this.filter_rules = grouplist;
    }
  },
  components: {
    "filter-tag": httpVueLoader(
      "/ui/plugin/tracking/static/component/filter-tag.vue"
    )
  },
  computed: {
    displayedData: function() {
      // filter出name
      let showdata = [];
      if (this.filter_rules.length == 0) {
        showdata = this.trackingdata;
      } else {
        for (let i = 0; i < this.filter_rules.length; i++) {
          let filter_rule = this.filter_rules[i];
          let filtercells = this.trackingdata.filter(function(elem) {
            return elem.groupname == filter_rule;
          });
          showdata = showdata.concat(filtercells);
        }
      }
      return showdata;
    }
  }
};
</script>

<style>
.data-table th div{
padding-left: 5px;
padding-right: 5px;
}
.data-table td div{
padding-left: 5px;
padding-right: 5px;
}
.tracking-list {
  height: calc(100vh - 80px);
  overflow-y: auto;
}

</style>
