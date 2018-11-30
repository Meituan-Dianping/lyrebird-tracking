from .base_handler import load_base, init_data
from .search_handler import SearchHandler
from .data_manager import new_caseresult
from .validator import Verify
from lyrebird_tracking.context import app_context
from lyrebird import context
import lyrebird


def tracking_init():
    """
    tracking初始化函数
    1. 加载基准文件
    2. 对基准文件进行初始化

    """
    load_base()
    init_data()


def search(jsonnode, jsonpath):
    """
    查询函数
    :param jsonnode: 待搜索的json数据源
    :param jsonpath: 搜索条件
    :return: 满足查询搜索条件的结果数组

    """
    node = SearchHandler(jsonnode)
    targets_list = node.find(jsonpath).data
    return targets_list


def validate(rule, targets_list):
    """
    验证函数
    :param rule: 校验规则
    :param targets_list: 目标查询的数组

    校验失败会发消息总线

    """
    verify = Verify()
    result_list = verify.check(targets_list, rule)
    for item in result_list:
        # handle data change
        new_caseresult(item)
        # emit socket io to FE
        context.application.socket_io.emit('update', namespace='/tracking-plugin')
        if item.get('result') == 'fail':
            error_message = dict((k, item[k]) for k in (
                'name', 'result', 'selector', 'asserts', 'content') if k in item)
            # 有埋点错误消息，发事件给消息总线
            pubilsh_error_msg(error_message)


def pubilsh_error_msg(msg):
    """
    将错误信息通过消息总线发送出去，订阅tracking频道的其他插件会监听到
    :param msg: 错误信息详情
    
    """
    
    app_context.error_list.append(msg)
    lyrebird.publish('tracking.error', msg)
    lyrebird.publish('tracking.error', msg, state=True)
    lyrebird.publish('tracking.error_list', app_context.error_list)
    lyrebird.publish('tracking.error_list', app_context.error_list, state=True)
