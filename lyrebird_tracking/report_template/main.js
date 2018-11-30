var caseInfo = new Vue({
    el: '#caseInfo',
    data: {
        columns1: [{
            title: 'Case',
            key: 'name',
            className: 'i-table-caseName',
            sortable: true
        }, {
            title: 'Result',
            width: 100,
            key: 'result',
            className: 'i-table-caseName',
            sortable: true,
            render: (h, params) => {
                if (params.row.result === "pass") {
                    return h(
                        "i-button", {
                            props: { size: "small", type: "success" },
                            style: { width: "50px" }
                        },
                        "Pass"
                    );
                } else if (params.row.result === "fail") {
                    return h(
                        "i-button", {
                            props: { size: "small", type: "error" },
                            style: { width: "50px" }
                        },
                        "Fail"
                    );
                } else {
                    return h(
                        "i-button", {
                            props: { size: "small", type: "default" },
                            style: { width: "50px" }
                        },
                        "N/A"
                    );
                }
            }
        }],
        caseInfo: reportCaseData.result,
        filter_rules: [],
        currentTracking: null,
        currentData: null,
        codedetail: null
    },
    methods: {
        filterList: function(grouplist) {
            this.filter_rules = grouplist;
        },
        handleRowSelect: function(row, index) {
            this.currentTracking = index;
            for (let i = 0; i < detailCollection.length; i++) {
                let id = detailCollection[i].id
                if (row.id == id) {
                    this.currentData = detailCollection[i];
                    this.codedetail = detailCollection[i].content;
                    console.log(id);
                    console.log(this.codedetail);
                    console.log(this.currentData);
                }
            }
        }
    },
    computed: {
        displayedData: function() {
            // filter出name
            let showdata = [];
            if (this.filter_rules.length == 0) {
                showdata = this.caseInfo;
            } else {
                for (let i = 0; i < this.filter_rules.length; i++) {
                    let filter_rule = this.filter_rules[i];
                    let filtercells = this.caseInfo.filter(function(elem) {
                        return elem.groupname == filter_rule;
                    });
                    showdata = showdata.concat(filtercells);
                }
            }
            return showdata;
        }
    }
})