from pytest import fixture
import requests
import requests_mock
import thycotic
import os
import vcr

username = os.environ.get("THYCOTIC_USER")
password = os.environ.get("THYCOTIC_PASS")
url = os.environ.get("THYCOTIC_URL")
MOCKUSER = "username"
MOCKPASS = "password"
MOCKURL = "http://examaple.com"


@fixture
def token_keys():
    """Access token data"""
    return ["access_token", "token_type", "expires_in", "refresh_token"]


def test_auth(token_keys):
    ss = thycotic.Api(username, password, url)
    ss.auth()
    assert isinstance(ss._token, dict)
    assert set(token_keys).issubset(ss._token)


@fixture
def PagingOfFolderPermissionSummary():
    return {
        "filter": {
            "searchText": None,
            "folderTypeId": None,
            "parentFolderId": 1234,
            "permissionRequired": None,
        },
        "skip": 10,
        "take": 10,
        "total": 123,
        "pageCount": 12,
        "currentPage": 2,
        "batchCount": 12,
        "prevSkip": 0,
        "nextSkip": 20,
        "hasPrev": True,
        "hasNext": True,
        "records": [
            {
                "id": 1234,
                "folderName": "server1",
                "folderPath": "\\Team\\Unix\\server1",
                "parentFolderId": 1234,
                "folderTypeId": 1,
                "secretPolicyId": 1,
                "inheritSecretPolicy": True,
                "inheritPermissions": True,
            }
        ],
        "sortBy": [],
        "success": True,
        "severity": "None",
    }


def test_mock_search_folders(requests_mock, PagingOfFolderPermissionSummary):
    ss = thycotic.Api(MOCKUSER, MOCKPASS, MOCKURL)
    requests_mock.get(ss.API_URI + "/folders", json=PagingOfFolderPermissionSummary)
    resp = ss.search_folders()
    assert isinstance(resp, dict)
    assert isinstance(resp["records"], list)
    assert 1234 == resp["filter"]["parentFolderId"]
