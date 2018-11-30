from lyrebird_tracking.context import app_context


def new_caseresult(result_content):
    """
    新增case内容，处理断言结果的原始内容，对应用上下文进行更新
    :param result_content: 断言结果的原始内容

    """
    # 筛选出带目标key的子字典
    show_cell = dict((k, result_content[k])
                     for k in ('result', 'id', 'name', 'groupid', 'groupname') if k in result_content)
    # 筛选出未测试的case，标记为NA，name为唯一标识进行筛选
    untested_list = list(filter(lambda x: x.get('result') == 'NA' and x.get(
        'name') == result_content.get('name'), app_context.content))
    # 如果对应未测试的case存在
    if untested_list:
        untested_item = untested_list[0]
        untested_list_item = list(filter(lambda x: x.get('result') == 'NA' and x.get(
            'name') == result_content.get('name'), app_context.result_list))[0]
        # 删除对应未测试case
        app_context.content.remove(untested_item)
        app_context.result_list.remove(untested_list_item)
    # 增加对应测试case，在列表展示数据内插入到列表index=0的位置
    app_context.result_list.insert(0, show_cell)
    app_context.content.append(result_content)
