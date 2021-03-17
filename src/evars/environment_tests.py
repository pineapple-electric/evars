# pylint: disable=missing-function-docstring
"environment.py tests"
import io
import tempfile
import unittest

from . import environment
from . import errors


simple1 = io.StringIO("FOO=bar\n")
simple1_expected = {"FOO": "bar"}

simple2 = io.StringIO("FOO=foo\nBAR=bar\nBAZ=baz\n")
simple2_expected = {"FOO": "foo", "BAR": "bar", "BAZ": "baz"}

var1 = io.StringIO(
    """FOO=foo
FOOBAR1=${FOO}bar1
FOOBAR2="$FOO"bar2
"""
)
var1_expected = {
    "FOO": "foo",
    "FOOBAR1": "foobar1",
    "FOOBAR2": "foobar2",
}

var2 = io.StringIO(
    """FOO='foo'
FOOBAR1='$FOO'bar1
FOOBAR2="$FOO""foo"bar2
"""
)
var2_expected = {
    "FOO": "foo",
    "FOOBAR1": "$FOObar1",
    "FOOBAR2": "foofoobar2",
}

invalid1 = io.StringIO("Foo Bar=Baz\n")


class EnvironmentTests(unittest.TestCase):
    "Tests for environment.py"

    def setUp(self) -> None:
        simple1.seek(0)
        simple2.seek(0)
        var1.seek(0)
        var2.seek(0)

    def test_dict(self) -> None:
        uut = environment.Environment()
        self.assertEqual({}, uut)

    def test_source1(self) -> None:
        uut = environment.Environment()
        uut.source(simple1)
        self.assertEqual(simple1_expected, uut)

    def test_source2(self) -> None:
        uut = environment.Environment()
        uut.source(simple1)
        self.assertEqual(simple1_expected, uut)
        uut.source(simple2)
        # We have not defined the overwrite_callback.
        expected = simple2_expected.copy()
        expected["FOO"] = "bar"
        self.assertEqual(expected, uut)

    def test_source3(self) -> None:
        uut = environment.Environment()
        uut.source(simple1)
        self.assertEqual(simple1_expected, uut)
        callback = lambda x, y, z: environment.RetainThe.FUTURE_VALUE
        uut.source(simple2, overwrite_callback=callback)
        self.assertEqual(simple2_expected, uut)

    def test_source4(self) -> None:
        uut = environment.Environment()
        uut.source(var1)
        self.assertEqual(var1_expected, uut)

    def test_source5(self) -> None:
        uut = environment.Environment()
        uut.source(var2)
        self.assertEqual(var2_expected, uut)

    def test_filename1(self) -> None:
        uut = environment.Environment()
        with tempfile.NamedTemporaryFile() as tfile:
            fname = tfile.name
            tfile.write(simple1.getvalue().encode("UTF-8"))
            tfile.flush()
            uut.source(fname)
            self.assertEqual(simple1_expected, uut)

    def test_invalid_argument1(self) -> None:
        uut = environment.Environment()
        self.assertRaises(errors.InvalidArgumentError, uut.source, None)

    def test_file_format1(self) -> None:
        uut = environment.Environment()
        self.assertRaises(errors.FileFormatError, uut.source, invalid1)


if __name__ == "__main__":
    unittest.main()
