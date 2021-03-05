import unittest
from os.path import dirname, join, realpath
import catz.commands
import catz.commands.util
from rich.console import Console
from click.testing import CliRunner


TESTS_ROOT = dirname(realpath(__file__))

class TestWhenExecutingDiff(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    def test_it_should_fail_when_file_not_found(self):
        result = self.runner.invoke(
            catz.commands.diff, [join(TESTS_ROOT,'files/yaml.yml'), join(TESTS_ROOT,'notfound.json')], obj=Console())
        self.assertEqual(result.exit_code, 1)
        assert 'No such file or directory:' in result.output

    def test_it_should_fail_when_missing_arg(self):
        result = self.runner.invoke(
            catz.commands.diff, [join(TESTS_ROOT, 'files/yaml.yml')], obj=Console())
        self.assertEqual(result.exit_code, 2)
        assert 'Error: Missing argument \'DIFF\'.' in result.output

    def test_it_should_display_correct_diff(self):
        result = self.runner.invoke(
            catz.commands.diff, [join(TESTS_ROOT,'files/yaml.yml'), join(TESTS_ROOT, 'files/yaml_diff.yml')], obj=Console())
        print(result.output)
        self.assertEqual(result.exit_code, 0)
        assert '-   - test+   - diff' in result.output

    def tearDown(self):
        self.runner = None

if __name__ == '__main__':
    unittest.main()
