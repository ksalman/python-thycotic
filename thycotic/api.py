import requests
from urllib.parse import urljoin

REQUEST_TOKEN_URI = "/SecretServer/oauth2/token"
API_URI = "/SecretServer/api/v1"

from thycotic import Folder


class Api:
    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url
        self._get_token()

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

    def get_folders(self, parentfolder=None, skip=None, take=None):
        """Search, filter, sort, and page secret folders

        The caller is responsible for handling pages and looping to gather all
        of the data

        Args:
          parentfolder:
            Parent folder ID [optional]
          skip:
            Number of records to skip before taking results [optional]

        Returns:
          hasNext:
            Whether there are any results in additional pages [bool]
          hasPrev:
            Whether there are any results in previous pages [bool]
          nextSkip:
            Correct value of 'skip' for the next page of results
          prevSkip::
            Correct value of 'skip' for the previous page of results
          pageCount:
            Number of result pages available with current query options

        """

        endpoint = "/folders"
        params = {
            "filter.parentFolderId": parentfolder,
            "skip": skip,
            "take": take,
        }
        response = self._session.get(
            self._geturl(endpoint),
            params=params,
            verify=False,
        )
        return [Folder(**x) for x in response.json()["records"]]

    def _geturl(self, endpoint):
        return urljoin(self.url, API_URI) + endpoint
