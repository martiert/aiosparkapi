import aiosparkapi.requests
from .api.messages import Messages
from .api.webhooks import Webhooks
from .api.people import People

import aiohttp


class AioSparkApi:

    def __init__(self, *, access_token):
        self._client = aiohttp.ClientSession('https://api.ciscospark.com/v1/')
        self._requests = aiosparkapi.requests.Requests(
            access_token,
            self._client)

        self.messages = Messages(self._requests)
        self.webhooks = Webhooks(self._requests)
        self.people = People(self._requests)


__all__ = ['AioSparkApi']
