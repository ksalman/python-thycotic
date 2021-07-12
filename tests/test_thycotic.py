from pytest import fixture
import thycotic
import os
import vcr

username = os.environ.get("THYCOTIC_USER")
password = os.environ.get("THYCOTIC_PASS")
url = os.environ.get("THYCOTIC_URL")


@fixture
def token_keys():
    """Access token data"""
    return ["access_token", "token_type", "expires_in", "refresh_token"]


@vcr.use_cassette("tests/vcr_cassette/get_token")
def test_get_token(token_keys):
    ss = thycotic.Api(username, password, url)
    response = ss._get_token()
    assert isinstance(response.json(), dict)
    assert set(token_keys).issubset(response.json())
