"Represent an environment with a dictionary"
import io
import logging
import shlex

from .errors import FileFormatError
from .errors import InvalidArgumentError
from .localtypes import RetainThe
from .localtypes import EnvironmentFile
from .localtypes import FileEncoding
from .localtypes import OverwriteCallback
from .parser import EnvironmentSubstitutionParser

logger = logging.getLogger(__name__)


class Environment(dict):
    "A key-value mapping for an execution environment"

    def source(
        self,
        env_file: EnvironmentFile,
        encoding: FileEncoding = None,
        overwrite_callback: OverwriteCallback = None,
    ) -> "Environment":
        """
        Source the specified environment file

        Values are expected in the format:

            VARIABLE_NAME=variable value as a string
            SECOND_VARIABLE="quotes are OK"

        The source ``env_file`` must be either a ``str``, specifying the file
        to open, or a ``TextIOBase`` which will provide lines via the
        ``readlines`` method.

        If ``encoding`` is not specified, UTF-8 is assumed.

        if ``overwrite_callback`` is not specified, values will not be
        overwritten when keys in the source match existing keys in the
        environment dictionary.  If ``overwrite_callback`` returns a value
        other than is specified in the ``RetainThe`` enumeration, values will
        not be overwritten.  To overwrite existing values, return
        ``RetainThe.FUTURE_VALUE`` from the ``overwrite_callback``.  Something
        as simple as this lambda will overwrite all values::

            lambda x, y, z: RetainThe.FUTURE_VALUE
        """
        # pylint: disable=too-many-locals
        working_values = self.copy()
        close_file = False
        if isinstance(env_file, str):
            logger.debug("Environment.source(): Opening file %s", env_file)
            if encoding is None:
                encoding = "UTF-8"
            env_file = open(  # pylint: disable=consider-using-with
                env_file, "r", encoding=encoding
            )
            close_file = True
        elif isinstance(env_file, io.TextIOBase):
            pass
        else:
            logger.error(
                "Environment.source() requires a file handle or string as the "
                "first argument: %s",
                env_file,
            )
            raise InvalidArgumentError(
                "Environment.source() requires a file handle or string as the "
                f"first argument: {env_file}"
            )
        for line in env_file.readlines():
            parts = shlex.shlex(line, posix=False)
            # mypy says that parts.get_token() returns an Optional[str].  To
            # ensure that we get a string, we add 'or ""' to (most) calls to
            # parts.get_token().
            left = parts.get_token() or ""
            equals = parts.get_token()
            if equals != "=":
                raise FileFormatError(
                    f"The second token is expected to be an equals sign: {line}"
                )
            # Assemble right side
            right_parts = []
            right = parts.get_token() or ""
            while right != "":
                right_parts.append(right)
                right = parts.get_token() or ""
            right = "".join(right_parts)
            # Check right side for substitutions
            parser = EnvironmentSubstitutionParser(right)
            expanded = parser.expand(working_values)
            if left in working_values.keys():
                if overwrite_callback is not None:
                    cb_result = overwrite_callback(
                        left, working_values[left], expanded
                    )
                    if cb_result == RetainThe.FUTURE_VALUE:
                        working_values[left] = expanded
            else:
                working_values[left] = expanded

        if close_file:
            env_file.close()
        self.update(working_values)
        return self
