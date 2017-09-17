import aiosparkapi.baseresponse


class Webhook(aiosparkapi.baseresponse.BaseResponse):

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
        await self._requests.list('webhooks', parameters)
