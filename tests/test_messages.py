import pytest

import aiosparkapi.messages


class StubRequests:

    def __init__(self):
        self.path = None
        self.parameters = None
        self.results = []

    async def list(self, path, parameters):
        self.path = path
        self.parameters = parameters
        return self.results

    async def create(self, path, parameters):
        self.path = path
        self.parameters = parameters
        return self.results


async def test_list_with_all_required_parameters():
    requests = StubRequests()
    messages = aiosparkapi.messages.Messages(requests)

    await messages.list(roomId='some_room_id')

    assert requests.path == 'messages'
    assert requests.parameters == {'roomId': 'some_room_id'}


async def test_list_using_all_allowed_parameters():
    requests = StubRequests()
    messages = aiosparkapi.messages.Messages(requests)

    expected = {
        'roomId': 'some_room_id',
        'max': 2,
        'before': '2017-09-07T19:54:44.780Z',
        'beforeMessage': 'some_message_id',
        'mentionedPeople': 'me',
    }

    await messages.list(
        roomId=expected['roomId'],
        mentionedPeople=expected['mentionedPeople'],
        before=expected['before'],
        beforeMessage=expected['beforeMessage'],
        max=expected['max'],
    )

    assert requests.path == 'messages'
    assert requests.parameters == expected


async def test_list_missing_roomId():
    requests = StubRequests()
    messages = aiosparkapi.messages.Messages(requests)

    with pytest.raises(AssertionError):
        await messages.list(mentionedPeople='some person')


async def test_list_returns_all_properties():
    requests = StubRequests()
    messages = aiosparkapi.messages.Messages(requests)
    requests.results = [
        {
            'id': 'first_message_id',
            'roomId': 'some_room_id',
            'roomType': 'group',
            'toPersonId': 'your_bot_id',
            'toPersonEmail': 'yourbot@mail.com',
            'text': 'Hello there',
            'markdown': 'Some markdown',
            'html': '<p>Hello there</p>',
            'personId': 'first_person_id',
            'personEmail': 'someperson@email.com',
            'created': '2017-09-07T19:54:44.780Z',
            'mentionedPeople': [
                'your bot',
            ],
            'files': [
                'http://some_file_hoster.com/first_file',
                'http://some_file_hoster.com/second_file',
            ],
        }
    ]

    response = await messages.list(roomId='some_room_id')

    assert await response.__anext__() == requests.results[0]


async def test_list_returns_multiple_results():
    requests = StubRequests()
    messages = aiosparkapi.messages.Messages(requests)
    requests.results = [
        {
            'id': 'first_message_id',
            'roomId': 'some_room_id',
            'roomType': 'direct',
            'text': 'Hello there',
            'personId': 'first_person_id',
            'personEmail': 'someperson@email.com',
            'created': '2017-09-07T19:54:44.780Z',
        },
        {
            'id': 'second_message_id',
            'roomId': 'some_room_id',
            'roomType': 'group',
            'toPersonId': 'my_person_id',
            'text': 'Hello there',
            'html': '<p>Hello there</p>',
            'personId': 'first_person_id',
            'personEmail': 'someperson@email.com',
            'created': '2017-09-07T19:54:44.780Z',
        }
    ]

    response = await messages.list(roomId='some_room_id')

    for expected in requests.results:
        got = await response.__anext__()
        assert got == expected

    with pytest.raises(StopAsyncIteration):
        await response.__anext__()


async def test_creating_message_to_person_with_id():
    requests = StubRequests()
    messages = aiosparkapi.messages.Messages(requests)

    await messages.create(toPersonId='<some id>', text='Hello')

    assert requests.path == 'messages'
    assert requests.parameters == {'toPersonId': '<some id>',
                                   'text': 'Hello'}


async def test_creating_message_to_person_with_email():
    requests = StubRequests()
    messages = aiosparkapi.messages.Messages(requests)

    await messages.create(toPersonEmail='foo@cisco.com', text='Hello')

    assert requests.path == 'messages'
    assert requests.parameters == {'toPersonEmail': 'foo@cisco.com',
                                   'text': 'Hello'}


async def test_creating_message_to_room():
    requests = StubRequests()
    messages = aiosparkapi.messages.Messages(requests)

    await messages.create(
        toRoomId='<some room id>',
        text='Hello')

    assert requests.path == 'messages'
    assert requests.parameters == {'toRoomId': '<some room id>',
                                   'text': 'Hello'}


async def test_creating_message_using_markdown():
    requests = StubRequests()
    messages = aiosparkapi.messages.Messages(requests)

    await messages.create(
        toPersonEmail='foo@cisco.com',
        markdown='Some markdown')

    assert requests.path == 'messages'
    assert requests.parameters == {'toPersonEmail': 'foo@cisco.com',
                                   'markdown': 'Some markdown'}


async def test_creating_messages_sending_files():
    requests = StubRequests()
    messages = aiosparkapi.messages.Messages(requests)

    await messages.create(
        toPersonEmail='foo@cisco.com',
        files=['first_file', 'second_file'])

    assert requests.path == 'messages'
    assert requests.parameters == {'toPersonEmail': 'foo@cisco.com',
                                   'files': ['first_file', 'second_file']}


async def test_creating_messages_without_recipient():
    requests = StubRequests()
    messages = aiosparkapi.messages.Messages(requests)

    with pytest.raises(AssertionError):
        await messages.create(text='what?')


async def test_creating_messages_multiple_recipients():
    requests = StubRequests()
    messages = aiosparkapi.messages.Messages(requests)

    with pytest.raises(AssertionError):
        await messages.create(toRoomId='first id',
                              toPersonId='second id',
                              toPersonEmail='third id',
                              text='what?')

    with pytest.raises(AssertionError):
        await messages.create(toRoomId='first id',
                              toPersonEmail='third id',
                              text='what?')


async def test_creating_messages_without_content():
    requests = StubRequests()
    messages = aiosparkapi.messages.Messages(requests)

    with pytest.raises(AssertionError):
        await messages.create(toPersonId='some person')


async def test_creating_messages_returns_message():
    requests = StubRequests()
    messages = aiosparkapi.messages.Messages(requests)
    requests.results = {
            'id': 'first_message_id',
            'roomId': 'some_room_id',
            'roomType': 'direct',
            'text': 'Hello there',
            'personId': 'first_person_id',
            'personEmail': 'someperson@email.com',
            'created': '2017-09-07T19:54:44.780Z',
        }

    response = await messages.create(
        toRoomId='some_room_id',
        text='Hello')

    assert response == requests.results
