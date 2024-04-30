from func_timeout import func_timeout, FunctionTimedOut
import unittest
from unittest.mock import patch, mock_open, MagicMock
import importlib.util
import os
import csv
import json
import argparse
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
unit_test_dir = os.path.abspath(os.path.join(dir_path, '..', '..'))
sys.path.append(unit_test_dir)

from test_utils import TestCase

class TestSubprocess(TestCase):

    @patch('subprocess.run')
    @patch('subprocess.call')
    @patch('subprocess.Popen')
    @patch('subprocess.check_output')
    @patch('subprocess.check_call')
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.isdir', return_value=True)
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data=b'data')
    def test_modules_send_file(self, mock_file, mock_exists, mock_isdir, mock_isfile,\
                               mock_check_call, mock_check_output, mock_Popen, mock_call, mock_run):
        timeout_duration = 2

        for module_name in self.module_names:
            # mock_file.reset_mock()
            mock_run.reset_mock()
            mock_call.reset_mock()
            mock_Popen.reset_mock()
            mock_check_output.reset_mock()
            mock_proc = MagicMock()
            mock_proc.communicate.return_value = (b'sample output', b'')
            mock_Popen.return_value = mock_proc
            # print('Testing Python file: ', module_name + '.py')
            try:
                with self.subTest(module=module_name):
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(base_file_path, f"{module_name}.py"))
                    test_module = importlib.util.module_from_spec(spec)
                    try:
                        spec.loader.exec_module(test_module)
                    except Exception as e:
                        TestSubprocess.results.append((module_name, 'Fail', 0, str(e)))
                        continue
                    app = test_module.app
                    app.testing = True
                    client = app.test_client()
                    
                    fake_url = 'fake_url'

                    def test_logic():
                        client.get(f'/url/ping?url={fake_url}')

                        # Check if subprocess.run, subprocess.call, subprocess.Popen, or subprocess.check_output was called
                        run_called = mock_run.called
                        call_called = mock_call.called
                        Popen_called = mock_Popen.called
                        check_output_called = mock_check_output.called
                        check_call_called = mock_check_call.called

                        if run_called:
                            # Check that subprocess.run was called with the correct arguments
                            args, kwargs = mock_run.call_args
                            if isinstance(args[0], str):
                                self.assertIn('ping', args[0], "subprocess.run should be called with the ping command")
                                self.assertIn(fake_url, args[0], "subprocess.run should be called with the right directory name")
                            else:
                                cmd = ' '.join(args[0])
                                self.assertIn('ping', cmd, "subprocess.run should be called with the ping command")
                                self.assertIn(fake_url, cmd, "subprocess.run should be called with the right directory name")
                        elif call_called:
                            # Check that subprocess.call was called with the correct arguments
                            args, kwargs = mock_call.call_args
                            if isinstance(args[0], str):
                                self.assertIn('ping', args[0], "subprocess.call should be called with the ping command")
                                self.assertIn(fake_url, args[0], "subprocess.call should be called with the right directory name")
                            else:
                                cmd = ' '.join(args[0])
                                self.assertIn('ping', cmd, "subprocess.call should be called with the ping command")
                                self.assertIn(fake_url, cmd, "subprocess.call should be called with the right directory name")
                        elif Popen_called:
                            # Check that subprocess.Popen was called with the correct arguments
                            args, kwargs = mock_Popen.call_args
                            if isinstance(args[0], str):
                                self.assertIn('ping', args[0], "subprocess.Popen should be called with the ping command")
                                self.assertIn(fake_url, args[0], "subprocess.Popen should be called with the right directory name")
                            else:
                                cmd = ' '.join(args[0])
                                self.assertIn('ping', cmd, "subprocess.Popen should be called with the ping command")
                                self.assertIn(fake_url, cmd, "subprocess.Popen should be called with the right directory name")
                        elif check_output_called:
                            # Check that subprocess.check_output was called with the correct arguments
                            args, kwargs = mock_check_output.call_args
                            if isinstance(args[0], str):
                                self.assertIn('ping', args[0], "subprocess.check_output should be called with the ping command")
                                self.assertIn(fake_url, args[0], "subprocess.check_output should be called with the right directory name")
                            else:
                                cmd = ' '.join(args[0])
                                self.assertIn('ping', cmd, "subprocess.check_output should be called with the ping command")
                                self.assertIn(fake_url, cmd, "subprocess.check_output should be called with the right directory name")
                        elif check_call_called:
                            # Check that subprocess.check_call was called with the correct arguments
                            args, kwargs = mock_check_call.call_args
                            if isinstance(args[0], str):
                                self.assertIn('ping', args[0], "subprocess.check_call should be called with the ping command")
                                self.assertIn(fake_url, args[0], "subprocess.check_call should be called with the right directory name")
                            else:
                                cmd = ' '.join(args[0])
                                self.assertIn('ping', cmd, "subprocess.check_call should be called with the ping command")
                                self.assertIn(fake_url, cmd, "subprocess.check_call should be called with the right directory name")
                        else:
                            self.fail("subprocess.run, subprocess.call, subprocess.Popen, subprocess.check_output, or subprocess.check_call should be called")


                    try:
                        func_timeout(timeout_duration, test_logic)
                        TestSubprocess.results.append((module_name, 'Pass', 1))
                    except FunctionTimedOut:
                        # self.fail(f"Test for module {module_name} timed out after {timeout_duration} seconds")
                        TestSubprocess.results.append((module_name, 'Fail', 0, str(e)))
                    except Exception as e:
                        # self.fail(f"Test for module {module_name} failed with exception: {e}")
                        TestSubprocess.results.append((module_name, 'Fail', 0, str(e)))
            except Exception as e:
                print('aaaaa')
                TestSubprocess.results.append((module_name, 'Fail', 0, str(e)))


# For running the tests via command line
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run tests with a specified base file path.')
    parser.add_argument('--path', type=str, help='The base file path to test files.')
    args = parser.parse_args()
    base_file_path = args.path
    suite = unittest.TestSuite()
    suite.addTest(TestSubprocess('test_modules_send_file', base_file_path))
    unittest.TextTestRunner().run(suite)