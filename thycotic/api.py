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
        return self._get(self._geturl(endpoint), endpoint=endpoint, params=params)

    def _get(self, url, **kwargs):
        return self._internal_call("GET", url, kwargs)

    def _internal_call(self, method, url, params):
        endpoint = params.pop("endpoint")
        args = dict(params=params)
        args["params"] = args["params"]["params"]
        response = self._session.request(method, url, **args)
        response.raise_for_status()
        mydict = response.json()
        mydict["endpoint"] = endpoint
        return mydict

    def _geturl(self, endpoint):
        return urljoin(self.url, self.API_URI) + endpoint

    def next(self, result):
        """Helper method to handle pagination"""

        if not ("endpoint" or "filter") in result:
            return None
        if result["hasNext"] == False:
            return None
        endpoint = result["endpoint"]
        params = {}
        for k in result["filter"]:
            params[f"filter.{k}"] = result["filter"][k]
        params["skip"] = result["skip"] + result["take"]
        params["take"] = result["take"]
        return self._get(self._geturl(endpoint), endpoint=endpoint, params=params)
