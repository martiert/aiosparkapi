import urllib.parse

from aiosparkapi.baseresponse import BaseResponse
from aiosparkapi.async_generator import AsyncGenerator


def _is_url(url):
    parsed = urllib.parse.urlparse(url)
    return parsed.scheme.lower() in ['http', 'https', 'ftp'] and parsed.netloc


class Message(BaseResponse):

    def __init__(self, result):
        super(Message, self).__init__(result)

    @property
    def id(self):
        return self._result['id']

    @property
    def roomId(self):
        return self._result['roomId']

    @property
    def roomType(self):
        return self._result['roomType']

    @property
    def personId(self):
        return self._result['personId']

    @property
    def personEmail(self):
        return self._result['personEmail']

    @property
    def created(self):
        return self._result['created']

    @property
    def toPersonId(self):
        return self._result.get('toPersonId')

    @property
    def toPersonEmail(self):
        return self._result.get('toPersonEmail')

    @property
    def text(self):
        return self._result.get('text')

    @property
    def html(self):
        return self._result.get('html')

    @property
    def markdown(self):
        return self._result.get('markdown')

    @property
    def mentionedPeople(self):
        return self._result.get('mentionedPeople')

    @property
    def files(self):
        return self._result.get('files')


class Messages:
    def __init__(self, requests):
        self._requests = requests

    async def list(self, **kwargs):
        '''List all messages in a room

        Args:
            roomId(str): The roomId for the room to list messages from.
            mentionedPeople(str): List messages for a person, by 'personId'
                or 'me'.
            before(str): List messages sent before a data and time in ISO8601
                format.
            beforeMessage(str): List messages sent before a message with id.
            max(int): Limit the maximum number of messages returned from the
                Spark service per request.

        Returns:
            GeneratorContainer: When iterated, the GeneratorContainer yield
                the messages returned by the query.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiException: If the Cisco Spark cloud returns an error.
        '''

        assert 'roomId' in kwargs
        results = await self._requests.list('messages', kwargs)
        return AsyncGenerator(results, Message)

    async def create(self,
                     toRoomId=None,
                     toPersonId=None,
                     toPersonEmail=None,
                     text=None,
                     markdown=None,
                     files=None,
                     **kwargs):

        number_of_recipients = 0
        for recipient in [toRoomId, toPersonId, toPersonEmail]:
            number_of_recipients += 1 if recipient else 0

        assert number_of_recipients == 1
        assert text is not None or markdown is not None or files is not None
        assert files is None or len(files) == 1

        request = {}
        if toRoomId:
            request['toRoomId'] = toRoomId
        if toPersonId:
            request['toPersonId'] = toPersonId
        if toPersonEmail:
            request['toPersonEmail'] = toPersonEmail
        if text:
            request['text'] = text
        if markdown:
            request['markdown'] = markdown
        multipart = False
        if files:
            if _is_url(files[0]):
                request['files'] = files
            else:
                multipart = True
                request['file'] = {
                    'content': open(files[0], 'rb'),
                    'name': files[0],
                }

        for key, value in kwargs.items():
            request[key] = value

        results = await self._requests.create(
            'messages',
            request,
            multipart=multipart)
        return Message(results)

    async def get(self, message_id):
        return Message(await self._requests.get('messages', message_id))

    async def delete(self, message_id):
        await self._requests.delete('messages', message_id)
