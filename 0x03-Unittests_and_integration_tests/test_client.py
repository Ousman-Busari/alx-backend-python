#!/usr/bin/env python3
"""
Test suit for client module
"""
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class
from requests import HTTPError
from typing import Dict
import unittest
from unittest.mock import (
    MagicMock,
    Mock,
    patch,
    PropertyMock
)


class TestGithubOrgClient(unittest.TestCase):
    """Test suites for GithubOtgClient"""
    @parameterized.expand([
        ("google"),
        ("abc"),
    ])
    @patch("client.get_json")
    def test_org(self, org_name: str, mocked_get_json: MagicMock) -> None:
        """test for org method correct outputs"""
        url = "https://api.github.com/orgs/{org}".format(org=org_name)
        test = GithubOrgClient(org_name)
        test.org
        mocked_get_json.assert_called_once_with(url)

    # @parameterized.expand([
    #     ("random_org", {"repos_url": "https://random_repos.com"})
    # ])
    def test_public_respos_url(self):
        """Test for correct outputs of _public_repos_url"""
        with patch("client.GithubOrgClient.org",
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://random_repos.com"}
            response = GithubOrgClient("google")._public_repos_url
            self.assertEqual(response, "https://random_repos.com")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo: Dict, license_key: str,
                         expected_result: bool) -> None:
        actual_result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(actual_result, expected_result)


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test: fixtures"""
    test = GithubOrgClient("google")

    @classmethod
    def setUpClass(cls):
        """Setup for integration test"""
        url_payload = {
            "https://api.github.com/orgs/google": cls.org_payload,
            "https://api.github.com/orgs/google/repo": cls.repos_payload,
        }

        def get_payload(url) -> Dict:
            """Get url payload"""
            if url in url_payload:
                return Mock(**{"json.return_value": url_payload[url]})
            return HTTPError

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.mocked_get = cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """Test public repos method of GithubOrgClient class"""
        # test = GithubOrgClient("google")
        self.assertEqual(self.test.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """
        Test public repos method of GithubOrgClient
        class with license key
        """
        # test = GithubOrgClient("google")
        self.assertEqual(self.test.public_repos(license="apache-2.0"),
                         self.apache2_repos)

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down for integration test"""
        cls.get_patcher.stop()
