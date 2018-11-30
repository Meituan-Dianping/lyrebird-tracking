import re


class SearchHandler:
    """
    搜索逻辑类
    主要用于判断数据源是否符合配置规则

    """

    def __init__(self, *args):
        self.data = []
        self.data += args
        self.search_list = []
        self.subnodes = []

    def find(self, jsonpath):
        """
        查询逻辑的入口函数，支持链式查询方式，如 SearchHandler(data).find(path1).find(path2)
        :param jsonpath: 用JSONPath描述的查询逻辑
        :return: SearchHandler对象，用于链式查询

        """
        self.subnodes = self.data
        self.search_list = self.transfer_query(jsonpath)
        for query in self.search_list:
            self._query_parser(query)
        return SearchHandler(*self.subnodes)

    def transfer_query(self, jsonpath):
        """
        解析jsonpath语法函数
        主要用正则进行拆分解析查询逻辑
        :param jsonpath: 用JSONPath描述的查询逻辑
        :return: 按查询顺序进行排列的查询语句数组

        """
        if '$' in jsonpath and not jsonpath.startswith('$'):
            return
        # split $ means root
        if jsonpath.startswith('$'):
            jsonpath = jsonpath[1:]
        # 以[...]为条件进行正则字符串切割
        pattern = re.compile(r'(\[.+?\])')
        source_list = re.split(pattern, jsonpath)
        query_list = []
        # 解析正则切割后的string list
        for item in source_list:
            # 如果是[...],直接append
            if item.startswith('['):
                query_list.append(item)
            # 如果是 property，以.切割成多个属性,extend到querylist里
            elif '.' in item:
                item_list = item.split('.')
                query_list.extend(item_list)
            else:
                query_list.append(item)
        # remove null item
        query_list = [x for x in query_list if x != '']
        return query_list

    def _query_parser(self, query_str):
        """
        根据正则匹配，识别list或property
        :param query_str: 查询字符串

        """
        # 匹配 [...]
        if re.match(r'(\[.+?\])', query_str):
            self._query_list(query_str)
        else:
            self._query_property(query_str)

    def _query_list(self, query_str):
        """
        根据正则匹配，识别三种类型的list模式
        :param query_str: 查询字符串

        """
        node_list = self.subnodes
        self.subnodes = []
        for obj in node_list:
            if not isinstance(obj, list):
                continue
            # match such as:[2]
            if re.match(r'(\[\d+?\])', query_str):
                self._query_list_by_index(obj, query_str)
            # match such as:[*]
            elif query_str == '[*]':
                self._query_list_no_index(obj, query_str)
            # match such as: [?key=val]
            elif re.match(r'(\[\?.+?\=.+?\])', query_str):
                self._query_list_kw(obj, query_str)

    def _query_list_by_index(self, node, query_str):
        # 从[333]取出index 333
        index_num = query_str.split('[')[1].split(']')[0]
        if len(node) - 1 >= int(index_num):
            self.subnodes.append(node[int(index_num)])

    def _query_list_no_index(self, node, query_str):
        # 将整个list extend 至 subnodes里
        self.subnodes.extend(node)

    def _query_list_kw(self, node, query_str):
        # handle such as :[?key1=val1&key2=val2&key3=val3]
        sword = query_str.split('?')[1].split(']')[0]
        q_list = sword.split('&')

        for item in node:
            if not isinstance(item, dict):
                continue
            
            flag = 1
            for q in q_list:
                key = q.split('=')[0]
                val = q.split('=')[1].strip("'")
                # handle value of int type
                if val.isnumeric():
                    val = int(val)
                if item.get(key) != val:
                    flag = 0
                    break
                continue
            if flag == 1:
                self.subnodes.append(item)

    def _query_property(self, query_str):
        """
        处理property模式，默认返回对应property的val
        :param query_str: 查询字符串

        """
        node_list = self.subnodes
        self.subnodes = []
        for obj in node_list:
            if not isinstance(obj, dict):
                continue
            if query_str not in obj:
                continue
            self.subnodes.append(obj[query_str])
