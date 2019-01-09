<template>
     <Card>
       <div class="tracking-detail">
          <font style="font-size: 16px; font-weight: bold; color: rgb(70, 76, 91);">Detail</font>
          <br/>
          <br/>
          <el-collapse v-model="activeNames">
              <el-collapse-item v-for="item in currentcontent.asserts" :key="item.field">
                  <template slot="title" v-if="item.flag===true">
                    <i class="header-icon el-icon-circle-check-outline"></i>
                    <font color="LimeGreen">Check field - {{item.field}} </font>
                  </template>
                  <!-- 没有预期值或未测试的埋点信息，展示问号样式 -->
                  <template slot="title" v-else-if="item.flag===2||typeof(item.flag) == 'undefined'">
                    <i class="header-icon el-icon-question"></i>
                    <font color="CornflowerBlue">Check field - {{item.field}} </font>
                  </template>
                  <template slot="title" v-else>
                    <i class="header-icon el-icon-circle-close-outline"></i>
                    <font color="red">Check field - {{item.field}} </font>
                  </template>
                  <div>
                      <!-- 没有期望值-展示文案提示 -->
                      <li>Field : {{item.field}}</li>
                      <li v-if="JSON.stringify(item.schema)=='{}'">Expect schema : 
                        No expected value
                      </li>
                      <!-- 未测试过场景-展示NA -->
                      <!-- <li v-else-if="item.schema">Expect schema : 
                        <div v-html="jsoninfo(item.schema)"></div>
                      </li> -->
                      <!-- 测试过场景-取expect参数 -->
                      <li v-else>Expect schema :
                        <div v-html="jsoninfo(item.schema)"></div>
                      </li>
                      <li>Actual value : 
                        <div v-if="item.actual" v-html="jsoninfo(item.actual)"></div>
                        <!-- 未测试过场景-实际值不存在展示NA -->
                        <div v-else v-html="jsoninfo('N/A')"></div>
                      </li>
                  </div>
              </el-collapse-item>
          </el-collapse>
          <div id="container" style="height:500px;border:1px solid grey"></div>
       </div>
    </Card>
</template>

<script>
module.exports = {
  props: ["trackingdetail", "trackingindex", "currentcontent", "codedetail"],
  computed: {
    infoContaint: function() {
      infoStr = JSON.stringify(this.currentcontent.content, null, 4);
      return '<pre><code class="language-json">' + infoStr + "</code></pre>";
    }
  },
  updated: function() {
    Prism.highlightAll();
  },
  mounted: function() {
    Prism.highlightAll();
    //create monaco editor
    editorContainer = this.$el.querySelector("#container");
    option = {
      value: JSON.stringify(this.codedetail, null, 4),
      language: "json",
      theme: "vs",
      glyphMargin: true,
      readOnly: true
    };
    this.editor = window.monaco.editor.create(editorContainer, option);
    //hover register
    showhint = this.showhint
    monaco.languages.register({ id: 'json' });
    monaco.languages.registerHoverProvider('json', {
      provideHover: function(model,position) {
        return showhint(model,position)
      }
    });
  },
  data: function() {
    return {
      editor: null,
      activeNames: ["1"],
      match_array:[]
    };
  },
  methods: {
    jsoninfo: function(content) {
      infoStr = JSON.stringify(content, null, 4);
      return '<pre><code class="language-json">' + infoStr + "</code></pre>";
    },
    showhint: function(model,position){
        let line = position.lineNumber;
        let field = null;
        let hint = null;
        console.log(this.match_array);
        for(var i=0;i<this.match_array.length;i++){
          if(this.match_array[i].linenumber===line){
            field = this.match_array[i].linenumber;
            hint = JSON.stringify(this.match_array[i].hint);
            break;
          }
        }
        if(field){
          return{
            range: new monaco.Range(1,1,line,model.getLineMaxColumn(1)),
            contents: [ {value: '**Schema check**'},{value: hint}]
          }
        }else{
          return{
            range: new monaco.Range(0,0,0,0),
            contents: []
          }
        }
      }
  },
  components: {},
  watch: {
    codedetail: function() {
      //每次切换后，都需要清空保存hint提示的array
      this.match_array = []
      console.log("Code editor: content change");
      this.editor.setValue(JSON.stringify(this.codedetail, null, 4));
      this.editor.trigger(this.editor.getValue(),"editor.action.formatDocument");

      //如果没有数据展示，不需要做后续的显示处理
      if(this.codedetail == null){
        console.log('haha');
        return null
      }

      for (let i = 0; i < this.currentcontent.asserts.length; i++) {
        let matches = this.editor.getModel().findMatches('"' + this.currentcontent.asserts[i].field + '":',false,true,false,false);
        let match_start_linenumber = matches[0].range.startLineNumber;
        console.log(matches);
        
        //如果含错误提示，才放入hint提示列表中
        if(this.currentcontent.asserts[i].flag===false){
          let match_obj = {
            fieldname:this.currentcontent.asserts[i].field,
            linenumber:match_start_linenumber,
            hint:this.currentcontent.asserts[i].hint
          }
          this.match_array.push(match_obj);
          }
        
        let fieldname = this.currentcontent.asserts[i].field;
        let fvalue = this.codedetail[fieldname];
        let fstr = JSON.stringify(fvalue, null, 4);
        //获取块大小，涂色用，根据换行符的个数
        let detail_length = fstr.split('\n').length;


        //如果断言的字段有问题，就高亮出来
        if (this.currentcontent.asserts[i].flag === false) {
          this.editor.deltaDecorations([],
            [
              {
                range: new monaco.Range(match_start_linenumber,1,match_start_linenumber+detail_length-1,1),
                options: { isWholeLine: true,className: "myContentClass"}
              }
            ]
          );
        }
        // 无断言预期，高亮展示蓝色
        else if(this.currentcontent.asserts[i].flag === 2){
          this.editor.deltaDecorations([],
            [
              {
                range: new monaco.Range(match_start_linenumber,1,match_start_linenumber+detail_length-1,1),
                options: { isWholeLine: true,className: "infoContentClass"}
              }
            ]
          );
        }
        
      }
    }
  }
};
</script>

<style>
.myContentClass {
  background: lightpink;
}
.infoContentClass {
	background: lightblue;
}
.tracking-detail {
  height: calc(100vh - 80px);
  overflow-y: auto;
}
</style>
