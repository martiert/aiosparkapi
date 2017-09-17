import pytest

import aiosparkapi.webhooks
from .stubrequests import StubRequests


async def test_listing_webhooks():
    requests = StubRequests()
    webhooks = aiosparkapi.webhooks.Webhooks(requests)

    await webhooks.list()

    assert requests.path == 'webhooks'
    assert not requests.list_parameters


async def test_listing_webooks_with_limit():
    requests = StubRequests()
    webhooks = aiosparkapi.webhooks.Webhooks(requests)

    await webhooks.list(max=10)

    assert requests.path == 'webhooks'
    assert requests.list_parameters == {'max': 10}


async def test_listed_webooks_are_traversable():
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
    webhooks = aiosparkapi.webhooks.Webhooks(requests)

    result = await webhooks.list()

    for expected in requests.results:
        got = await result.__anext__()
        assert got == expected

    with pytest.raises(StopAsyncIteration):
        await result.__anext__()


async def test_creating_webhook_only_required_parameters():
    requests = StubRequests()
    webhooks = aiosparkapi.webhooks.Webhooks(requests)

    expected = {
        'name': 'My webhook',
        'targetUrl': 'https://some.target.url',
        'resource': 'messages',
        'event': 'created',
    }

    await webhooks.create(
        name=expected['name'],
        targetUrl=expected['targetUrl'],
        resource=expected['resource'],
        event=expected['event'])

    assert requests.path == 'webhooks'
    assert requests.create_parameters == expected


async def test_creating_webhook_all_parameters():
    requests = StubRequests()
    webhooks = aiosparkapi.webhooks.Webhooks(requests)

    expected = {
        'name': 'My webhook',
        'targetUrl': 'https://some.target.url',
        'resource': 'messages',
        'event': 'created',
        'filter': 'roomId=abcdeabcd',
        'secret': 'super secret',
    }

    await webhooks.create(
        name=expected['name'],
        targetUrl=expected['targetUrl'],
        resource=expected['resource'],
        event=expected['event'],
        filter=expected['filter'],
        secret=expected['secret'])

    assert requests.path == 'webhooks'
    assert requests.create_parameters == expected


async def test_response_from_creating_webhook():
    requests = StubRequests()
    requests.results = {
        'name': 'My webhook',
        'targetUrl': 'https://some.target.url',
        'resource': 'messages',
        'event': 'created',
        'created': 'some time',
    }
    webhooks = aiosparkapi.webhooks.Webhooks(requests)

    response = await webhooks.create(
        name='My webhook',
        targetUrl='https://my.target.url',
        resource='messages',
        event='created')

    assert response == requests.results


async def test_creating_webhook_without_required_parameters():
    requests = StubRequests()
    webhooks = aiosparkapi.webhooks.Webhooks(requests)

    with pytest.raises(AssertionError):
        await webhooks.create(
            targetUrl='https://my.target.url',
            resource='messages',
            event='created')

    with pytest.raises(AssertionError):
        await webhooks.create(
            name='some name',
            resource='messages',
            event='created')

    with pytest.raises(AssertionError):
        await webhooks.create(
            name='some name',
            targetUrl='https://my.target.url',
            event='created')

    with pytest.raises(AssertionError):
        await webhooks.create(
            name='some name',
            targetUrl='https://my.target.url',
            resource='messages')
