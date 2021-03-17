"Local types for evars"
import enum
import typing

# Environment map
T_EMAP = typing.Mapping[str, str]

T_FILE = typing.Union[typing.TextIO, str]
T_FILE_ENCODING = typing.Optional[str]


class RetainThe(enum.Enum):  # pylint: disable=invalid-name
    "Return values for the overwrite callback"
    CURRENT_VALUE = 1
    FUTURE_VALUE = 2


T_OVERWRITE_CALLBACK_KEY = str
T_OVERWRITE_CALLBACK_CURRENT_VALUE = str
T_OVERWRITE_CALLBACK_FUTURE_VALUE = str
# A callback which receives the arguments:
#     key: str
#     current_value: str
#     future_value: str
# and returns an enumerated value, indicating that the current_value should be
# discarded and the future_value retained (RetainThe.FUTURE_VALUE) or that the
# future_value should be ignored and the current_value retained
# (RetainThe.CURRENT_VALUE).
T_OVERWRITE_CALLBACK = typing.Optional[
    typing.Callable[
        [
            T_OVERWRITE_CALLBACK_KEY,
            T_OVERWRITE_CALLBACK_CURRENT_VALUE,
            T_OVERWRITE_CALLBACK_FUTURE_VALUE,
        ],
        RetainThe,
    ]
]
