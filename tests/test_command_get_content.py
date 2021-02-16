import unittest
import responses
from os.path import dirname, join, realpath
from catz.commands import get_content
from click.testing import CliRunner
import warnings


TESTS_ROOT = dirname(realpath(__file__))
RUNNER = CliRunner()

VALID_URL = 'https://raw.githubusercontent.com/chelnak/catz/main/README.md'
INVALID_URL = f'{VALID_URL}x'

MOCK_HTTP_RESPONSE = '{"test": "file"}'

MOCK_CATZ_RESPONSE = '1 "{\\"test\\": \\"file\\"}"'


class TestGetContent(unittest.TestCase):

    def test_it_should_load(self):
        result = RUNNER.invoke(get_content.get)
        self.assertEqual(result.exit_code, 0)

    def test_it_should_display_help_with_no_params(self):
        result = RUNNER.invoke(get_content.get)
        self.assertEqual(result.exit_code, 0)
        assert 'Perform syntax highlighting on raw text from a local file or a url' in result.output


class TestGetContentFile(unittest.TestCase):

    def test_it_should_fail_when_file_not_found(self):
        result = RUNNER.invoke(get_content.get, ['./notfound.json'])
        self.assertEqual(result.exit_code, 1)
        assert 'FileNotFound' in result.output

    def test_it_should_return_expected_content(self):
        result = RUNNER.invoke(get_content.get, [join(
            TESTS_ROOT, 'files', 'json_utf8.json')])
        self.assertEqual(result.exit_code, 0)

    def test_it_should_handle_alternative_encoding(self):
        result = RUNNER.invoke(get_content.get, [join(
            TESTS_ROOT, 'files', 'json_utf16le.json')])
        self.assertEqual(result.exit_code, 0)


class TestGetContentUrl(unittest.TestCase):

    @responses.activate
    def test_it_should_fail_on_http_error(self):
        responses.add(responses.GET, INVALID_URL, status=404)

        result = RUNNER.invoke(get_content.get, [INVALID_URL])
        self.assertEqual(result.exit_code, 1)
        assert f'Error: 404 Client Error: Not Found for url: {INVALID_URL}' in result.output

    def test_it_should_fail_when_invalid_protocol(self):
        url = VALID_URL.replace('https', 'ftp')
        result = RUNNER.invoke(get_content.get, [url])
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(result.output.strip(), 'Error: ftp is not a valid http protocol.')

    @responses.activate
    def test_it_should_return_expected_content(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        responses.add(responses.GET, VALID_URL,
                      json=MOCK_HTTP_RESPONSE, status=200)

        result = RUNNER.invoke(get_content.get, [VALID_URL])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.strip(), MOCK_CATZ_RESPONSE)


if __name__ == '__main__':
    unittest.main()
