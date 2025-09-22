# Unit vs. Integration
**Unit Tests:** These tests focus on a single, isolated piece of code—a `unit`. The goal is to ensure each small component of your app is bug-free before it's combined with other components.

Think of `unittest` as a built-in "test harness" for Python. It's a framework that gives you a structured way to write and run automated tests for your code.

Here's a simple breakdown of how it works and the key components:

**Test Case:** The core of unittest is the concept of a test case. A test case is a single, isolated scenario that tests a specific behavior of your code. In our example, test_add_positive_numbers is a test case.

**Test Suite:** A group of related test cases is called a test suite. This is usually a class that inherits from unittest.TestCase. This class provides all the methods you need to write tests.

**Assertions:** Inside your test case, you'll use assertion methods to check if a condition is true. An assertion is just a statement that "asserts" or claims something about your code. For example, assertEqual(a, b) asserts that a is equal to b. If the assertion is false, the test fails.

**Test Runner:** This is the tool that finds your test files, runs all the test cases, and reports the results (pass or fail). When you run `python -m unittest test_add.py`, you're telling Python to use its built-in test runner to find and run the tests in that file.

**Integration Tests:** These tests check how multiple pieces of code work together.

**Assertions (assert):** used the assert keyword to check if a condition is true, such as assert len(all_list) == 3. This is a much cleaner way to write tests compared to older frameworks.

### PYTEST FRAMEWORK  
`pytest` is another popular and often more concise testing framework in Python and easier to use.  

#### Testing parterns
1. **Parametrization** is to test the same function with many different inputs without having to write a separate test function for each one. This makes your test code much cleaner and more efficient.

e.g You have a function to get the sum of two numbers, pssible tests would be check for additins f floats, negatives , psitives e.t.c. So intead of: 

```python
def test_add_positive_numbers(self):
    self.assertEqual(add(2, 3), 5)

def test_add_negative_numbers(self):
    self.assertEqual(add(-2, -3), -5)

def test_add_mixed_numbers(self):
    self.assertEqual(add(5, -3), 2)

```
We get:

```python
import pytest
from add import add

@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),          # Positive numbers
    (-1, -1, -2),       # Negative numbers
    (2.5, 3.5, 6.0),    # Floats
    (0, 0, 0),          # Zeros
])
def test_add_multiple_cases(a, b, expected):
    assert add(a, b) == expected
```
The `@pytest.mark.parametrize decorator` is one of pytest's most powerful features. It lets you run a single test function multiple times with different inputs and expected outputs. Think of it as a way to create a "data-driven" test. Instead of writing a separate test for each scenario, you provide a list of data sets, and pytest handles the rest.

2.**Mocking** - the process of simulating the behavior of a real object or function that your code interacts with, but which you don't want to actually use in a test. You use a "mock" object instead of the real one e.g API calls, database access. e.g A call t a weather API
```python
import requests

def get_weather(city):
    """Fetches weather data from a fake API."""
    url = f"https://api.weather.com/{city}"
    response = requests.get(url)
    response.raise_for_status() # Raises an exception for bad responses
    return response.json()
```
A sample mock becomes

```python
import unittest
import requests
from unittest import mock
from weather import get_weather

class weatherApi_test(unittest.TestCase):

    @mock.patch('weather.requests.get')
    def test_get_weather_success(self, mock_get):
        mock_json = {
            "city": "Nairobi",
            "temperature": "25C",
            "condition": "Sunny"
        }
        # 2. Configure the mock response object
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_json

        # 3. Tell our mock_get object to return this mock_response
        mock_get.return_value = mock_response

        # 4. Now, call our function and check the result
        result = get_weather("Nairobi")

        # 5. Assert that the result is what we expected
        self.assertEqual(result, mock_json)

    @mock.patch('weather.requests.get')
    def test_get_weather_connection_error(self, mock_get):
        # Tell the mock to raise a ConnectionError when it's called
        mock_get.side_effect = requests.exceptions.ConnectionError

        # We use a context manager to check if our function raises the expected exception
        with self.assertRaises(requests.exceptions.ConnectionError):
            get_weather("InvalidCity")
```

3. **Fixtures (@pytest.fixture):** Fixtures are used to set up a specific, controlled environment for your tests. They are perfect for providing a clean starting state, like creating a Task object. They help you avoid writing repetitive setup code However not every test needs a fixture. For instance the user:
```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def update_email(self, new_email):
        self.email = new_email
```
Uses the fixture:  

```python
import pytest
from user import User

@pytest.fixture
def user_fixture():
    return User("Test User", "test@example.com")

def test_user_login(user_fixture):
    assert user_fixture.name == "Test User"
    assert user_fixture.email == "test@example.com"

def test_user_email_update(user_fixture):
    user_fixture.update_email("test@example.com")
    assert user_fixture.email == "test@example.com"
```

**Global State Management:** It is important it is to manage global variables We used tasks.clear() to ensure each test started with a clean, empty list, which makes your tests more reliable and repeatable.