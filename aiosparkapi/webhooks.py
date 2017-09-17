from aiosparkapi.baseresponse import BaseResponse
from aiosparkapi.async_generator import AsyncGenerator


class Webhook(BaseResponse):

    def __init__(self, result):
        super(Webhook, self).__init__(result)

    @property
    def id(self):
        return self._result['id']

    @property
    def name(self):
        return self._result['name']

    @property
    def targetUrl(self):
        return self._result['targetUrl']

    @property
    def resource(self):
        return self._result['resource']

    @property
    def event(self):
        return self._result['event']

    @property
    def filter(self):
        return self._result.get('filter')

    @property
    def secret(self):
        return self._result.get('secret')

    @property
    def created(self):
        return self._result['created']


class Webhooks:

    def __init__(self, requests):
        self._requests = requests

    async def list(self, max=None):
        parameters = {}
        if max:
            parameters['max'] = max
        result = await self._requests.list('webhooks', parameters)
        return AsyncGenerator(result, Webhook)

    async def create(self,
                     name=None,
                     targetUrl=None,
                     resource=None,
                     event=None,
                     filter=None,
                     secret=None):

        assert name is not None
        assert targetUrl is not None
        assert resource is not None
        assert event is not None

        parameters = {
            'name': name,
            'targetUrl': targetUrl,
            'resource': resource,
            'event': event,
        }
        if filter:
            parameters['filter'] = filter
        if secret:
            parameters['secret'] = secret

        return await self._requests.create('webhooks', parameters)
