import requests
from urllib.parse import urljoin

REQUEST_TOKEN_URI = "/SecretServer/oauth2/token"
API_URI = "/SecretServer/api/v1"

from thycotic import Folder


class Api:
    def __init__(self, username, password, url, verify=True):
        self.username = username
        self.password = password
        self.url = url
        self.verify = verify
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
        self._session.verify = self.verify

    def get_folders(
        self, parentfolder=None, permissionrequired="View", skip=None, take=None
    ):
        """Search, filter, sort, and page secret folders

        The caller is responsible for handling pages and looping to gather all
        of the data

        :param parantfolder: (optional) Parent folder ID
        :param permissionrequired: (optional) Specify whether to filter by Owner, Edit,
            AddSecret, View folder permission. Default is View
        :param skip: (optional) Number of recoreds to skip taking results
        :param take: (optional) Maximum number of records to include in results
        :returns: PagingOfFolderSummary

        """

        endpoint = "/folders"
        params = {
            "filter.parentFolderId": parentfolder,
            "filter.permissionRequired": permissionrequired,
            "skip": skip,
            "take": take,
        }
        return self._get(self._geturl(endpoint), params=params)

    def _get(self, url, **kwargs):
        return self._internal_call("GET", url, kwargs)

    def _internal_call(self, method, url, params):
        args = dict(params=params)
        args["params"] = args["params"]["params"]
        response = self._session.request(method, url, **args)
        response.raise_for_status()
        return response.json()

    def _geturl(self, endpoint):
        return urljoin(self.url, API_URI) + endpoint
