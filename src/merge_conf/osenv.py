#
# Copyright (c) 2020 Carsten Igel.
#
# This file is part of merge-conf
# (see https://github.com/carstencodes/merge-conf).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#

"""Environment variables can be used as configuration source as well.
The environment variables must be prefixed with a unique string and can contain
arbitrary values.

The variable MYAPP_DB_HOST will be interpreted as db.host, if the prefix is
set to MYAPP and the separator is set to _.
"""

import os
from typing import List, Dict, Union

from .base import ConfigurationSource


class EnvironmentVariableSource(ConfigurationSource):
    """A configuration source for environment variables.
    """

    def __init__(
        self, prefix: str, separator: str = "_", list_separator: str = ","
    ) -> None:
        """Creates a new instance of the EnvironmentVariableSource.

        Args:
            prefix (str): The unique prefix for the environment variables.
            separator (str, optional): The value separator. Defaults to "_".
            list_separator (str, optional): If a value can be interpreted as a
                list, this will be used as separator.. Defaults to ",".
        """
        self.__prefix = prefix or ""
        self.__separator = separator
        self.__list_item_separator = list_separator
        super().__init__()

    def read(self) -> dict:
        """Reads the environment variables and produces a nested key-value list.

        Returns:
            dict: The mapped environment variables.
        """
        result = dict()
        value_map: Dict[str, str] = EnvironmentVariableSource.__get_value_map()
        mapped_variables: List[str] = [
            key
            for (key, _) in value_map.items()
            if key.startswith(self.__prefix)
        ]
        for key in mapped_variables:
            value = value_map[key]
            sanitized: List[str] = self.__sanitize_key(key)
            items: dict = result
            for key_part in sanitized[:-1]:
                if key_part not in items.keys():
                    items[key_part] = dict()
                items = items[key_part]

            last_key: str = sanitized[-1]
            items[last_key] = self.__sanitize_value(value)

        return result

    @staticmethod
    def __get_value_map() -> Dict[str, str]:
        """Gets a list of key-value-pairs representing the
        environment variables.

        Returns:
            Dict[str, str]: The key-value map.
        """
        return os.environ

    def __sanitize_key(self, key: str) -> List[str]:
        """Splits a key according to the specified separators.

        Args:
            key (str): The key to split into lists.

        Returns:
            List[str]: The list of split keys.
        """
        if key is not None:
            working_ptr: str = key.lstrip(self.__prefix)
            return working_ptr.split(self.__separator)

        return [key]

    def __sanitize_value(self, value: str) -> Union[str, List[str]]:
        """Splits a value into a list, if applicable.

        Args:
            value (str): The value to parse.

        Returns:
            Union[str, List[str]]: The value parsed.
        """
        if value is not None:
            if self.__list_item_separator in value:
                return value.split(self.__list_item_separator)

            return value

        return ""
