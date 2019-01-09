<template>
    <div v-if="allGroup.length!=0">
        <Tag v-for="item in grouplist" :key="item" :name="item" closable @on-close="handleClose">{{item}}</Tag>
        <i-button icon="ios-create-outline" type="dashed" size="small" @click="showModal=true"> Edit Tag </i-button>
        <modal v-model="showModal" title="Edit Tag" @on-ok="changeOk">
          <i-select multiple filterable style="width:260px,margin:auto" @on-change="activatedDataChange">
            <option-group label="Group">
              <i-option v-for="item in allGroup" :key="item" :value="item">{{item}}</i-option>
            </option-group>
          </i-select>
        </modal>
    </div>
</template>

<script>
module.exports = {
  props: [],
  mounted: function() {
    this.loadTagList();
  },
  data: function() {
    return {
      grouplist: [],
      showModal: false,
      allGroup: [],
      changeGroupCache: []
    };
  },
  methods: {
    loadTagList: function() {
      let filterdata = null;
      this.$http.get("/ui/plugin/tracking/base").then(
        response => {
          filterdata = response.data;
          for (let i = 0; i < filterdata.cases.length; i++) {
            let name = filterdata.cases[i].groupname;
            if (typeof name != "undefined") {
              // 如果grouplist里面不包含当前groupname返回-1，包含返回index值
              if (this.grouplist == 0 || this.grouplist.indexOf(name) == -1) {
                this.grouplist.push(name);
              }
            }
          }
          // 初始化，展示list赋值展示全部，赋值给AllGroup
          this.allGroup = [].concat(this.grouplist);
        },
        error => {
          console.log("load base failed!", error);
        }
      );
    },
    handleClose: function(event, name) {
      let index = this.grouplist.indexOf(name);
      if (index > -1) {
        this.grouplist.splice(index, 1);
      }
      this.$emit("filterchange", this.grouplist);
    },
    changeOk: function() {
      this.grouplist = this.changeGroupCache;
      this.$emit("filterchange", this.grouplist);
      this.$Notice.success({
        title: "Change Filter Success"
      });
    },
    activatedDataChange: function(val) {
      console.log("Selected Groups Change", val);
      this.changeGroupCache = val;
    }
  },
  watch: {}
};
</script>