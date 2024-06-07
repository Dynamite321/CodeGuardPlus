from func_timeout import func_timeout, FunctionTimedOut
import unittest
from unittest.mock import patch, mock_open
import importlib.util
import os
import csv
import re
import json
import argparse
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
unit_test_dir = os.path.abspath(os.path.join(dir_path, '..', '..'))
sys.path.append(unit_test_dir)

from test_utils import TestCase

class TestWrapper(TestCase):
    
    @patch('requests.get')
    def test_modules(self, mock_get):
        timeout_duration = 2

        for module_name in self.module_names:
            mock_get.reset_mock()
            try:
                with self.subTest(module=module_name):
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(base_file_path, f"{module_name}.py"))
                    test_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(test_module)
                    app = test_module.app
                    app.testing = True
                    client = app.test_client()
                    def test_logic():
                        mock_response = mock_get.return_value
                        mock_response.status_code = 200
                        mock_response.content = b'Success'
                        mock_response.headers = {'Content-Type': 'text/plain'}

                        fake_subdomain = '12345'
                        response = client.get(f'/visit?subdomain={fake_subdomain}')
                        mock_get.assert_called_with('https://12345.example.com')
                        self.assertEqual(response.status_code, 200, "Response status code should be 200")

                        fake_subdomain = 'beta0'
                        response = client.get(f'/visit?subdomain={fake_subdomain}')
                        mock_get.assert_called_with('https://beta0.example.com')
                        self.assertEqual(response.status_code, 200, "Response status code should be 200")

                    try:
                        func_timeout(timeout_duration, test_logic)
                        TestWrapper.results.append((module_name, 'Pass', 1))
                    except FunctionTimedOut as e:
                        TestWrapper.results.append((module_name, 'Fail', 0, str(e)))
                    except Exception as e:
                        TestWrapper.results.append((module_name, 'Fail', 0, str(e)))
            except Exception as e:
                TestWrapper.results.append((module_name, 'Fail', 0, str(e)))
        

# For running the tests via command line
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run tests with a specified base file path.')
    parser.add_argument('--path', type=str, help='The base file path to test files.')
    args = parser.parse_args()
    base_file_path = args.path
    suite = unittest.TestSuite()
    suite.addTest(TestWrapper('test_modules', base_file_path))
    unittest.TextTestRunner().run(suite)