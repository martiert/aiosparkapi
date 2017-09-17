class Message:
    def __init__(self, result):
        self._result = result

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

    def __getattr__(self, item):
        if item not in list(self._result.keys()):
            error = "'{}' object has no attribute '{}'".format(
                    self.__class__.__name__, item)
            raise AttributeError(error)

        return self._result[item]

    def __eq__(self, other):
        return other == self._result


class AsyncGenerator:

    def __init__(self, results):
        self._results = results
        self._index = 0
        self._length = len(results)

    async def __aiter__(self):
        return self

    async def __anext__(self):
        if self._index == self._length:
            raise StopAsyncIteration

        message = Message(self._results[self._index])
        self._index += 1
        return message


class Messages:
    def __init__(self, requests):
        self._requests = requests

    async def list(self,
                   roomId=None,
                   mentionedPeople=None,
                   before=None,
                   beforeMessage=None,
                   max=None):
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

        assert roomId is not None

        params = {}
        params['roomId'] = roomId
        if mentionedPeople:
            params['mentionedPeople'] = mentionedPeople
        if before:
            params['before'] = before
        if beforeMessage:
            params['beforeMessage'] = beforeMessage
        if max:
            params['max'] = max

        results = await self._requests.list('messages', params)
        return AsyncGenerator(results)

    async def create(self,
                     toRoomId=None,
                     toPersonId=None,
                     toPersonEmail=None,
                     text=None,
                     markdown=None,
                     files=None):

        number_of_recipients = 0
        for recipient in [toRoomId, toPersonId, toPersonEmail]:
            number_of_recipients += 1 if recipient else 0

        assert number_of_recipients == 1
        assert text is not None or markdown is not None or files is not None

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
        if files:
            request['files'] = files

        results = await self._requests.create(
            'messages',
            request)
        return results

    async def get(self, message_id):
        return await self._requests.get('messages', message_id)

    async def delete(self, message_id):
        await self._requests.delete('messages', message_id)
