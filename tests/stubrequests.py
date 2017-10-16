class IterableFaker:
    def __init__(self, result):
        self._result = result
        self._index = 0
        self._len = len(result)

    async def __anext__(self):
        if self._index == self._len:
            raise StopAsyncIteration
        answer = self._result[self._index]
        self._index += 1
        return answer


class StubRequests:

    def __init__(self):
        self.path = None
        self.list_parameters = None
        self.create_parameters = None
        self.create_multipart_parameters = None
        self.update_parameters = None
        self.get_id = None
        self.delete_id = None
        self.update_id = None
        self.results = []

    async def list(self, path, parameters=None):
        self.path = path
        self.list_parameters = parameters
        return IterableFaker(self.results)

    async def create(self, path, parameters, *, multipart=False):
        self.path = path
        if not multipart:
            self.create_parameters = parameters
        else:
            content = parameters['file']['content'].read()
            parameters['file']['content'] = content
            self.create_multipart_parameters = parameters
        return self.results

    async def get(self, path, get_id):
        self.path = path
        self.get_id = get_id
        return self.results

    async def delete(self, path, delete_id):
        self.path = path
        self.delete_id = delete_id
        return self.results

    async def update(self, path, update_id, parameters):
        self.path = path
        self.update_id = update_id
        self.update_parameters = parameters
        return self.results
