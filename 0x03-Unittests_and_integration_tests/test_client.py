import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    """Tests for the GithubOrgClient class."""

    @parameterized.expand([
        ('google'),
        ('abc'),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Tests that GithubOrgClient.org returns the correct value
        and that get_json is called once.
        """
        # Configure the mock to return a predefined payload
        # This will be returned when get_json is called
        mock_get_json.return_value = {"login": org_name}

        # Create an instance of the class
        client = GithubOrgClient(org_name)

        # Call the method being tested
        result = client.org()

        # Assertions
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, {"login": org_name})