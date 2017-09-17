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
