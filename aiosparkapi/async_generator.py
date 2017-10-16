class AsyncGenerator:

    def __init__(self, results, Generate):
        self._results = results
        self._Generate = Generate

    async def __aiter__(self):
        return self

    async def __anext__(self):
        return self._Generate(await self._results.__anext__())
