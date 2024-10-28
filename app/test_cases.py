import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

# Import the type_builtin function from main.py
from main import type_builtin

class TestTypeBuiltin(unittest.TestCase):
    @patch('os.environ', {'PATH': '/usr/bin:/usr/local/bin'})
    @patch('os.path.isfile')
    @patch('os.access')
    def test_type_builtin_found(self, mock_access, mock_isfile):
        mock_isfile.side_effect = lambda path: path in ['/usr/bin/ls', '/usr/local/bin/abcd']
        mock_access.side_effect = lambda path, mode: path in ['/usr/bin/ls', '/usr/local/bin/abcd']

        with patch('sys.stdout', new=StringIO()) as fake_out:
            type_builtin(['ls'])
            self.assertEqual(fake_out.getvalue().strip(), 'ls is /usr/bin/ls')

        with patch('sys.stdout', new=StringIO()) as fake_out:
            type_builtin(['abcd'])
            self.assertEqual(fake_out.getvalue().strip(), 'abcd is /usr/local/bin/abcd')

    @patch('os.environ', {'PATH': '/usr/bin:/usr/local/bin'})
    @patch('os.path.isfile')
    @patch('os.access')
    def test_type_builtin_not_found(self, mock_access, mock_isfile):
        mock_isfile.return_value = False
        mock_access.return_value = False

        with patch('sys.stdout', new=StringIO()) as fake_out:
            type_builtin(['missing_cmd'])
            self.assertEqual(fake_out.getvalue().strip(), 'missing_cmd: not found')

    @patch('os.environ', {'PATH': '/usr/bin:/usr/local/bin'})
    def test_type_builtin_no_args(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            type_builtin([])
            self.assertEqual(fake_out.getvalue().strip(), 'type: missing operand')

if __name__ == '__main__':
    unittest.main()