#!/usr/bin/env python3
"""
test_utils
"""
from parameterized import parameterized
from typing import (
    Callable,
    Dict,
    Sequence,
)
import unittest
from unittest.mock import patch, MagicMock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Class with test cases for util.access_nested_map"""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Dict, path: Sequence,
                               expected_output: str) -> None:
        """Test right input cases"""
        real_output = access_nested_map(nested_map, path)
        self.assertEqual(real_output, expected_output)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b")
    ])
    def test_access_nested_map_exception(self, nested_map: Dict,
                                         path: Sequence,
                                         expected_exception: str) -> None:
        """Test exception cases"""
        with self.assertRaises(KeyError) as err:
            access_nested_map(nested_map, path)
            self.assertEqual(expected_exception, err.exception)


class TestGetJson(unittest.TestCase):
    """Test suites for utils.get_json function"""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch("utils.requests")
    def test_get_json(self, test_url: str, test_payload: Dict,
                      mock_requests: MagicMock) -> None:
        """Test cases for correct outputs"""
        # create an instance of Mock
        mock_response = MagicMock()
        # give it a json method with test_payload as the return value
        mock_response.json.return_value = test_payload
        # patched requests.get returns the Mock instance
        mock_requests.get.return_value = mock_response

        self.assertEqual(get_json(test_url), test_payload)
        # check that mocked get is called once
        mock_requests.get.assert_called_once()


class TestMemoize(unittest.TestCase):
    """Test suites for utils.memoize function"""
    def test_memoize(self) -> None:
        """Test cases for memoize"""
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self) -> Callable:
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock_a:
            test = TestClass()
            test.a_property
            test.a_property
            mock_a.assert_called_once()
