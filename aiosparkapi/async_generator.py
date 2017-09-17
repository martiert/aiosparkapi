class AsyncGenerator:

    def __init__(self, results, Generate):
        self._results = results
        self._index = 0
        self._length = len(results)
        self._Generate = Generate

    async def __aiter__(self):
        return self

    async def __anext__(self):
        if self._index == self._length:
            raise StopAsyncIteration

        message = self._Generate(self._results[self._index])
        self._index += 1
        return message
