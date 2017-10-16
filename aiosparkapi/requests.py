import json
import aiohttp

import aiosparkapi.exceptions as exceptions


def _add_parameters_to_path(path, parameters):
    if not parameters:
        return path

    path += '?'
    for key, value in parameters.items():
        path += '{}={}&'.format(key, value)
    return path[:-1]


def _create_multipart(arguments):
    data = aiohttp.FormData()
    for key, value in arguments.items():
        filename = None
        content_type = None
        if isinstance(value, dict):
            filename = value['name']
            value = value['content']

        data.add_field(
            key,
            value,
            content_type=content_type,
            filename=filename)
    return data


async def _validate_response(response):
        if response.status == 401:
            raise exceptions.Unauthorized()

        if response.status == 404:
            raise exceptions.NotFound(await response.json())

        if response.status == 429:
            raise exceptions.TooManyRequests(
                int(response.headers.get('retry-after', '3600')))

        if response.status >= 500:
            raise exceptions.ServerError(
                response.status,
                await response.json())

        if response.status >= 400:
            raise exceptions.InvalidRequest(
                response.status,
                await response.json())

        raise exceptions.SparkApiException(
            response.status,
            await response.json(),
            'Failed request')


def _get_next_link(request):
    link = request.headers.get('Link')
    if not link:
        return None

    return link.split()[0][1:-2]


class AsyncGenerator:

    def __init__(self, results, next_link, client, headers):
        self._client = client
        self._headers = headers
        self._set_result(results, next_link)

    def _set_result(self, results, next_link):
        self._results = results['items']
        self._index = 0
        self._length = len(self._results)
        self._next_link = next_link

    async def __aiter__(self):
        return self

    async def __anext__(self):
        if self._index == self._length:
            if not self._next_link:
                raise StopAsyncIteration
            response = await self._client.get(
                self._next_link,
                headers=self._headers)
            if not response.status == 200:
                await _validate_response(response)

            results = await response.json()
            self._set_result(results, _get_next_link(response))

        result = self._results[self._index]
        self._index += 1
        return result


class Requests:

    def __init__(self, token, client, baseurl=''):
        self._client = client
        self._headers = {
            'Authorization': 'Bearer {}'.format(token),
        }
        self._baseurl = baseurl

    async def list(self, path, parameters=None):
        path = '{}/{}'.format(self._baseurl, path)
        path = _add_parameters_to_path(path, parameters)
        response = await self._client.get(path, headers=self._headers)

        if not response.status == 200:
            await _validate_response(response)

        results = await response.json()
        return AsyncGenerator(
            results,
            _get_next_link(response),
            self._client, self._headers)

    async def get(self, path, fetch_id):
        path = '{}/{}/{}'.format(self._baseurl, path, fetch_id)
        response = await self._client.get(path, headers=self._headers)

        if response.status == 200:
            return await response.json()
        await _validate_response(response)

    async def create(self, path, arguments, *, multipart=False):
        path = '{}/{}'.format(self._baseurl, path)
        headers = self._headers
        data = None
        if not multipart:
            headers['content-type'] = 'application/json'
            data = json.dumps(arguments)
        else:
            data = _create_multipart(arguments)

        response = await self._client.post(
            path,
            headers=headers,
            data=data)

        if response.status == 200:
            return await response.json()
        await _validate_response(response)

    async def update(self, path, update_id, arguments):
        path = '{}/{}/{}'.format(self._baseurl, path, update_id)
        headers = self._headers
        headers['content-type'] = 'application/json'

        response = await self._client.put(
            path,
            headers=headers,
            data=json.dumps(arguments))

        if response.status == 200:
            return await response.json()
        await _validate_response(response)

    async def delete(self, path, delete_id):
        path = '{}/{}/{}'.format(self._baseurl, path, delete_id)

        response = await self._client.delete(
            path,
            headers=self._headers)

        if response.status == 204:
            return True
        await _validate_response(response)
