class BaseResponse(object):

    def __init__(self):
        self.code = 1000
        self.data = None
        self.error = None

    @property
    def dict(self):
        return self.__dict__

ret = BaseResponse()
ret.code = 1999


print(ret.dict )
