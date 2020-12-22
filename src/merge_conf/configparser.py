#
# Copyright (c) 2020 Carsten Igel.
#
# This file is part of merge-conf
# (see https://github.com/carstencodes/merge-conf).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#

"""With this module, the configuration values stored in a configuration
    file will be read. The file must be parsable using the configparser module.
"""

from configparser import SafeConfigParser, ConfigParser, SectionProxy

from typing import List, Union

from .base import ConfigurationSource


class ConfigFileConfigurationSource(ConfigurationSource):
    """A configuration source based on a file that can be parsed by the
        configparser module.
    """

    def __init__(self, config_file: str) -> None:
        """Creates a new instance of the ConfigFileConfigurationFile class

        Args:
            config_file (str): The configuration file to read.
        """
        self.__config_file = config_file

    def read(self) -> dict:
        """Reads the configuration file and parses it values to a dictionary.

        Returns:
            dict: The key-value list of options.
        """
        parser: ConfigParser = SafeConfigParser()
        lines: List[str] = parser.read(self.__config_file)
        if len(lines) == 0:
            return dict()

        result = dict()
        for section_name in parser.sections():
            section_values = dict()

            section: SectionProxy = parser[section_name]

            for key in section.keys():
                section_values[key] = self._read_key_typed(
                    section_name, key, section[key]
                )

            result[section] = section_values

        return result

    def _read_key_typed(
        self, section: str, key: str, value: str
    ) -> Union[str, bool, int, float]:
        """If overridden in a class, the type of the value
            can be determined based upon the section and key.

        Args:
            section (str): The section
            key (str): The key
            value (str): The value to parse

        Returns:
            Union[str, bool, int, float]: THe parsed value.
        """
        # Satisfy linter
        _ = section
        _ = key
        _ = self

        return value
