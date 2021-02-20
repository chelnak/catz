import unittest
import urllib
from unittest.mock import patch, MagicMock
from os.path import dirname, join, realpath
import catz.commands
import catz.commands.command_helpers
from rich.console import Console
from click.testing import CliRunner
import warnings


TESTS_ROOT = dirname(realpath(__file__))

VALID_URL = 'https://raw.githubusercontent.com/chelnak/catz/main/README.md'
INVALID_URL = f'{VALID_URL}x'

MOCK_HTTP_RESPONSE = '{"test": "file"}'

MOCK_CATZ_RESPONSE = '1 {"test": "file"}'


class TestGetContentCommand(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    def test_it_should_load(self):
        result = self.runner.invoke(catz.commands.get)
        self.assertEqual(result.exit_code, 0)

    def test_it_should_display_help_with_no_params(self):
        result = self.runner.invoke(catz.commands.get)
        self.assertEqual(result.exit_code, 0)
        assert 'Perform syntax highlighting on raw text from a local file or a url' in result.output

    def tearDown(self):
        self.runner = None


class TestGetContentFile(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    def test_it_should_fail_when_file_not_found(self):
        result = self.runner.invoke(
            catz.commands.get, ['./notfound.json'], obj=Console())
        self.assertEqual(result.exit_code, 1)
        assert 'No such file or directory:' in result.output

    def test_it_should_return_expected_content(self):
        result = self.runner.invoke(catz.commands.get, [join(
            TESTS_ROOT, 'files', 'json_utf8.json')], obj=Console())
        self.assertEqual(result.exit_code, 0)

    def test_it_should_handle_alternative_encoding(self):
        result = self.runner.invoke(catz.commands.get, [join(
            TESTS_ROOT, 'files', 'json_utf16le.json')], obj=Console())
        self.assertEqual(result.exit_code, 0)

    def tearDown(self):
        self.runner = None


class TestGetContentUrl(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    @patch('catz.commands.command_helpers.get_content_from_url')
    def test_it_should_fail_on_http_error(self, mock_urllib):

        mock = mock_urllib.return_value
        mock.side_effect = urllib.error.HTTPError

        result = self.runner.invoke(
            catz.commands.get, [INVALID_URL], obj=Console())
        self.assertEqual(result.exit_code, 1)
        assert 'Error: HTTP Error 404: Not Found' in result.output

    @patch('catz.commands.command_helpers.urllib.request.urlopen')
    def test_it_should_fail_when_invalid_protocol(self, mock_urllib):

        url = VALID_URL.replace('https', 'ftp')
        result = self.runner.invoke(catz.commands.get, [url], obj=Console())
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(result.output.strip(), 'Error: ftp is not a valid http protocol.')

    @patch('catz.commands.command_helpers.urllib.request.urlopen')
    def test_it_should_return_expected_content(self, mock_urlopen):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = bytes(MOCK_HTTP_RESPONSE, 'utf-8')
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm

        result = self.runner.invoke(
            catz.commands.get, [VALID_URL], obj=Console())
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.strip(), MOCK_CATZ_RESPONSE)

    def tearDown(self):
        self.runner = None


class TestLineHighlighting(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    def test_highlight_accepts_a_single_value(self):
        result = self.runner.invoke(catz.commands.get, [join(
            TESTS_ROOT, 'files', 'json_utf8.json'), '--highlight', '1'], obj=Console())

        self.assertIn('❱ 1', result.output)
        self.assertEqual(result.exit_code, 0)

    def test_highlight_accepts_a_csv_of_values(self):
        result = self.runner.invoke(catz.commands.get, [join(
            TESTS_ROOT, 'files', 'json_utf8.json'), '--highlight', '1,2,3'], obj=Console())
        print(result.output)
        self.assertIn('❱ 1', result.output)
        self.assertIn('❱ 2', result.output)
        self.assertIn('❱ 3', result.output)
        self.assertEqual(result.exit_code, 0)

    def test_highlight_fails_for_invalid_input(self):
        result = self.runner.invoke(catz.commands.get, [join(
            TESTS_ROOT, 'files', 'json_utf8.json'), '--highlight', '1x'], obj=Console())
        self.assertEqual(result.output.strip(), 'Error: Invalid value for --highlight / -hl: invalid literal for int() with base 10: \'1x\' is not a valid integer range')

    def test_highlight_fails_for_invalid_range_input(self):
        result = self.runner.invoke(catz.commands.get, [join(
            TESTS_ROOT, 'files', 'json_utf8.json'), '--highlight', '1-z'], obj=Console())
        self.assertEqual(result.output.strip(), 'Error: Invalid value for --highlight / -hl: invalid literal for int() with base 10: \'z\' is not a valid integer range')

    def test_higlight_accepts_a_range_of_values(self):
        result = self.runner.invoke(catz.commands.get, [join(
            TESTS_ROOT, 'files', 'json_utf8.json'), '--highlight', '1-10'], obj=Console())
        self.assertEqual(result.exit_code, 0)

    def test_highlight_fails_when_range_position_0_is_greater_than_1(self):
        result = self.runner.invoke(catz.commands.get, [join(
            TESTS_ROOT, 'files', 'json_utf8.json'), '--highlight', '10-1'], obj=Console())
        self.assertEqual(result.output.strip(), 'Error: Invalid value for --highlight / -hl: 10 is greater than 1')


if __name__ == '__main__':
    unittest.main()
