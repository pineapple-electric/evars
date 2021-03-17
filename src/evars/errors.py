"Errors for evars"


class EvarsBaseError(Exception):
    "A base for errors raised by the evars package"


class FileFormatError(EvarsBaseError):
    "An unexpected token has been found or an expected token is missing."


class InvalidArgumentError(EvarsBaseError):
    "The provided argument was not of the type required by this method."


class NoMatchingSubstitutionError(EvarsBaseError):
    "The parser found a variable which does not have a defined substitution."


class UnsupportedVariableError(EvarsBaseError):
    "The parser found an unsupported variable."
