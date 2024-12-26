# https://reqres.in/

import pytest
import requests

@pytest.fixture(scope='session')
def url_fixture():
    return 'https://reqres.in/'

def url_not_fixture():
    return 'https://reqres.in/'


def test_reqres_in_get(url_fixture):
    params = {'page': 2}
    print(url_fixture + 'users')
    response = requests.get(url_fixture + 'api/users', params=params)
    print(response.url)
    assert response.status_code == 200
    assert response.apparent_encoding == 'ascii'

    assert response.json()['data'][2]['id'] == 9
    assert 'https://reqres.in/' == url_fixture
    print(url_fixture)


def test_reqres_in_delete(url_fixture):
    params = {'page': 2}
    response = requests.delete(url_fixture + 'api/users/2')
    assert response.status_code == 204
    assert response.apparent_encoding == 'utf-8', f"expecet utf-8 encoding, but received {response.apparent_encoding}"
    assert response.request.method == 'delete'.upper()
    assert len(response.text) == 0
    assert response.request.headers['User-Agent'] == 'python-requests/2.32.3'
    assert 'Content-Length' in response.request.headers
    assert response.request.headers['Content-Length'] == '0'

    response = requests.get(url_fixture + 'api/users/2')
    assert response.status_code == 200, f"expecet response status_code 200, but received {response.status_code}"
    assert response.request.method == 'GET'
    assert len(response.text) != 0
    assert "email" in response.json()['data']
    assert "@" in response.json()['data']['email']
    assert response.request.headers['User-Agent'] == 'python-requests/2.32.3'
    assert 'Content-Length' not in response.request.headers


def test_reqres_in_post(url_fixture):
    url = url_fixture + 'api/users'
    payload = {
        'job': 'leader',
        'id': '770',
        'dummy': 111
    }

    response = requests.post(url, json=payload)
    assert response.status_code == 201  # 201 Created
    assert response.apparent_encoding == 'ascii'
    for key in payload:
        assert payload[key] == response.json()[key]
    assert response.request.method == 'POST'

if __name__ == '__main__':
    pytest.main(['Test_reqres_in_web_API.py', '-v', '--showlocals'])
    # pytest.main()