class InvalidAPIResponse(Exception):
    def __init__(self, message="API returned an unexpected response"):
        self.message = message
        super().__init__(self.message)