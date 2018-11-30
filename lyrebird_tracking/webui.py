import json
import lyrebird
import os
import codecs
from flask import request, jsonify, Response, abort
from lyrebird import context
from lyrebird_tracking.server import tracking_init
from lyrebird_tracking.context import app_context
import shutil


class Tracking(lyrebird.PluginView):
    """
    tracking插件视图

    """
    def index(self):
        """
        插件首页
        """
        return self.render_template('index.html')

    def get_result(self):
        """
        获取case列表API
        :return: case列表数据
        """
        return jsonify({'result': app_context.result_list})

    def get_content(self, id=''):
        """
        获取校验详情API
        :param id: 对应uuid，每个case的唯一标识，根据id查询校验详情
        :return: 对应id的校验详情
        """
        for item in app_context.content:
            if item['id'] == id:
                return jsonify(item)
        return abort(400, 'Request not found')
    
    def save_report(self):
        """
        保存测试报告API
        """
        report_data_path = os.path.join(os.path.dirname(__file__), 'report_template/data/report-data.js')
        with codecs.open(report_data_path, 'w+', 'utf-8') as f:
            f.write('var reportCaseData='+json.dumps({'result': app_context.result_list}, ensure_ascii = False))
            f.write('\n')
            f.write('var baseData='+json.dumps(app_context.config, ensure_ascii = False))
            f.write('\n')
            f.write('var detailCollection='+json.dumps(app_context.content, ensure_ascii = False))
            f.write('\n')
        report_path = os.path.join(os.path.dirname(__file__), 'report_template')
        target_path = os.path.abspath(os.path.join(lyrebird.get_plugin_storage(), 'report'))
        if os.path.exists(target_path):
            shutil.rmtree(target_path)
        shutil.copytree(report_path, target_path)

        return context.make_ok_response()

    def clear_result(self):
        """
        清空测试缓存API
        需要进行初始化，并且发送socketio消息给前端重新load页面
        """
        app_context.result_list = []
        app_context.content = []
        tracking_init()
        context.application.socket_io.emit('update', namespace='/tracking-plugin')
        return context.make_ok_response()

    def get_base_info(self):
        """
        获取基准文件信息API
        主要用于分组筛选
        :return: 基准文件原始数据
        """
        return jsonify(app_context.config)

    def on_create(self):
        """
        插件初始化函数
        """
        # tracking 初始化
        tracking_init()
        # 设置模板文件目录（可选，设置静态文件目录）
        self.set_template_root('lyrebird_tracking')
        self.add_url_rule('/', view_func=self.index)
        self.add_url_rule('/result', view_func=self.get_result)
        self.add_url_rule('/content/<string:id>', view_func=self.get_content)
        self.add_url_rule('/report', view_func=self.save_report)
        self.add_url_rule('/clear', view_func=self.clear_result)
        self.add_url_rule('/base', view_func=self.get_base_info)

    def get_icon(self):
        """
        设置展示在边栏的图标
        :return: 返回图标样式
        """
        return 'fa fa-fw fa-line-chart'

    def default_conf(self):
        """
        设置默认的 conf.json
        :return: 返回 conf.json 内容
        """
        # 读取插件 conf.json 返回
        conf_path = os.path.dirname(__file__) + '/conf.json'
        with codecs.open(conf_path, 'r', 'utf-8') as f:
            return json.load(f)
