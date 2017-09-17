import pytest

import aiosparkapi.webhooks


def test_webhook_representation_of_all_known_properties():
    webhook = {
        'id': 'some webhook id',
        'name': 'User defined webhook name',
        'targetUrl': 'https://my_webhook_url.com',
        'resource': 'messages',
        'event': 'created',
        'filter': 'roomId=<some room id>',
        'secret': 'I am a terrible secret!',
        'created': '2017-09-07T20:54:44.780Z',
    }

    result = aiosparkapi.webhooks.Webhook(webhook)

    assert result.id == webhook['id']
    assert result.name == webhook['name']
    assert result.targetUrl == webhook['targetUrl']
    assert result.resource == webhook['resource']
    assert result.event == webhook['event']
    assert result.filter == webhook['filter']
    assert result.secret == webhook['secret']
    assert result.created == webhook['created']


def test_webhook_only_required_properties():
    webhook = {
        'id': 'some webhook id',
        'name': 'User defined webhook name',
        'targetUrl': 'https://my_webhook_url.com',
        'resource': 'messages',
        'event': 'created',
        'created': '2017-09-07T20:54:44.780Z',
    }

    result = aiosparkapi.webhooks.Webhook(webhook)

    assert not result.filter
    assert not result.secret
    assert result.id == webhook['id']
    assert result.name == webhook['name']
    assert result.targetUrl == webhook['targetUrl']
    assert result.resource == webhook['resource']
    assert result.event == webhook['event']
    assert result.created == webhook['created']


def test_webhook_representation_of_unkown_property():
    webhook = {
        'something': 'some unkown webhook property',
    }

    result = aiosparkapi.webhooks.Webhook(webhook)

    assert result.something == webhook['something']
    with pytest.raises(AttributeError):
        result.do_not_exist


def test_webhook_equalities():
    webhook = {
        'id': 'some webhook id',
        'name': 'User defined webhook name',
        'targetUrl': 'https://my_webhook_url.com',
        'resource': 'messages',
        'event': 'created',
        'filter': 'roomId=<some room id>',
        'secret': 'I am a terrible secret!',
        'created': '2017-09-07T20:54:44.780Z',
    }

    first = aiosparkapi.webhooks.Webhook(webhook)
    second = aiosparkapi.webhooks.Webhook(webhook)

    assert first == second
    assert first == webhook
