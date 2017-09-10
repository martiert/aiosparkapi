import json


class SparkApiException(Exception):
    def __init__(self, response_code, response, message):
        super(SparkApiException, self).__init__(message)

        self.response_code = response_code
        self.response = response


class Unauthorized(SparkApiException):
    def __init__(self):
        super(Unauthorized, self).__init__(
            401,
            {},
            'Request not authorized')


class TooManyRequests(SparkApiException):
    def __init__(self, retry_after):
        super(TooManyRequests, self).__init__(
            503,
            {},
            'Too many requests, please try again after {} seconds'
            .format(retry_after))
        self.retry_after = retry_after


class ServerError(SparkApiException):
    def __init__(self, response_code, response):
        super(ServerError, self).__init__(
            response_code,
            response,
            '''Something went wrong on the server:
status code: {}
content: {}
'''.format(response_code, json.dumps(response)))


class NotFound(SparkApiException):
    def __init__(self, response):
        super(NotFound, self).__init__(
            404,
            response,
            'Resource not found: {}'.format(response))


class InvalidRequest(SparkApiException):
    def __init__(self, response_code, message):
        super(InvalidRequest, self).__init__(
            response_code,
            message,
            'Resource not found: {}'.format(message))
