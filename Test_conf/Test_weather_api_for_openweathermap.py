# https://home.openweathermap.org/api_keys
# https://openweathermap.org/
import pytest
import requests

import parameters_file
import argparse


# A fixture to access the command-line options
@pytest.fixture(scope="module")
def get_api_keys(request):
    KEY = request.config.getoption("--KEY")
    KEY2 = request.config.getoption("--KEY2")
    return [KEY, KEY2]

def my_params():
    test_parameters = [('sUnRiSe', 200), ('detroit', 200),
                       ('Miami', 200), ('FORT Lauderdale', 200),
                       ('Champaign', 200), ('Urbana', 200),
                       ('Tel aViv', 200), ('Lod', 200),
                       ('ramla', 200), ('Jerusalem', 200),
                       ('RomE', 200), ('paris', 200),
                       ('london', 200), ('laauderhill', 404),
                       ('no_city_err', 404), ('pariserr', 404)]
    return test_parameters

@pytest.mark.parametrize("_city, _status_code", my_params())
def test_api_key_parametrize(get_api_keys, _city, _status_code):
    # Example: Using requests to Call a Public API:
    # Calling a public API (OpenWeatherMap)
    API_KEY = get_api_keys[0]  # API_KEY possible err code 401
    city = _city.replace(' ', '%20')  # city  possible err code 404
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    print(url)
    response = requests.get(url)
    print(response.status_code)
    assert response.status_code == _status_code, f"Expected response.status_code 200" \
                                                 f" but got {response.status_code}"

    if response.status_code == 200:
        data = response.json()
        assert 'description' in data['weather'][0]
        assert (data['main']['temp']) - 273.15 < 50
        assert data['name'] == city.replace('%20', ' ').title()
        assert data['base'] == 'stations'
        assert data['visibility'] <= 10000
        assert 'timezone' in data
        if city.replace('%20', ' ').title() in ['Tel aViv'.title(), 'Jerusalem'.title(), 'lod'.title()]:
            assert data['timezone'] == 7200

        print(f"Weather in {city.replace('%20', ' ')}: {data['weather'][0]['description']}")
        print(data)
        print(
            f"Weather in {city.replace('%20', ' ')}: {data['weather'][0]['description']}, temp: {'%.0f' % (data['main']['temp'] - 273.15)} c")
    else:
        assert response.status_code == _status_code
        print(f"Failed to retrieve data. Status code: {response.status_code}")


def test_api_key():
    # Example: Using requests to Call a Public API:
    # Calling a public API (for example, OpenWeatherMap)
    API_KEY = '214adb730e455460b36de542f44a059c'
    # API_KEY = '6e22f9e727115df87ddb05c7b8bd6157'
    # API_KEY = 'YOUR_API_KEY_from_openweathermap.org'
    city = 'Tel Aviv'
    # city = 'Detroit'
    # city = 'Miami'
    # city = 'fort lauderdale'
    # city = 'Lauderhill'

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    print(url.replace(' ', '%20'))
    response = requests.get(url)

    params = {'q': f'{city}', 'appid': f'{API_KEY}'}
    url = f'http://api.openweathermap.org/data/2.5/weather'
    print(url.replace(' ', '%20'))
    response = requests.get(url, params=params)

    assert response.status_code == 200, f"Expected response.status_code 200" \
                                        f" but got {response.status_code}"
    if response.status_code == 200:
        print(response.status_code)
        data = response.json()
        print(f"Weather in {city}: {data['weather'][0]['description']}")
        print(data)
        print(
            f"Weather in {city}: {data['weather'][0]['description']}, temp: {'%.0f' % (data['main']['temp'] - 273.15)} c")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")


# if __name__ == "__main__":
#     pytest.main(['Test_weather_api_for_openweathermap.py::test_api_key_parametrize', '-v',
#                  "--cov=parameters_file", "--cov-report=html",
#                  "--self-contained-html", "--html=reports/test_weather_api_for_openweathermap.html"])
#     test_api_key()
