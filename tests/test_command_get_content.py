import unittest
from os.path import dirname, join, realpath
import catz.commands
import catz.commands.util
from rich.console import Console
from click.testing import CliRunner


TESTS_ROOT = dirname(realpath(__file__))


class TestWhenExecutingTheBaseCommand(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    def test_it_should_load(self):
        result = self.runner.invoke(catz.commands.get)
        self.assertEqual(result.exit_code, 0)

    def test_it_should_display_help_with_no_params(self):
        result = self.runner.invoke(catz.commands.get)
        self.assertEqual(result.exit_code, 0)
        assert 'Perform syntax highlighting on raw text from a local file' in result.output

    def tearDown(self):
        self.runner = None


class TestWhenExecutingWithAFileAsInput(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    def test_it_should_fail_when_file_not_found(self):
        result = self.runner.invoke(
            catz.commands.get, ['./notfound.json'], obj=Console())
        self.assertEqual(result.exit_code, 2)
        assert 'Error: Invalid value for' in result.output

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

class TestWhenHighlightingLines(unittest.TestCase):

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

    def test_highlight_fails_when_range_contains_more_than_two_values(self):
        result = self.runner.invoke(catz.commands.get, [join(
            TESTS_ROOT, 'files', 'json_utf8.json'), '--highlight', '10-11-12'], obj=Console())
        self.assertEqual(result.output.strip(), 'Error: Invalid value for --highlight / -hl: Could not convert 10-11-12 to a valid range')


if __name__ == '__main__':
    unittest.main()
