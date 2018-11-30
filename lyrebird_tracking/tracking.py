import gzip
import json
import time

import lyrebird
from lyrebird import HandlerContext, context
from urllib.parse import urlparse

from lyrebird_tracking.context import app_context
from lyrebird_tracking.server import search, validate


class TrackingHandler:
    """
    处理Lyrebird数据流
    Trakcing校验数据来源，来自于Lyrebird的请求上下文
    """
    def handle(self, handler_context: HandlerContext):
        """
        数据流处理函数，继承与Lyrebird的HandlerContext，会获取Lyrebird的请求上下文
        :param handler_context: 请求上下文，取request data进行筛选校验
        """
        url = handler_context.get_origin_url()
        if url:
            hostname = urlparse(url).hostname
        else:
            hostname = urlparse(handler_context.request.url).hostname

        # 获取配置文件的目标host列表，取自于config中的target
        if hostname in app_context.config.get('target'):
            # 判断是否为gzip类型，若是进行解压缩处理
            if 'Content-Encoding' in handler_context.request.headers and handler_context.request.headers.get(
                    'Content-Encoding') == 'gzip':
                reqs_data = json.loads(gzip.decompress(handler_context.request.data).decode())
            else:
                reqs_data = []
            # 取出配置文件的cases内容，进行查询和校验
            rule_list = app_context.config.get('cases')
            for rule in rule_list:
                # 根据配置文件的selector选择器配置，进行查询
                targets_list = search(reqs_data, rule.get('selector'))
                # 如果有匹配的结果，进行进一步的校验
                if targets_list:
                    validate(rule, targets_list)
