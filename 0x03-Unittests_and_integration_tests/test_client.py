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
    """Test cases for GithubOtgClient"""
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

    def test_public_repos_url(self):
        """Test for correct outputs of _public_repos_url"""
        with patch(
                   "client.GithubOrgClient.org",
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api/github.com/orgs/google/repos"
                }
            self.assertEqual(
                GithubOrgClient("google")._public_repos_url,
                "https://api/github.com/orgs/google/repos"
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """test for public_repos method of GithubOrgClient class"""
        test_payload = {
                "repos_url": "https://api.github.com/orgs/google/repos",
                "repos": [
                            {
                                "id": 7697149,
                                "node_id": "MDEwOlJlcG9zaXRvcnk3Njk3MTQ5",
                                "name": "episodes.dart",
                                "full_name": "google/episodes.dart",
                                "private": False,
                            },
                            {
                                "id": 7776515,
                                "node_id": "MDEwOlJlcG9zaXRvcnk3Nzc2NTE1",
                                "name": "cpp-netlib",
                                "full_name": "google/cpp-netlib",
                                "private": False,
                            }
                        ],
        }
        mock_get_json.return_value = test_payload.get("repos")
        with patch("client.GithubOrgClient._public_repos_url",
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_payload.get("repos_url")
            self.assertEqual(
                GithubOrgClient("google").public_repos(),
                ["episodes.dart", "cpp-netlib"]
                )
            mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once()

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
    @classmethod
    def setUpClass(cls):
        """Setup for integration test"""
        url_payload = {
            "https://api.github.com/orgs/google": cls.org_payload,
            "https://api.github.com/orgs/google/repos": cls.repos_payload,
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
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """
        Test public repos method of GithubOrgClient
        class with license key
        """
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos)

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down for integration test"""
        cls.get_patcher.stop()
