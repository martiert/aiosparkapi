class StubRequests:

    def __init__(self):
        self.path = None
        self.list_parameters = None
        self.create_parameters = None
        self.get_id = None
        self.delete_id = None
        self.results = []

    async def list(self, path, parameters=None):
        self.path = path
        self.list_parameters = parameters
        return self.results

    async def create(self, path, parameters):
        self.path = path
        self.create_parameters = parameters
        return self.results

    async def get(self, path, get_id):
        self.path = path
        self.get_id = get_id
        return self.results

    async def delete(self, path, delete_id):
        self.path = path
        self.delete_id = delete_id
        return self.results
