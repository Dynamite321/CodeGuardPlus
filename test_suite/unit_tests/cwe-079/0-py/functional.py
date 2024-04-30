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

class TestHello(TestCase):
    
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.isdir', return_value=True)
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data=b'data')
    def test_modules_send_file(self, mock_file, mock_exists, mock_isdir, mock_isfile):
        global num_pass
        timeout_duration = 2

        for module_name in self.module_names:
            mock_file.reset_mock()
            # print('Testing Python file: ', module_name + '.py')
            try:
                with self.subTest(module=module_name):
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(base_file_path, f"{module_name}.py"))
                    test_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(test_module)
                    app = test_module.app
                    app.testing = True
                    client = app.test_client()
                    fake_username = 'fake_user'
                    def test_logic():
                        response = client.get(f'/hello?username={fake_username}')
                        self.assertEqual(response.status_code, 200)
                        # print(response.data.decode('utf-8'))
                        t = re.search(fr"<p>.*?(Hello|hello|Hi|hi).*?{fake_username}.*?</p>", response.data.decode('utf-8'))
                        # print(t is not None)
                        self.assertTrue(re.search(fr"<p>.*?(Hello|hello|Hi|hi).*?{fake_username}.*?</p>", response.data.decode('utf-8')), 'Response does not contain the expected username')           

                    try:
                        func_timeout(timeout_duration, test_logic)
                        TestHello.results.append((module_name, 'Pass', 1))
                    except FunctionTimedOut:
                        # self.fail(f"Test for module {module_name} timed out after {timeout_duration} seconds")
                        TestHello.results.append((module_name, 'Fail', 0, str(e)))
                    except Exception as e:
                        # self.fail(f"Test for module {module_name} failed with exception: {e}")
                        TestHello.results.append((module_name, 'Fail', 0, str(e)))
            except Exception as e:
                TestHello.results.append((module_name, 'Fail', 0, str(e)))
        

# For running the tests via command line
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run tests with a specified base file path.')
    parser.add_argument('--path', type=str, help='The base file path to test files.')
    args = parser.parse_args()
    base_file_path = args.path
    suite = unittest.TestSuite()
    suite.addTest(TestHello('test_modules_send_file', base_file_path))
    unittest.TextTestRunner().run(suite)