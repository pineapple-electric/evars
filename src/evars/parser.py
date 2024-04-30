"Parse environment variable lines from POSIX shells"
import enum
import logging

from .errors import NoMatchingSubstitutionError
from .errors import UnsupportedVariableError
from .localtypes import EnvironmentMapping

logger = logging.getLogger(__name__)


class _ESPStates(enum.Enum):
    # State: none
    # Transitions:
    #   -> FOUND_BACKSLASH
    #   -> FOUND_DOLLAR_SIGN
    #   -> FOUND_DOUBLE_QUOTE
    #   -> FOUND_SINGLE_QUOTE
    NONE = 1
    FOUND_DOLLAR_SIGN = 2
    FOUND_OPEN_BRACKET = 3
    FOUND_VARIABLE_NAME = 4
    FOUND_DOUBLE_QUOTE = 5
    FOUND_SINGLE_QUOTE = 6
    FOUND_BACKSLASH = 7


class EnvironmentSubstitutionParser:
    "Parse environment values for substitutions"
    # pylint: disable=too-few-public-methods

    _parsing_variable_name = [
        _ESPStates.FOUND_DOLLAR_SIGN,
        _ESPStates.FOUND_OPEN_BRACKET,
        _ESPStates.FOUND_VARIABLE_NAME,
    ]
    _ready_for_variable = [
        _ESPStates.NONE,
        _ESPStates.FOUND_DOUBLE_QUOTE,
    ]

    def __init__(self, value: str):
        self._v = value

    def expand(self, evars: EnvironmentMapping) -> str:
        "Expand variables found in the initial string"
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-statements
        # Because of quotes, regular expressions are not
        # reasonable to use here.
        i = 0
        parts = []
        varname = []  # Just the name of the variable, for look-up in evars
        varparts = []  # Raw parts of the varname, including $ and {}
        state = [_ESPStates.NONE]

        # Ugh, a parsing loop.
        # This parsing loop is based on reading code from pdksh and reading the
        # BASH manual:
        # https://www.gnu.org/software/bash/manual/html_node/Quoting.html
        while i < len(self._v):
            cur = self._v[i]
            if state[-1] in self._parsing_variable_name:
                if (  # pylint: disable=no-else-continue
                    cur == "_" or cur.isalpha() and cur.isascii()
                ):
                    assert "$" in varparts
                    varname.append(cur)
                    varparts.append(cur)
                    if state[-1] != _ESPStates.FOUND_VARIABLE_NAME:
                        state.append(_ESPStates.FOUND_VARIABLE_NAME)
                    i = i + 1
                    continue
                # Digits cannot be the first character in a variable name.
                elif (
                    cur.isdigit()
                    and cur.isascii()
                    and state[-1] == _ESPStates.FOUND_VARIABLE_NAME
                ):
                    varname.append(cur)
                    varparts.append(cur)
                    i = i + 1
                    continue
                # These are special parameters in BASH.  Ignore them.
                elif (
                    cur in ["*", "#", "?", "-", "$", "!", "0"]
                    and len(varname) == 0
                ):
                    varparts.append(cur)
                    var = "".join(varparts)
                    varparts.clear()
                    logger.error(
                        "Unsupported special variable %s encountered",
                        repr(var),
                    )
                    raise UnsupportedVariableError(var)
                    # if _ESPStates.FOUND_OPEN_BRACKET == state.pop():
                    #    assert _ESPStates.FOUND_DOLLAR_SIGN == state.pop()
                    # i = i + 1
                    # continue
                elif cur == "{" and state[-1] == _ESPStates.FOUND_DOLLAR_SIGN:
                    assert len(varparts) == 1
                    assert varparts[0] == "$"
                    varparts.append(cur)
                    state.append(_ESPStates.FOUND_OPEN_BRACKET)
                    i = i + 1
                    continue
                elif cur == "}" and _ESPStates.FOUND_OPEN_BRACKET in state:
                    assert "$" in varparts
                    assert "{" in varparts
                    assert "}" not in varparts
                    varparts.append(cur)

                    # Flush the arrays
                    var = "".join(varname)
                    if var in evars:
                        parts.append(evars[var])
                    else:
                        raise NoMatchingSubstitutionError("".join(varparts))
                    varname.clear()
                    varparts.clear()

                    assert _ESPStates.FOUND_VARIABLE_NAME == state.pop()
                    assert _ESPStates.FOUND_OPEN_BRACKET == state.pop()
                    assert _ESPStates.FOUND_DOLLAR_SIGN == state.pop()
                    i = i + 1
                    continue
                # Otherwise...
                assert "$" in varparts
                assert "{" not in varparts
                assert "}" not in varparts

                # Flush the arrays
                var = "".join(varname)
                if var in evars:
                    parts.append(evars[var])
                else:
                    raise NoMatchingSubstitutionError("".join(varparts))
                varname.clear()
                varparts.clear()

                assert _ESPStates.FOUND_VARIABLE_NAME == state.pop()
                assert _ESPStates.FOUND_DOLLAR_SIGN == state.pop()
            if cur == "$" and state[-1] in [
                _ESPStates.NONE,
                _ESPStates.FOUND_DOUBLE_QUOTE,
            ]:
                state.append(_ESPStates.FOUND_DOLLAR_SIGN)
                varparts.append(cur)
                i = i + 1
            elif cur == "'":
                if state[-1] == _ESPStates.NONE:
                    state.append(_ESPStates.FOUND_SINGLE_QUOTE)
                elif state[-1] == _ESPStates.FOUND_SINGLE_QUOTE:
                    state.pop()
                elif state[-1] == _ESPStates.FOUND_DOUBLE_QUOTE:
                    parts.append(cur)
                i = i + 1
            elif cur == '"':
                if state[-1] == _ESPStates.NONE:
                    state.append(_ESPStates.FOUND_DOUBLE_QUOTE)
                elif state[-1] == _ESPStates.FOUND_SINGLE_QUOTE:
                    parts.append(cur)
                elif state[-1] == _ESPStates.FOUND_DOUBLE_QUOTE:
                    state.pop()
                i = i + 1
            else:
                parts.append(cur)
                i = i + 1

        # If a variable has been found but not expanded, expand it.
        if varname:
            var = "".join(varname)
            if var in evars:
                parts.append(evars[var])
            else:
                raise NoMatchingSubstitutionError("".join(varparts))
            varname.clear()
            varparts.clear()

        expanded = "".join(parts)
        return expanded
