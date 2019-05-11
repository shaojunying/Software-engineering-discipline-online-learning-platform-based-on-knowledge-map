import json

from ExceptionMsg import ExceptionMsg


class ResponseData:
    def __init__(self, exceptionMsg=ExceptionMsg.SUCCESS, data=None):
        self.code = exceptionMsg.get_code()
        self.message = exceptionMsg.get_message()
        self.data = data

    def encode(self):
        return json.dumps(self, cls=ResponseDataEncoder, ensure_ascii=False)


class ResponseDataEncoder(json.JSONEncoder):
    """
    ResponseData的编码类
    """

    def default(self, obj):
        if isinstance(obj, ResponseData):
            result = {
                "code": obj.code,
                "message": obj.message,
                "data": obj.data}
            if result['data'] is None:
                result.pop('data')
            return result
        return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':
    responseData = ResponseData(
        # data={"key": "value"}
    )
    print(responseData.encode())
    # print(json.loads(test))
