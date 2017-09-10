import pytest

import aiosparkapi.messages


def test_message_representation_of_all_known_properties():
    message = {
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
    result = aiosparkapi.messages.Message(message)

    assert result.id == message['id']
    assert result.roomId == message['roomId']
    assert result.roomType == message['roomType']
    assert result.toPersonId == message['toPersonId']
    assert result.toPersonEmail == message['toPersonEmail']
    assert result.text == message['text']
    assert result.markdown == message['markdown']
    assert result.html == message['html']
    assert result.personId == message['personId']
    assert result.personEmail == message['personEmail']
    assert result.created == message['created']
    assert result.mentionedPeople == message['mentionedPeople']
    assert result.files == message['files']


async def test_listing_returns_only_non_optional_properties():
    message = {
        'id': 'first_message_id',
        'roomId': 'some_room_id',
        'roomType': 'direct',
        'personId': 'first_person_id',
        'personEmail': 'someperson@email.com',
        'created': '2017-09-07T19:54:44.780Z',
    }
    result = aiosparkapi.messages.Message(message)

    assert result.toPersonId is None
    assert result.toPersonEmail is None
    assert result.text is None
    assert result.markdown is None
    assert result.html is None
    assert result.mentionedPeople is None
    assert result.files is None


async def test_message_with_unhandled_property():
    message = {
        'id': 'first_message_id',
        'roomId': 'some_room_id',
        'roomType': 'direct',
        'personId': 'first_person_id',
        'personEmail': 'someperson@email.com',
        'created': '2017-09-07T19:54:44.780Z',
        'unknown': 'some_unknown_property',
    }
    result = aiosparkapi.messages.Message(message)

    assert result.unknown == 'some_unknown_property'

    with pytest.raises(AttributeError):
        result.non_existent


async def test_message_equality():
    message = {
        'id': 'first_message_id',
        'roomId': 'some_room_id',
        'roomType': 'direct',
        'personId': 'first_person_id',
        'personEmail': 'someperson@email.com',
        'created': '2017-09-07T19:54:44.780Z',
        'unknown': 'some_unknown_property',
    }
    first = aiosparkapi.messages.Message(message)
    second = aiosparkapi.messages.Message(message)

    assert first == second


async def test_message_equality_with_dict():
    message = {
        'id': 'first_message_id',
        'roomId': 'some_room_id',
        'roomType': 'direct',
        'personId': 'first_person_id',
        'personEmail': 'someperson@email.com',
        'created': '2017-09-07T19:54:44.780Z',
        'unknown': 'some_unknown_property',
    }
    result = aiosparkapi.messages.Message(message)

    assert result == message
