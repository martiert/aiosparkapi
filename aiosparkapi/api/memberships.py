from aiosparkapi.baseresponse import BaseResponse
from aiosparkapi.async_generator import AsyncGenerator


class Membership(BaseResponse):

    def __init__(self, result):
        super(Membership, self).__init__(result)


class Memberships:

    def __init__(self, requests):
        self._requests = requests

    async def list(self, roomId=None, personId=None, personEmail=None, max=None):
        parameters = {}
        if roomId:
            parameters['roomId'] = roomId
        if personId:
            parameters['personId'] = personId
        if personEmail:
            parameters['personEmail'] = personEmail
        if max:
            parameters['max'] = max

        result = await self._requests.list('memberships', parameters)
        return AsyncGenerator(result, Membership)

    async def get(self, membership_id):
        return Membership(await self._requests.get('memberships', membership_id))
