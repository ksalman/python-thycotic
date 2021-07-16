import requests
from urllib.parse import urljoin


from thycotic import Folder


class Api:
    REQUEST_TOKEN_URI = "/SecretServer/oauth2/token"
    API_URI = "/SecretServer/api/v1"

    def __init__(self, username, password, url, verify=True):
        self.username = username
        self.password = password
        self.url = url
        self._session = requests.Session()
        self._session.verify = verify
        self._token = None

    def auth(self):
        TOKEN_URL = urljoin(self.url, self.REQUEST_TOKEN_URI)
        payload = {
            "username": self.username,
            "password": self.password,
            "grant_type": "password",
        }
        response = requests.post(TOKEN_URL, data=payload, verify=False)
        response.raise_for_status()
        self._token = response.json()
        self._session.headers.update(
            {"Authorization": "Bearer {}".format(self._token["access_token"])}
        )

    def search_folders(
        self,
        foldertypeid=None,
        parentfolder=None,
        permissionrequired="View",
        searchtext=None,
        limit=10,
    ):
        """Search, filter, sort, and page secret folders

        The caller is responsible for handling pages and looping to gather all
        of the data

        :param foldertypeid: (optional) Folder type ID
        :param parantfolder: (optional) Parent folder ID
        :param permissionrequired: (optional) Specify whether to filter by Owner, Edit,
            AddSecret, View folder permission. Default is View
        :param searchtext: (optional) Search text
        :param limit: (optional) Maximum number of records to include in results.
            Default is 10
        :returns: PagingOfFolderSummary

        """

        endpoint = "/folders"
        params = {
            "filter.folderTypeId": foldertypeid,
            "filter.parentFolderId": parentfolder,
            "filter.permissionRequired": permissionrequired,
            "filter.searchText": searchtext,
            "take": limit,
        }
        return self._internal_call("GET", self._geturl(endpoint), params=params)

    def _internal_call(self, method, url, params):
        args = dict(params=params)
        response = self._session.request(method, url, **args)
        response.raise_for_status()
        return response.json()

    def _geturl(self, endpoint):
        return urljoin(self.url, self.API_URI) + endpoint

    def lookup_folders(
        self,
        foldertypeid=None,
        parentfolder=None,
        permissionrequired="View",
        searchtext=None,
        limit=10,
    ):
        """Search, filter, sort, and page secret folders, returning only folder ID and name

        :param foldertypeid: (optional) Folder type ID
        :param parantfolder: (optional) Parent folder ID
        :param permissionrequired: (optional) Specify whether to filter by Owner, Edit,
            AddSecret, View folder permission. Default is View
        :param searchtext: (optional) Search text
        :param limit: (optional) Maximum number of records to include in results.
            Default is 10
        :returns: PagingOfFolderLookup

        """

        endpoint = "/folders/lookup"
        params = {
            "filter.folderTypeId": foldertypeid,
            "filter.parentFolderId": parentfolder,
            "filter.permissionRequired": permissionrequired,
            "filter.searchText": searchtext,
            "take": limit,
        }
        return self._internal_call("GET", self._geturl(endpoint), params=params)
