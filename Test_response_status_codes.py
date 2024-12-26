import pytest
import requests


def test_response_status_code():
    # get
    response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
    assert response.status_code == 200
    print('get', response.text)

    response = requests.get('https://jsonplaceholder.typicode.com/posts/99999')
    assert response.status_code == 404
    print('get err', response.text)

    # post
    url = 'https://jsonplaceholder.typicode.com/posts'
    payload = {'title': 'foo', 'body': 'bar', 'userId': 1}
    response = requests.post(url, json=payload)  # Sends the JSON payload
    assert response.status_code == 201
    print('post', response.text)

    # put
    url = 'https://jsonplaceholder.typicode.com/posts/1'
    payload = {
        'id': 770,
        'title': 'Updated Title',
        'body': 'Updated Body',
        'userId': 11,
        'zzz': 'bbb'
    }
    response = requests.put(url, json =payload)
    assert response.status_code == 200
    print('put', response.text)

    # patch
    url = 'https://jsonplaceholder.typicode.com/posts/1'
    payload = {
        'id': 770,
        'title': 'Updated Title',
        'body': 'Updated Body',
        'userId': 101,
        'ttt': 'aaa'
    }
    response = requests.patch(url, json=payload)
    assert response.status_code == 200
    print('patch', response.text)

    # delete
    url = 'https://jsonplaceholder.typicode.com/posts/1'
    response = requests.delete(url)
    assert response.status_code == 200
    print('delete', response.text)



if __name__ == "__main__":
    pytest.main(['Test_response_status_codes.py::test_response_status_code', '-v'])
    test_response_status_code()