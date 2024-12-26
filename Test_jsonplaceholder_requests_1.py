import pytest
import requests


def test_jsonplaceholder_get_requests():
    # get
    id = 1
    response = requests.get('https://jsonplaceholder.typicode.com/posts/' + str(id))
    assert response.status_code == 200
    # print('get', response.text)

    rsp_jsn = response.json()
    assert rsp_jsn['id'] == id
    assert rsp_jsn['title'] == "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"
    assert len(rsp_jsn['body']) > 50

    response = requests.get('https://jsonplaceholder.typicode.com/posts/99999')
    assert response.status_code == 404
    print('get err', response.text)


def test_jsonplaceholder_post_requests():
    url = 'https://jsonplaceholder.typicode.com/posts'
    payload = {'title': 'foo', 'body': 'bar', 'userId': 1, 'id': 770}
    response = requests.post(url, json=payload)  # Sends the JSON payload
    assert response.status_code == 201
    print('post', response.text)
    print('post', response.url)

    rsp_jsn = response.json()
    assert rsp_jsn['title'] == payload['title']
    assert rsp_jsn['body'] == payload['body']

    with pytest.raises(Exception):
        assert rsp_jsn['userId'] != payload['userId']

    assert rsp_jsn['id'] != payload['id']


def test_jsonplaceholder_put_requests():
    url = 'https://jsonplaceholder.typicode.com/posts/1'
    payload = {
        'id': 770,
        'title': 'Updated Title',
        'body': 'Updated Body',
        'userId': 11,
        'dummy_field_1': 'dummy_1',
        'dummy_field_2': {'d1': 'dummy_1', 'd2': 'dummy_2'},
        'dummy_field_3': 770
    }
    response = requests.put(url, json=payload)
    assert response.status_code == 200
    print('put', response.text)

    rsp_jsn = response.json()
    assert rsp_jsn['title'] == payload['title']
    assert rsp_jsn['body'] == payload['body']
    assert rsp_jsn['dummy_field_1'] == payload['dummy_field_1']
    assert rsp_jsn['dummy_field_2']['d1'] == payload['dummy_field_2']['d1']
    assert rsp_jsn['dummy_field_2']['d2'] == 'dummy_2'
    assert rsp_jsn['dummy_field_3'] == 770

    with pytest.raises(Exception):
        assert rsp_jsn['userId'] != payload['userId']

    assert rsp_jsn['id'] != payload['id']


def test_jsonplaceholder_patch_requests():
    url = 'https://jsonplaceholder.typicode.com/posts/1'
    payload = {
        'id': 770,
        'title': 'Updated Title',
        'body': 'Updated Body',
        'userId': 111,
        'dummy_field_1': 'dummy_1',
        'dummy_field_2': {'d1': 'dummy_1', 'd2': 'dummy_2'},
        'dummy_field_3': 770
    }
    session = requests.Session()
    session.headers.update({'User-Agent': 'MyApp/770.0', 'Connection': 'keep-test', 'test_1': '12345'})
    response = session.patch(url, json=payload)
    assert response.status_code == 200
    # print('put', response.headers)
    print('put ', response.request.headers)

    rsp_jsn = response.json()
    assert rsp_jsn['title'] == payload['title']
    assert rsp_jsn['body'] == payload['body']
    assert rsp_jsn['dummy_field_1'] == payload['dummy_field_1']
    assert rsp_jsn['dummy_field_2']['d1'] == payload['dummy_field_2']['d1']
    assert rsp_jsn['dummy_field_2']['d2'] == 'dummy_2'
    assert rsp_jsn['dummy_field_3'] == 770

    with pytest.raises(Exception):
        assert rsp_jsn['userId'] != payload['userId']

    assert rsp_jsn['id'] == payload['id']

    '''
    # headers update
    session.headers.update({'User-Agent': 'MyApp/770.0', 'Connection': 'keep-keep'})
    response = session.get(url)
    print('put2', response.request.headers)
    session.headers.update({'test_2': '67890'})
    response = session.get(url)
    print('put3', response.request.headers)
    '''


def test_jsonplaceholder_delete_requests():
    # delete

    url = 'https://jsonplaceholder.typicode.com/posts/1'
    payload = {
        'id': 770,
        'title': 'Updated Title',
        'body': 'Updated Body',
        'userId': 111,
        'dummy_field_1': 'dummy_1',
        'dummy_field_2': {'d1': 'dummy_1', 'd2': 'dummy_2'},
        'dummy_field_3': 770
    }
    session = requests.Session()
    url = 'https://jsonplaceholder.typicode.com/posts/1'

    response = session.delete(url)

    assert response.status_code == 200
    assert response.text == '{}'
    assert response.json() == {}
    assert response.request.headers['Content-Length'] == '0'
    assert response.request.headers['User-Agent'] == 'python-requests/2.32.3'
    assert response.headers['Content-Type'] == 'application/json; charset=utf-8'
    # print('delete', response.text, type(response.json()))
    # print('1', response.request.headers)
    # print('1', response.headers)

    d1 = {'test': 'test'}

    def dict_chr_len(_d):
        d_len = 0
        for key, val in _d.items():
            d_len += 8 + len(key) + len(val)
        return str(d_len)

    response = session.delete(url, json=d1)

    assert response.status_code == 200
    assert response.text == '{}'
    assert response.json() == {}
    assert response.request.headers['Content-Length'] == dict_chr_len(d1)
    assert response.request.headers['User-Agent'] == 'python-requests/2.32.3'
    assert response.headers['Content-Type'] == 'application/json; charset=utf-8'
    # print('delete', response.text, type(response.json()))
    # print('2', response.request.headers)
    # print('2', response.headers)


def test_jsonplaceholder_header_updates_requests():
    session = requests.Session()
    headers = {'User-Agent': 'MyApp/999.0'}
    headers_1 = {'User-Agent': 'MyApp/999.0', 'test_1': '12345'}
    session.headers.update(headers_1)
    # Send a request using the session
    response = session.get('https://jsonplaceholder.typicode.com/posts/1') # , headers=headers_1)
    assert response.status_code == 200
    # print(response.json())
    # print(response.request.headers)
    assert response.request.headers['test_1'] == headers_1['test_1']
    assert response.request.headers['User-Agent'] == 'MyApp/999.0'
    #
    headers_2 = {'User-Agent': 'MyApp/770.0', 'Connection': 'keep--test', 'test_1': '54321', 'test_2': '770_770'}
    session.headers.update(headers_2)
    response = session.get('https://jsonplaceholder.typicode.com/posts/1')
    assert response.status_code == 200
    # print(response.json())
    # print(response.request.headers)
    assert response.request.headers['test_1'] != headers_1['test_1']
    assert response.request.headers['User-Agent'] == 'MyApp/770.0'


if __name__ == "__main__":
    # pytest.main(["Test_jsonplaceholder_requests_1.py",  "-v", "--showlocals",
    #              "--self-contained-html", "--html=reports/Test_jsonplaceholder_requests_1_report.html"])
    #
    test_jsonplaceholder_post_requests()
    # test_jsonplaceholder_patch_requests()
    # test_jsonplaceholder_delete_requests()





