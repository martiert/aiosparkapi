import json
import pytest
from aiohttp import web

import aiosparkapi.requests as requests
import aiosparkapi.exceptions as exceptions


def get_headers(request):
    headers = {}
    if request.headers.get('Authorization'):
        headers['Authorization'] = request.headers['Authorization']
    if request.headers.get('content-type'):
        headers['content-type'] = request.headers['content-type']

    return headers


class TestServer:

    def setup(self):
        self.reset()
        self.status_code = 200
        self.response = {}
        self._authorized = True
        self._retry_after = None

    def reset(self):
        self.last_parameters = None
        self.last_headers = None
        self.last_id = None
        self.last_body = None

    def unauthorized(self):
        self._authorized = False

    def retry_after(self, timeout):
        self._retry_after = timeout

    async def get_rooms(self, request):
        if not self._authorized:
            return web.Response(status=401)
        if self._retry_after:
            return web.Response(
                status=429,
                headers={'retry-after': str(self._retry_after)})

        self.reset()
        self.last_parameters = request.query
        self.last_headers = get_headers(request)

        return web.Response(
                body=json.dumps(self.response).encode(),
                headers={'content-type': 'application/json'},
                status=self.status_code)

    async def get_messages(self, request):
        if not self._authorized:
            return web.Response(status=401)

        self.reset()
        self.last_id = request.match_info['id']
        self.last_headers = get_headers(request)

        return web.Response(
                body=json.dumps(self.response).encode(),
                headers={'content-type': 'application/json'},
                status=self.status_code)

    async def create_messages(self, request):
        if not self._authorized:
            return web.Response(status=401)

        self.reset()
        self.last_body = await request.json()
        self.last_headers = get_headers(request)

        return web.Response(
                body=json.dumps(self.response).encode(),
                headers={'content-type': 'application/json'},
                status=self.status_code)

    async def update_messages(self, request):
        if not self._authorized:
            return web.Response(status=401)

        self.reset()
        self.last_id = request.match_info['id']
        self.last_body = await request.json()
        self.last_headers = get_headers(request)

        return web.Response(
                body=json.dumps(self.response).encode(),
                headers={'content-type': 'application/json'},
                status=self.status_code)

    async def delete_messages(self, request):
        if not self._authorized:
            return web.Response(status=401)

        self.reset()
        self.last_id = request.match_info['id']
        self.last_headers = get_headers(request)

        return web.Response(status=self.status_code)

    def create_app(self, loop):
        app = web.Application(loop=loop)
        app.router.add_route('GET', '/rooms', self.get_rooms)
        app.router.add_route('GET', '/messages/{id}', self.get_messages)
        app.router.add_route('POST', '/messages', self.create_messages)
        app.router.add_route('PUT', '/messages/{id}', self.update_messages)
        app.router.add_route('DELETE', '/messages/{id}', self.delete_messages)
        return app


async def create_api(test_client, server):
    client = await test_client(server.create_app)
    return requests.Requests('my_bot_token', client)


@pytest.fixture
def test_server():
    server = TestServer()
    server.setup()
    yield server


async def test_listing_without_parameters(test_client, test_server):
    api = await create_api(test_client, test_server)
    expected = {
        'list': 'result',
    }
    test_server.response = expected
    expected_headers = {
        'Authorization': 'Bearer my_bot_token',
    }

    response = await api.list('rooms')

    assert response == expected
    assert test_server.last_parameters == {}
    assert test_server.last_headers == expected_headers
    assert test_server.last_id is None
    assert test_server.last_body is None


async def test_listing_with_parameters(test_client, test_server):
    api = await create_api(test_client, test_server)
    expected = {
        'list': 'result with parameters',
    }
    test_server.response = expected
    expected_headers = {
        'Authorization': 'Bearer my_bot_token',
    }

    parameters = {
        'foo': 'bar',
        'hello': 'world',
    }
    response = await api.list('rooms', parameters)

    assert response == expected
    assert test_server.last_parameters == parameters
    assert test_server.last_headers == expected_headers
    assert test_server.last_id is None
    assert test_server.last_body is None


async def test_getting_details(test_client, test_server):
    api = await create_api(test_client, test_server)
    expected = {
        'get': 'information about a message',
    }
    test_server.response = expected
    expected_headers = {
        'Authorization': 'Bearer my_bot_token',
    }

    response = await api.get('messages', 'some_id')

    assert response == expected
    assert test_server.last_id == 'some_id'
    assert test_server.last_headers == expected_headers
    assert test_server.last_parameters is None
    assert test_server.last_body is None


async def test_create_stuff(test_client, test_server):
    api = await create_api(test_client, test_server)
    expected = {
        'create': 'creating a message',
    }
    test_server.response = expected
    expected_headers = {
        'Authorization': 'Bearer my_bot_token',
        'content-type': 'application/json',
    }

    request = {
        'toPersonEmail': 'someemail@gmail.com',
        'title': 'Hello world',
    }
    response = await api.create('messages', request)

    assert response == expected
    assert test_server.last_body == request
    assert test_server.last_headers == expected_headers
    assert test_server.last_id is None
    assert test_server.last_parameters is None


async def test_updating(test_client, test_server):
    api = await create_api(test_client, test_server)
    expected = {
        'update': 'updating a message',
    }
    test_server.response = expected
    expected_headers = {
        'Authorization': 'Bearer my_bot_token',
        'content-type': 'application/json',
    }

    request = {
        'toPersonEmail': 'someemail@gmail.com',
        'title': 'Hello world',
    }
    response = await api.update('messages', 'some_update_id', request)

    assert response == expected
    assert test_server.last_id == 'some_update_id'
    assert test_server.last_body == request
    assert test_server.last_headers == expected_headers
    assert test_server.last_parameters is None


async def test_deleting(test_client, test_server):
    api = await create_api(test_client, test_server)
    test_server.status_code = 204
    expected_headers = {
        'Authorization': 'Bearer my_bot_token',
    }

    response = await api.delete('messages', 'some_delete_id')

    assert response
    assert test_server.last_id == 'some_delete_id'
    assert test_server.last_headers == expected_headers
    assert test_server.last_parameters is None
    assert test_server.last_body is None


async def test_unauthorized_listing(test_client, test_server):
    api = await create_api(test_client, test_server)
    test_server.unauthorized()
    with pytest.raises(exceptions.Unauthorized):
        await api.list('rooms')


async def test_unauthorized_get_details(test_client, test_server):
    api = await create_api(test_client, test_server)
    test_server.unauthorized()
    with pytest.raises(exceptions.Unauthorized):
        await api.get('messages', 'some_id')


async def test_unauthorized_create(test_client, test_server):
    api = await create_api(test_client, test_server)
    test_server.unauthorized()
    with pytest.raises(exceptions.Unauthorized):
        await api.create('messages', {})


async def test_unauthorized_update(test_client, test_server):
    api = await create_api(test_client, test_server)
    test_server.unauthorized()
    with pytest.raises(exceptions.Unauthorized):
        await api.update('messages', 'update_id', {})


async def test_unauthorized_delete(test_client, test_server):
    api = await create_api(test_client, test_server)
    test_server.unauthorized()
    with pytest.raises(exceptions.Unauthorized):
        await api.delete('messages', 'update_id')


async def test_too_many_requests(test_client, test_server):
    api = await create_api(test_client, test_server)
    test_server.retry_after(35251)
    with pytest.raises(exceptions.TooManyRequests):
        await api.list('rooms')


async def test_server_error(test_client, test_server):
    api = await create_api(test_client, test_server)
    test_server.status_code = 503
    test_server.response = {
        'reason': 'Something went wrong on the server',
        'description': [
            'first',
            'second',
        ],
        'tracking_id': 'Some tracking id',
    }
    with pytest.raises(exceptions.ServerError):
        await api.list('rooms')


async def test_not_found(test_client, test_server):
    api = await create_api(test_client, test_server)
    test_server.status_code = 404
    test_server.response = {
        'message': 'Could not find rooms with provided ID',
        'errors': [
            'first',
            'second',
        ],
        'tracking_id': 'Some tracking id',
    }
    with pytest.raises(exceptions.NotFound):
        await api.list('rooms')


async def test_request_error(test_client, test_server):
    api = await create_api(test_client, test_server)
    test_server.status_code = 400
    test_server.response = {
        'message': 'Request error',
        'tracking_id': 'Some tracking id',
    }
    with pytest.raises(exceptions.InvalidRequest):
        await api.list('rooms')


async def test_other_errors(test_client, test_server):
    api = await create_api(test_client, test_server)
    test_server.status_code = 305
    test_server.response = {
        'message': 'Request error',
        'tracking_id': 'Some tracking id',
    }
    with pytest.raises(exceptions.SparkApiException):
        await api.list('rooms')
