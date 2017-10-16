import aiosparkapi.requests
from .api.messages import Messages
from .api.webhooks import Webhooks
from .api.people import People

import aiohttp


class AioSparkApi:

    def __init__(self, *, access_token):
        self._token = access_token

    async def __aenter__(self):
        self._client = aiohttp.ClientSession()
        self._requests = aiosparkapi.requests.Requests(
            self._token,
            self._client,
            baseurl='https://api.ciscospark.com/v1')

        self.messages = Messages(self._requests)
        self.webhooks = Webhooks(self._requests)
        self.people = People(self._requests)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self._client.close()


__all__ = ['AioSparkApi']
