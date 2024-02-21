class Auth:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {}

    def get_headers_with_token(self):
        return {"Authorization": f"Bearer {self.token}"}