import json


class BaseResponse:

    def __init__(self, result):
        self._result = result

    def __getattr__(self, item):
        if item in self._result.keys():
            return self._result[item]
        error = "'{}' object has no attribute '{}'".format(
                self.__class__.__name__, item)
        raise AttributeError(error)

    def __eq__(self, other):
        return self._result == other

    def __str__(self):
        return json.dumps(self._result, indent=2)
