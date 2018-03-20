from aiosparkapi.baseresponse import BaseResponse
from aiosparkapi.async_generator import AsyncGenerator


class Room(BaseResponse):

    def __init__(self, result):
        super(Room, self).__init__(result)


class Rooms:

    def __init__(self, requests):
        self._requests = requests

    async def get(self, room_id):
        return Room(await self._requests.get('rooms', room_id))
