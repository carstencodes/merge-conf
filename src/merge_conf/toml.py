#
# Copyright (c) 2020 Carsten Igel.
#
# This file is part of merge-conf
# (see https://github.com/carstencodes/merge-conf).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#

"""Uses TOML files as configuration sources. A TOML file is basically
   a dictionary consisting of grouped key-value-pairs. This can be
   activated using the extra 'toml'.
"""

from typing import Any, TextIO
import toml

from .base import FileBasedConfigurationSource


class TomlConfigurationSource(FileBasedConfigurationSource):
    """A configuration source using TOML files for data retrieval.
    """

    def _load_stream(self, stream: TextIO) -> dict:
        """Loads the specified text stream as TOML file.

        Args:
            stream (TextIO): The stream to read as TOML file.

        Returns:
            dict: The key-value list.
        """
        items: Any = toml.load(stream)

        result: dict = dict()

        result.update(items)

        return result
