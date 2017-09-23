import pytest

import aiosparkapi.api.people
from .stubrequests import StubRequests


async def test_list_with_all_required_parameters():
    requests = StubRequests()
    people = aiosparkapi.api.people.People(requests)

    expected = {
        'email': 'some_email',
        'displayName': 'some display name',
        'id': 'some id',
        'orgId': 'some org id',
        'max': 10,
    }

    await people.list(
        email=expected['email'],
        displayName=expected['displayName'],
        id=expected['id'],
        orgId=expected['orgId'],
        max=expected['max'])

    assert requests.path == 'people'
    assert requests.list_parameters == expected


async def test_list_without_any_parameters():
    requests = StubRequests()
    people = aiosparkapi.api.people.People(requests)

    await people.list()

    assert requests.path == 'people'
    assert requests.list_parameters == {}


async def test_list_results():
    requests = StubRequests()
    requests.results = [
        {
            'id': 'first id',
            'name': 'first name',
        },
        {
            'id': 'second id',
            'name': 'second name',
        },
        {
            'id': 'third id',
            'name': 'third name',
        },
    ]
    people = aiosparkapi.api.people.People(requests)

    result = await people.list()

    for expected in requests.results:
        got = await result.__anext__()
        assert got == expected
        assert isinstance(got, aiosparkapi.api.people.Person)

    with pytest.raises(StopAsyncIteration):
        await result.__anext__()


async def test_getting_person_details():
    requests = StubRequests()
    requests.results = {
        'id': 'some id',
        'emails': ['john.andersen@example.com', 'john.andersen@gmail.com'],
        'displayName': 'John Andersen',
        'firstName': 'John',
        'lastName': 'Andersen',
        'avatar': 'http://ciscospark/johnanders.avatar',
    }

    people = aiosparkapi.api.people.People(requests)

    result = await people.get('some person id')

    assert requests.path == 'people'
    assert requests.get_id == 'some person id'
    assert result == requests.results


async def test_getting_myself():
    requests = StubRequests()
    requests.results = {
        'id': 'my id',
        'emails': ['john.andersen@example.com'],
        'displayName': 'This is me!',
        'firstName': 'First',
        'lastName': 'Last',
        'avatar': 'http://ciscospark/johnanders.avatar',
    }

    people = aiosparkapi.api.people.People(requests)

    result = await people.me()

    assert requests.path == 'people'
    assert requests.get_id == 'me'
    assert result == requests.results
