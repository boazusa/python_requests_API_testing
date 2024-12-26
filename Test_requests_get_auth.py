import pytest

import requests
from requests.auth import HTTPBasicAuth


def test_basic_auth():
    # URL of the service you are testing
    url = 'https://httpbin.org/basic-auth/user/pass'

    # Using requests.auth.HTTPBasicAuth to send credentials
    response = requests.get(url, auth=('user', 'pass'))

    # Check if authentication was successful
    assert response.status_code == 200
    print(f"Status code: {response.status_code}")


def test_basic_auth_failure():
    # URL of the service you are testing
    url = 'https://httpbin.org/basic-auth/user/pass'

    # Using requests.auth.HTTPBasicAuth to send credentials
    response = requests.get(url, auth=HTTPBasicAuth('err_user', 'pass'))

    # Check if authentication was not successful due to username err
    assert response.status_code == 401
    print(f"Status code: {response.status_code}")

    # Using requests.auth.HTTPBasicAuth to send credentials
    response = requests.get(url, auth=HTTPBasicAuth('user', 'err_pass'))

    # Check if authentication was not successful due to password err
    assert response.status_code == 401
    print(f"Status code: {response.status_code}")

    # Using requests.auth.HTTPBasicAuth to send credentials
    response = requests.get(url, auth=HTTPBasicAuth('err_user', 'err_pass'))

    # Check if authentication was not successful due to password err
    assert response.status_code == 401
    print(f"Status code: {response.status_code}")


if __name__ == "__main__":
    # pytest.main(['Test_requests_get_auth.py::test_basic_auth', '-v'])
    # pytest.main(['Test_requests_get_auth.py::test_basic_auth_failure', '-v'])
    pytest.main(['Test_requests_get_auth.py', '-v', '--showlocals'])
    # test_basic_auth()
