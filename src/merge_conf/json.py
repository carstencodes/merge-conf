#
# Copyright (c) 2020 Carsten Igel.
#
# This file is part of merge-conf
# (see https://github.com/carstencodes/merge-conf).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#

"""Reads JSON files as configuration files.
"""

import json

from typing import Any, TextIO

from .base import FileBasedConfigurationSource, ConfigurationError


class JsonFileConfigurationSource(FileBasedConfigurationSource):
    """A configuration source using a JSON file a configuration source.
    """

    def _load_stream(self, stream: TextIO) -> dict:
        try:
            result: Any = json.load(stream)
        except json.decoder.JSONDecodeError as error:
            raise ConfigurationError(self._file_path) from error
        if result is dict:
            return result

        return dict(value=result)
