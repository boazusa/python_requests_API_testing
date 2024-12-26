# conftest.py
def pytest_addoption(parser):
    parser.addoption(
        "--KEY", action="store", default="default_value1", help="First input parameter"
    )
    parser.addoption(
        "--KEY2", action="store", default="default_value2", help="Second input parameter"
    )
