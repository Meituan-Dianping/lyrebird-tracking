import jsonschema
from jsonschema import Draft4Validator
import uuid
from lyrebird_tracking.server.search_handler import SearchHandler


class Verify:
    """
    校验类
    根据配置文件的校验规则进行校验

    """

    def check(self, elements_list, rule):
        """
        校验函数
        基于JSONSchea根据校验规则和输入的数据源进行校验，返回的数据会更新应用上下文，校验结果随之会更新在前端
        :param elements_list: list类型，待校验的数据列表
        :param rule: 校验规则

        """
        result_list = []
        checker = rule.get('asserts')
        for ele in elements_list:
            flag = True
            check_list = []
            for item in checker:
                field = item.get('field')
                schema = item.get('schema')

                # 判断实际有没有对应的字段
                search_list = [field]
                node = SearchHandler(ele)
                for i in range(len(search_list)):
                    node = node.find(search_list[i])
                result = node.data
                if result:
                    content = result[0]
                else:
                    content = None

                # 错误提示标记hint
                hint = None
                # 如果schema为空，高亮，不校验，用特殊高亮区别标记出来
                if schema:
                    result = Draft4Validator(schema).is_valid(content)
                    try:
                        jsonschema.validate(content, schema)
                    except jsonschema.ValidationError as e:
                        hint = e.message
                else:
                    result = 2

                flag = flag * result

                if content:
                    check_list.append(
                        {'field': field, 'schema': schema, 'actual': content, 'flag': result, 'hint': hint})
                else:
                    check_list.append({'field': field, 'schema': schema, 'actual': 'error!exists-false',
                                    'flag': result, 'hint': 'The field is not exists!'})

            result_dict = dict((k, rule[k]) for k in ('name', 'groupid', 'groupname', 'selector') if k in rule)
            result_dict['asserts'] = check_list
            result_dict['id'] = str(uuid.uuid4())
            result_dict['content'] = ele
            if flag:
                result_dict['result'] = 'pass'
            else:
                result_dict['result'] = 'fail'

            result_list.append(result_dict)

        return result_list
