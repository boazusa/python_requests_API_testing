# test_example.py
import pytest

# Fixture to access the command-line options
@pytest.fixture
def get_params(request):
    param1 = request.config.getoption("--KEY")
    param2 = request.config.getoption("--KEY2")
    return param1, param2

# Helper function to return parameters dynamically
def dynamic_params(get_params):
    KEY1, KEY2 = get_params
    return [(KEY1, KEY2)]  # Return as a list of tuples

# Parametrize using the helper function that fetches parameters dynamically
@pytest.mark.parametrize("param1, param2", dynamic_params(("value1", "value2")))  # Or use get_params fixture here directly
def test_with_dynamic_params(param1, param2):
    print(f"Received PARAM1: {param1}")
    print(f"Received PARAM2: {param2}")
    assert param1 == "value1"
    assert param2 == "value2"
