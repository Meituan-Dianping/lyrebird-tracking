"""
应用上下文类

"""
class Context:
    def __init__(self):
        # config
        self.config = {}
        # result list : name and result for list show
        self.result_list = []
        # content : all data
        self.content = []
        # error messages list
        self.error_list = []


# 单例模式
app_context = Context()
