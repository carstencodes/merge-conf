#
# Copyright (c) 2020 Carsten Igel.
#
# This file is part of merge-conf
# (see https://github.com/carstencodes/merge-conf).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#

"""Configuration entries provided by a .env file will be parsed using
   this file. This configuration source is only enabled, if the extra
   'dotenv' is enabled.
"""

from typing import Optional
from dotenv import load_dotenv

from .osenv import EnvironmentVariableSource


class DotEnvConfigurationSource(EnvironmentVariableSource):
    """Configuration source using .env files.
    """

    def __init__(
        self,
        prefix: str,
        env_file: Optional[str] = None,
        separator: str = "_",
        list_separator: str = ",",
    ) -> None:
        """Creates a new instance of the .env configuration source.

        Args:
            prefix (str): The prefix for .env files.
            env_file (Optional[str], optional): The path of the
                configuration file. Defaults to None.
            separator (str, optional): The separator for
                splitting. Defaults to "_".
            list_separator (str, optional): If a configuration
                value is a list, split different values by this
                separator. Defaults to ",".
        """
        super().__init__(
            prefix, separator=separator, list_separator=list_separator
        )
        self.__env_file: Optional[str] = env_file
        self.__override_existing: bool = False

    def __get_override(self) -> bool:
        """Returns the value whether overriding
            existing environment variables is allowed.

        Returns:
            bool: A flag indicating whether overriding
                is allowed or not.
        """
        return self.__override_existing

    def __set_override(self, value: bool) -> None:
        """Sets the value whether overriding existing
            environment variables is allowed or not.

        Args:
            value (bool): A flag indicating whether
            overriding existing environment variables
            is allowed or not.
        """
        self.__override_existing = value

    override = property(__get_override, __set_override)
    """A value indicating whether overriding existing
        environment variables is allowed (True) or not.
    """

    def read(self) -> dict:
        """Reads the configuration source to a key-value list.

        Returns:
            dict: The configuration values.
        """
        if self.__env_file is None:
            load_dotenv(override=self.__override_existing)
        else:
            load_dotenv(self.__env_file, override=self.__override_existing)
        return super().read()
