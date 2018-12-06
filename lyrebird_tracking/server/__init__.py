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
            error_message = dict((k, item[k]) for k in ('name', 'content') if k in item)
            error_message['error_msg'] = filter_error_msg(item)
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


def filter_error_msg(result_dict):
    """
    从测试结果中筛选出错误信息，转化为字符串
    :param result_dict: dict类型，待处理的结果信息
    :return error_str: str类型，最终的错误信息字符串

    """
    # 筛选错误信息
    error_msg = dict((k, result_dict[k]) for k in ('groupname', 'name') if k in result_dict)
    error_list = []
    for item in result_dict.get('asserts'):
        if item.get('flag') is False:
            error_detail = {'field': item.get('field'), 'error detail': item.get('hint')}
            error_list.append(error_detail)
    error_msg['error message'] = error_list

    # 转换为字符串
    error_str = ''
    for key in error_msg.keys():
        if key == 'error message':
            temp_str = key + ':\n'
            for item in error_msg.get(key):
                temp_str = temp_str + 'field: ' + item.get('field') + '\n' \
                           + 'error detail: ' + item.get('error detail') + '\n'
        else:
            temp_str = key + ': ' + str(error_msg.get(key)) + '\n'
        error_str = error_str + temp_str

    return error_str
