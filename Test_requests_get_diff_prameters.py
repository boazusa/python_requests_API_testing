import pytest
import requests
from requests.auth import HTTPBasicAuth
import os

def test_basic_auth():
    # URL of the service you are testing
    url = 'https://httpbin.org/basic-auth/user/pass'

    # Using requests.auth.HTTPBasicAuth to send credentials
    response = requests.get(url, auth=HTTPBasicAuth('user', 'pass'), timeout=3)

    # Check if authentication was successful
    assert response.status_code == 200
    print(f"Status code: {response.status_code}")

def test_requests_get_1():
    user_id = 12
    # url = f'https://api.example.com/users/{user_id}'
    url = f'https://jsonplaceholder.typicode.com/posts/{user_id}'

    response = requests.get(url, timeout=3)
    assert response.status_code == 200
    assert response.request.headers['User-Agent'] == 'python-requests/2.32.3'
    assert response.json()['id'] == user_id
    assert response.url.split('/')[-1] == str(user_id)
    assert response.request.path_url == url.split('.com')[1]
    # print(response.json())
    # print(response.request.headers)
    # print(response.url)
    # print(response.request.body)


def test_requests_query_parameters():
    # Define query parameters
    params = {
        'q': 'python',
        'sort': 'desc',
        'page': '2',
        'limit': '10'
    }
    url = f'https://jsonplaceholder.typicode.com/posts/1'
    # Make the GET request with query parameters
    response = requests.patch(url, params=params, headers=params)

    assert response.status_code == 200, f"Expected response.status_code 200, but got {response.status_code}"
    #
    assert 'title' in response.json() and 'body' in response.json()
    for val in params.values():
        assert val in response.url
    assert response.request.headers['User-Agent'] == 'python-requests/2.32.3'
    assert response.headers['Content-Type'] == 'application/json; charset=utf-8'
    assert response.headers['Connection'] == 'keep-alive'
    # print(response.json())
    # print(response.url)


def test_requests_query_parameters_2():
    # Define query parameters
    params = {
        'postId': '1'
    }
    url = f'https://jsonplaceholder.typicode.com/comments'

    # Make the GET request with query parameters
    response = requests.get(url, params=params, headers=params)

    assert response.status_code == 200, f"Expected response.status_code 200, but got {response.status_code}"
    #
    curr_id = 1
    for d in response.json():
        assert '@' in d['email']
        assert d['id'] == curr_id
        assert d['postId'] == 1
        assert 'name' in d and 'body' in d
        curr_id += 1
    assert len(response.json()) > 2
    assert response.headers['Content-Type'] == 'application/json; charset=utf-8'
    assert response.request.headers['Connection'] == 'keep-alive'
    first_key, first_val = next(iter(params.items()), (None, None))
    assert response.url == url + '?' + first_key + '=' + first_val
    # print(response.headers)
    # print(response.request.headers)
    # print(len(response.json()))
    # print(response.url)


def test_requests_get_headers():
    url = f'https://jsonplaceholder.typicode.com/posts/1'

    # Headers with an Authorization token
    headers = {
        'Authorization': 'Bearer YOUR_TOKEN_HERE',
        'User-Agent': 'MyApp/1.0'
    }

    response = requests.get(url, headers=headers)
    #
    assert response.request.headers['Authorization'] == 'Bearer YOUR_TOKEN_HERE'
    assert response.request.headers['User-Agent'] == 'MyApp/1.0'

def test_requests_get_auth():
    # URL of the service you are testing
    url = 'https://httpbin.org/basic-auth/user/pass'

    # Using requests.auth.HTTPBasicAuth to send credentials
    response = requests.get(url, auth=('user', 'pass'))

    # Check if authentication was successful
    assert response.status_code == 200

    # Using requests.auth.HTTPBasicAuth to send credentials
    response = requests.get(url, auth=('usera', 'pass'))
    # Check if authentication was successful
    assert response.status_code == 401

    # Using requests.auth.HTTPBasicAuth to send credentials
    response = requests.get(url, auth=('auser', 'pass'))
    # Check if authentication was successful
    assert response.status_code == 401

    # Using requests.auth.HTTPBasicAuth to send credentials
    response = requests.get(url, auth=('user', 'passz'))
    # Check if authentication was successful
    assert response.status_code == 401

    # Using requests.auth.HTTPBasicAuth to send credentials
    response = requests.get(url, auth=('user', 'zpass'))
    # Check if authentication was successful
    assert response.status_code == 401


def test_requests_get_cookies():
    url = f'https://jsonplaceholder.typicode.com/posts/1'

    # Cookies to send with the request
    cookies = {
        'sessionid': 'abc123',
        'loggedin': 'true'
    }
    response = requests.get(url, cookies=cookies)

    assert response.status_code == 200, f"Expected response.status_code 200, but got {response.status_code}"
    assert response.cookies.values() == []


def test_requests_get_timeout():
    response = requests.get('https://httpbin.org/delay/1', timeout=3)

    assert response.status_code == 200, f"Expected response.status_code 200, but got {response.status_code}"
    with pytest.raises(requests.exceptions.Timeout):
        requests.get('https://httpbin.org/delay/5', timeout=2)  # 5 seconds delay, 2 seconds timeout
    # with pytest.raises(TimeoutError):
    #     requests.get('https://httpbin.org/delay/3', timeout=1)  # 3 seconds delay, 1 seconds timeout


def test_request_get_download():
    photos_url = 'https://jsonplaceholder.typicode.com/photos'
    response = requests.get(photos_url)
    assert response.status_code == 200, f"Expected response.status_code 200, but got {response.status_code}"

    folder_path = 'download_colors'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    count = 0
    for d in response.json():
        if count == 2:
            break
        assert 'url' in d
        url = d['url']
        photo_name = url.split('/')[-1]
        photo_response = requests.get(url)
        assert photo_response.status_code in [200, 504], f"Expected photo_response.status_code 200, " \
                                                  f"but got {photo_response.status_code} for {url}"
        print(f'status code: {photo_response.status_code}, url: {url}')
        file_path = os.path.join(folder_path, photo_name)
        #
        with open(file_path + '.jpg', 'wb') as file:
            file.write(photo_response.content)
        count += 1

    count = 0
    for d in response.json():
        if count == 2:
            break
        assert 'thumbnailUrl' in d
        thumbnailUrl = d['thumbnailUrl']
        #
        with pytest.raises(requests.exceptions.Timeout):
            requests.get(thumbnailUrl, timeout=2)  # 2 seconds timeout
            response = requests.get(thumbnailUrl)
            assert response.status_code in [200, 504], f"Expected photo_response.status_code 200, " \
                                                  f"but got {response.status_code} for {thumbnailUrl}"
        print(f'thumbnailUrl: {thumbnailUrl}')
        count += 1



    # Create the full file path by combining the folder path and file name



if __name__ == "__main__":
    pytest.main(["Test_requests_get_diff_prameters.py",  "-v", "--showlocals",   "--tb=short",
                 "--self-contained-html", "--html=reports/Test_requests_get_diff_prameters_report.html"])

    # test_requests_query_parameters()
    # test_requests_query_parameters_2()
    # test_request_get_download()
    # test_requests_get_1()

