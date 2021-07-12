import requests
from urllib.parse import urljoin

REQUEST_TOKEN_URI = "/SecretServer/oauth2/token"
API_URI = "/SecretServer/api/v1"


class thycotic:
    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url

    def _get_token(self):
        TOKEN_URL = urljoin(self.url, REQUEST_TOKEN_URI)
        payload = {
            "username": self.username,
            "password": self.password,
            "grant_type": "password",
        }
        response = requests.post(TOKEN_URL, data=payload, verify=False)
        self._set_headers(response)
        return response

    def _set_headers(self, response):
        s = requests.Session()
        ACCESS_TOKEN = response.json()["access_token"]
        s.headers.update({"Authorization": "Bearer {}".format(ACCESS_TOKEN)})
        self._session = s
