import json


class SparkApiException(Exception):
    pass


class UnauthroizedException(SparkApiException):
    pass


class TooManyRequests(SparkApiException):
    def __init__(self, retry_after):
        super(TooManyRequests, self).__init__(
            'Too many requests, please try again after {} seconds'
            .format(retry_after))
        self._retry_after = retry_after

    def retry_after(self):
        return self._retry_after


class ServerError(SparkApiException):
    def __init__(self, response_code, response):
        super(ServerError, self).__init__(
            '''Something went wrong on the server:
status code: {}
content: {}
'''.format(response_code, json.dumps(response)))


class NotFound(SparkApiException):
    def __init__(self, message, errors, tracking_id):
        super(NotFound, self).__init__(
            'Resource not found: {}'.format(message))


class InvalidRequest(SparkApiException):
    def __init__(self, response_code, message):
        super(InvalidRequest, self).__init__(
            'Resource not found: {}'.format(message))
