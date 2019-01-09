Vue.component(
    'filter-tag', {
        template: '#filter-tag',
        props: [],
        data: function() {
            return {
                grouplist: [],
                showModal: false,
                changeGroupCache: [],
                allGroup: []
            }
        },
        mounted: function() {
            this.tagData();
        },
        methods: {
            tagData: function() {
                let filterdata = null;
                filterdata = baseData;
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
        }

    }
)