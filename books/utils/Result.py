class Result:
    def __init__(self, code="0", msg="成功", data=None):
        self.code = code
        self.msg = msg
        self.data = data

    @staticmethod
    def success(data=None):
        """
        返回成功的结果
        """
        return Result(code="0", msg="成功", data=data)

    @staticmethod
    def error(code, msg):
        """
        返回失败的结果
        """
        return Result(code=code, msg=msg, data=None)

    def to_dict(self):
        """
        将Result对象转换为字典，以便序列化为JSON
        """
        return {
            "code": self.code,
            "msg": self.msg,
            "data": self.data
        }