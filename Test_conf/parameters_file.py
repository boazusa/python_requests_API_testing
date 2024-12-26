
def my_params(API_KEY='', API_KEY_2=''):
    test_parameters = [('sUnRiSe', API_KEY, 200), ('detroit', API_KEY, 200),
                       ('Miami', API_KEY_2, 200), ('FORT Lauderdale', API_KEY, 200),
                       ('Champaign', API_KEY, 200), ('Urbana', API_KEY, 200),
                       ('Tel aViv', API_KEY, 200), ('Lod', API_KEY_2, 200),
                       ('ramla', API_KEY, 200), ('Jerusalem', API_KEY, 200),
                       ('RomE', API_KEY, 200), ('paris', API_KEY_2, 200),
                       ('london', API_KEY, 200), ('lauderhill', API_KEY + 'err', 401),
                       ('london', 'api_key_err', 401), ('paris', 'err' + API_KEY[:-3], 401),
                       ('no_city_err', API_KEY, 404), ('pariserr', API_KEY, 404)]
    return test_parameters
