import json

import aiosparkapi.exceptions as exceptions


def add_parameters_to_path(path, parameters):
    if not parameters:
        return path

    path += '?'
    for key, value in parameters.items():
        path += '{}={}&'.format(key, value)
    return path[:-1]


async def validate_response(response):
        if response.status == 401:
            raise exceptions.UnauthroizedException()

        if response.status == 404:
            data = await response.json()
            raise exceptions.NotFound(
                data['message'],
                data['errors'],
                data['tracking_id'])

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
            await response.json())


class Requests:

    def __init__(self, token, client):
        self._client = client
        self._headers = {
            'Authorization': 'Bearer {}'.format(token),
        }

    async def list(self, path, parameters=None):
        path = add_parameters_to_path(path, parameters)
        response = await self._client.get(path, headers=self._headers)

        if response.status == 200:
            return await response.json()
        await validate_response(response)

    async def get(self, path, fetch_id):
        path = '{}/{}'.format(path, fetch_id)
        response = await self._client.get(path, headers=self._headers)

        if response.status == 200:
            return await response.json()
        await validate_response(response)

    async def create(self, path, arguments):
        headers = self._headers
        headers['content-type'] = 'application/json'

        response = await self._client.post(
            path,
            headers=headers,
            data=json.dumps(arguments))

        if response.status == 200:
            return await response.json()
        await validate_response(response)

    async def update(self, path, update_id, arguments):
        path = '{}/{}'.format(path, update_id)
        headers = self._headers
        headers['content-type'] = 'application/json'

        response = await self._client.put(
            path,
            headers=headers,
            data=json.dumps(arguments))

        if response.status == 200:
            return await response.json()
        await validate_response(response)

    async def delete(self, path, delete_id):
        path = '{}/{}'.format(path, delete_id)

        response = await self._client.delete(
            path,
            headers=self._headers)

        if response.status == 204:
            return True
        await validate_response(response)
