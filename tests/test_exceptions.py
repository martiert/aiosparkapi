import aiosparkapi.exceptions as exceptions


def test_spark_api_exception():
    exception = exceptions.SparkApiException(
        402,
        {'foo': 'bar'},
        'Some message')

    assert isinstance(exception, Exception)
    assert exception.response_code == 402
    assert exception.response == {'foo': 'bar'}


def test_unauthorized():
    exception = exceptions.Unauthorized()

    assert isinstance(exception, exceptions.SparkApiException)
    assert exception.response_code == 401


def test_too_many_requests():
    exception = exceptions.TooManyRequests(32151)

    assert isinstance(exception, exceptions.SparkApiException)
    assert exception.retry_after == 32151
    assert exception.response_code == 503


def test_server_error():
    response = {
        'message': 'Server is overloaded',
    }
    exception = exceptions.ServerError(503, response)

    assert isinstance(exception, exceptions.SparkApiException)
    assert exception.response_code == 503
    assert exception.response == response


def test_not_found():
    response = {
        'message': 'Not found',
    }

    exception = exceptions.NotFound(response)
    assert isinstance(exception, exceptions.SparkApiException)
    assert exception.response_code == 404
    assert exception.response == response


def test_invalid_request():
    response = {
        'message': 'Invalid request',
    }

    exception = exceptions.InvalidRequest(403, response)
    assert isinstance(exception, exceptions.SparkApiException)
    assert exception.response_code == 403
    assert exception.response == response
