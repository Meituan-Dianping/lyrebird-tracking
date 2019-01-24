<template>
    <div v-if="allGroup.length!=0">
        <!-- <Tag v-for="item in grouplist" :key="item" :name="item" closable @on-close="handleClose">{{item}}</Tag> -->
        <Tag >Case filters : {{grouplist.length}} conditions </Tag>
        <i-button icon="ios-create-outline" type="dashed" size="small" @click="editTag"> Edit </i-button>
        <modal v-model="showModal" title="Edit Tag" @on-ok="changeOk" height="auto" :mask="false" width="70vh">
          <i-select filterable class="custom-select" v-model="changeGroupCache" multiple style="width:260px,margin:auto;" @on-change="activatedDataChange">
            <option-group label="Group">
              <i-option v-for="item in allGroup" :key="item" :value="item">{{item}}</i-option>
            </option-group>
          </i-select>
          <div slot="footer">
            <i-button @click="clearFilter" style="margin:auto" class="pull-left">Clear All</i-button>
            <i-button type="text" @click="cancelmodel"> Cancel </i-button>
            <i-button type="primary"  @click="changeOk"> OK </i-button>
        </div>
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
          let group = [];
          for (let i = 0; i < filterdata.cases.length; i++) {
            let name = filterdata.cases[i].groupname;
            if (typeof name != "undefined") {
              // 如果grouplist里面不包含当前groupname返回-1，包含返回index值
              if (group == 0 || group.indexOf(name) == -1) {
                group.push(name);
              }
            }
          }
          // 初始化，展示list赋值展示全部，赋值给AllGroup
          this.allGroup = group;
        },
        error => {
          console.log("load base failed!", error);
        }
      );
      this.$http.get("/ui/plugin/tracking/group").then(
        response => {
          filterdata = response.data;
          this.grouplist = filterdata;
          this.changeGroupCache = filterdata;
          this.$emit("filterchange", this.grouplist);
        },
        error => {
          console.log("load filter group failed!", error);
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
      this.$http.post('/ui/plugin/tracking/select',
        {
          group: this.grouplist
        }
      ).then(resp=>{
          if(resp.data.code===1000){
            console.log('change selected group ok');
          }else{
            console.log('change selected group failed');
          }
        }
      )
      this.showModal = false;
    },
    activatedDataChange: function(val) {
      console.log("Selected Groups Change", val);
      this.changeGroupCache = val;
    },
    clearFilter: function(){
      this.changeGroupCache = []
    },
    cancelmodel: function(){
      this.showModal = false;
    },
    editTag: function(){
      this.showModal = true;
      this.changeGroupCache = this.grouplist;
    }
  },
  watch: {}
};
</script>
<style>
  .custom-select > .ivu-select-selection {
      max-height: 180px;
      overflow-y: scroll;
  }
</style>
