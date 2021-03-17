# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
"parser.py tests"
import unittest

from . import errors
from . import parser


class EnvironmentSubstitutionParserTests(unittest.TestCase):
    def test_simple1(self) -> None:
        uut = parser.EnvironmentSubstitutionParser("$FOO")
        result = uut.expand({"FOO": "foo"})
        self.assertEqual("foo", result)

    def test_simple2(self) -> None:
        uut = parser.EnvironmentSubstitutionParser("$FOO123")
        result = uut.expand({"FOO123": "foo"})
        self.assertEqual("foo", result)

    def test_double_quote1(self) -> None:
        uut = parser.EnvironmentSubstitutionParser("Hello '\"'$Name'\"'.")
        result = uut.expand({"Name": "Jane"})
        self.assertEqual('Hello "Jane".', result)

    def test_single_quote1(self) -> None:
        uut = parser.EnvironmentSubstitutionParser('Hello "\'"$Name"\'".')
        result = uut.expand({"Name": "Fred"})
        self.assertEqual("Hello 'Fred'.", result)

    def test_special1(self) -> None:
        uut = parser.EnvironmentSubstitutionParser("$$Foo")
        self.assertRaises(errors.UnsupportedVariableError, uut.expand, {})

    def test_nomatch1(self) -> None:
        uut1 = parser.EnvironmentSubstitutionParser("$FOO")
        self.assertRaises(errors.NoMatchingSubstitutionError, uut1.expand, {})
        uut2 = parser.EnvironmentSubstitutionParser("${FOO}")
        self.assertRaises(errors.NoMatchingSubstitutionError, uut2.expand, {})
        uut3 = parser.EnvironmentSubstitutionParser("$FOO-bar")
        self.assertRaises(errors.NoMatchingSubstitutionError, uut3.expand, {})


if __name__ == "__main__":
    unittest.main()
