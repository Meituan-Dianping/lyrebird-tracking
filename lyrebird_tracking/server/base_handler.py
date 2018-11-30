import lyrebird
import os
import json
import codecs
from lyrebird_tracking.context import app_context
from lyrebird.log import get_logger
import uuid
storage = lyrebird.get_plugin_storage()
BASE_FILE = os.path.abspath(os.path.join(storage, 'base.json'))
DEFAULT_BASE_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', './data/base.json'))


def load_base():
    """
    加载基准文件（Base文件）
    读取文件路径：~/.lyrbeird/plugin/lyrebird_tracking/base.json
    没有该文件，会加载为默认配置 DEFAULT_BASE_FILE

    """
    lyrebird_conf = lyrebird.context.application.conf
    # 读取指定base文件，写入到base.json
    if lyrebird_conf.get('tracking.base'):
        base_path = lyrebird_conf.get('tracking.base')
        base = codecs.open(base_path, 'r', 'utf-8').read()
        f = codecs.open(BASE_FILE, 'w', 'utf-8')
        f.write(base)
        f.close()

     # 通过本地默认base文件获取base
    elif not os.path.exists(BASE_FILE):
        copy_file(BASE_FILE)

    with codecs.open(BASE_FILE, 'r', 'utf-8') as f:
        conf_data = json.load(f)

    # base文件内容放置到conf_data中
    app_context.config = conf_data


def init_data():
    """
    初始化基准文件
    初始化解析为应用上下文的变量：
    app_context.result_list - case列表数据
    app_context.content - 校验结果详情数据

    """
    for item in app_context.config.get('cases'):
        result_dict = {
            'id': str(uuid.uuid4()),
            'result': 'NA', 'name': item.get('name')}
        # 加入分组信息，用于前端筛选
        if item.get('groupid'):
            result_dict.update({'groupid': item.get('groupid')})
        if item.get('groupname'):
            result_dict.update({'groupname': item.get('groupname')})

        target_dict = {
            'asserts': item.get('asserts'),
            'content': None, 'selector': item.get('selector'),
            'source': None, 'url': None}
        target_dict.update(result_dict)

        app_context.result_list.append(result_dict)
        app_context.content.append(target_dict)


def copy_file(target_path):
    """
    复制文件内容，复制默认基准文件到 ~/.lyrbeird/plugin/lyrebird_tracking/base.json
    :param target_path: 目标路径

    """
    f_from = codecs.open(DEFAULT_BASE_FILE, 'r', 'utf-8')
    f_to = codecs.open(target_path, 'w', 'utf-8')
    f_to.write(f_from.read())
    f_to.close()
    f_from.close()
