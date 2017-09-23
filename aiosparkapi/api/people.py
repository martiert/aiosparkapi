from aiosparkapi.baseresponse import BaseResponse
from aiosparkapi.async_generator import AsyncGenerator


class Person(BaseResponse):

    def __init__(self, result):
        self._result = result

    @property
    def id(self):
        return self._result['id']

    @property
    def emails(self):
        return self._result['emails']

    @property
    def displayName(self):
        return self._result['displayName']

    @property
    def nickName(self):
        return self._result.get('nickName')

    @property
    def firstName(self):
        return self._result['firstName']

    @property
    def lastName(self):
        return self._result['lastName']

    @property
    def avatar(self):
        return self._result['avatar']

    @property
    def orgId(self):
        return self._result['orgId']

    @property
    def roles(self):
        return self._result.get('roles')

    @property
    def licenses(self):
        return self._result.get('licenses')

    @property
    def timezone(self):
        return self._result.get('timezone')

    @property
    def lastActivity(self):
        return self._result['lastActivity']

    @property
    def status(self):
        return self._result['status']

    @property
    def invitePending(self):
        return self._result.get('invitePending')

    @property
    def loginEnabled(self):
        return self._result.get('loginEnabled')

    @property
    def type(self):
        return self._result['type']

    @property
    def created(self):
        return self._result['created']


class People:

    def __init__(self, requests):
        self._requests = requests

    async def list(self,
                   *,
                   email=None,
                   displayName=None,
                   id=None,
                   orgId=None,
                   max=None):

        params = {}

        if email:
            params['email'] = email
        if displayName:
            params['displayName'] = displayName
        if id:
            params['id'] = id
        if orgId:
            params['orgId'] = orgId
        if max:
            params['max'] = max

        result = await self._requests.list('people', params)
        return AsyncGenerator(result, Person)

    async def get(self, person_id):
        return Person(await self._requests.get('people', person_id))

    async def me(self):
        return await self.get('me')
