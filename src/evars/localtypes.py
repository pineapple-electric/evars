"Local types for evars"
import enum
import typing

EnvironmentFile = typing.Union[typing.TextIO, str]
EnvironmentMapping = typing.Mapping[str, str]
FileEncoding = typing.Optional[str]


class RetainThe(enum.Enum):  # pylint: disable=invalid-name
    "Return values for the overwrite callback"
    CURRENT_VALUE = 1
    FUTURE_VALUE = 2


OverwriteCallbackKey = str
OverwriteCallbackCurrentValue = str
OverwriteCallbackFutureValue = str
# A callback which receives the arguments:
#     key: str
#     current_value: str
#     future_value: str
# and returns an enumerated value, indicating that the current_value should be
# discarded and the future_value retained (RetainThe.FUTURE_VALUE) or that the
# future_value should be ignored and the current_value retained
# (RetainThe.CURRENT_VALUE).
OverwriteCallback = typing.Optional[
    typing.Callable[
        [
            OverwriteCallbackKey,
            OverwriteCallbackCurrentValue,
            OverwriteCallbackFutureValue,
        ],
        RetainThe,
    ]
]
