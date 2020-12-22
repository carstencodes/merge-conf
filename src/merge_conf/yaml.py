#
# Copyright (c) 2020 Carsten Igel.
#
# This file is part of merge-conf
# (see https://github.com/carstencodes/merge-conf).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#

"""This module handles YAML files as configuration file sources.
It must be activated using the extra 'yaml'.
"""

from typing import Any, TextIO
import yaml


from .base import FileBasedConfigurationSource


class YamlConfigurationSource(FileBasedConfigurationSource):
    """A configuration source using yaml files.
    """

    def _load_stream(self, stream: TextIO) -> dict:
        """Loads the specified text stream as YAML file.

        Args:
            stream (TextIO): The text stream to read.

        Returns:
            dict: The configuration values.
        """
        result: Any = yaml.parse(stream, Loader=yaml.SafeLoader)

        if result is dict:
            return result

        return dict(value=result)
