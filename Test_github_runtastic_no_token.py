#
import os

import pytest
import requests

"""

# GitHub API URL to list files in a specific directory
https://api.github.com/repos/boazusa/runtastic-analysis-boaz/contents/runtastic-activities-analisys-for-desktop

# GitHub project URL
https://github.com/boazusa/runtastic-analysis-boaz/tree/main/runtastic-activities-analisys-for-desktop

# 
https://raw.githubusercontent.com/boazusa/runtastic-analysis-boaz/main/runtastic-activities-analisys-for-desktop/<FILE_NAME>

# URL of the GitHub repository ZIP for the 'main' branch
https://github.com/boazusa/runtastic-analysis-boaz/archive/refs/heads/main.zip
"""


def test_github_list_files_my_runtastic_project():

    # GitHub API URL to list files in a specific directory
    url = 'https://api.github.com/repos/boazusa/runtastic-analysis-boaz/contents/runtastic-activities-analisys-for-desktop'
    # response = requests.get(url)
    response = requests.get(url)

    assert response.status_code == 200
    files_list = response.json()
    for file in files_list:
        assert 'git' in file['_links'] and 'html' in file['_links']
        assert 'name' in file
        assert file['type'] == 'file' or file['type'] == 'dir'

    url = 'https://api.github.com/repos/boazusa/runtastic-analysis-boaz/contents/runtastic-activities-analisys-for-desktop/plots'
    # response = requests.get(url)
    response = requests.get(url)

    # test response headers:
    assert 'date' in response.headers
    assert 'X-GitHub-Request-Id' in response.headers
    assert 'application/json' in response.headers['Content-Type']

    print(response.headers)
    print(response.request.headers)
    assert response.status_code == 200
    files_list = response.json()
    for file in files_list:
        file_name, file_extension = os.path.splitext(file['name'])
        assert file_extension in ['.jpg', '.pdf']
        assert file_extension == '.jpg' or file_extension == '.pdf'

    url = 'https://api.github.com/repos/boazusa/runtastic-analysis-boaz/contents/runtastic-activities-analisys'
    # response = requests.get(url)
    response = requests.get(url)
    assert response.status_code == 404, f"expected status_code 404, but received {response.status_code}"


def test_file_download_from_github():
    FILE_NAME = 'read_runtastic_json.py'
    url = 'https://raw.githubusercontent.com/boazusa/runtastic-analysis-boaz/' \
          'main/runtastic-activities-analisys-for-desktop/' + FILE_NAME

    # Send a GET request to the raw file URL
    response = requests.get(url)

    assert response.status_code == 200

    folder_path = 'downloads'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Create the full file path by combining the folder path and file name
    file_path = os.path.join(folder_path, FILE_NAME)

    with open(file_path, 'wb') as file:
        file.write(response.content)

    # test if file was downloaded successfully
    assert os.path.exists(file_path)

    # remove (delete) file
    os.remove(file_path)
    assert not os.path.exists(file_path)

    # remove (delete) folder
    os.rmdir(folder_path)
    assert not os.path.exists(folder_path)


def test_github_package_was_downloaded():
    # URL of the GitHub repository ZIP for the 'main' branch
    url = 'https://github.com/boazusa/runtastic-analysis-boaz/archive/refs/heads/main.zip'

    # Send a GET request to the URL
    response = requests.get(url)
    assert response.status_code == 200

    folder_path = 'downloads'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Create the full file path by combining the folder path and file name
    file_path = os.path.join(folder_path, 'runtastic-analysis-boaz.zip')

    with open(file_path, 'wb') as f:
        f.write(response.content)

    # # test if file was downloaded successfully
    assert os.path.exists(file_path)

    # remove (delete) file
    os.remove(file_path)
    assert not os.path.exists(file_path)

    # remove (delete) folder
    os.rmdir(folder_path)
    assert not os.path.exists(folder_path)

def test_for_invalid_request_400():
    url = 'https://raw.githubusercontent.com/boazusa/runtastic-analysis-boaz/main/runtastic-activities-analisys-for-desktop/'
    # response = requests.get(url)
    response = requests.get(url)
    assert response.status_code == 400  # Invalid request

def test_for_page_not_found_404():

    url = 'https://api.github.com/repos/boazusa/runtastic-analysis-boaz/contents/runtastic-activities-analisys'
    # response = requests.get(url)
    response = requests.get(url)
    assert response.status_code == 404

if __name__ == "__main__":
    pytest.main(['Test_github_runtastic_no_token.py', '-v', '--showlocals',
                 "--self-contained-html", "--html=reports/Test_github_runtastic_no_token.html"])
    # test_github_list_files_my_runtastic_project()
    test_github_list_files_my_runtastic_project()
    # test_github_package_was_downloaded()
