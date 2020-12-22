#
# Copyright (c) 2020 Carsten Igel.
#
# This file is part of merge-conf
# (see https://github.com/carstencodes/merge-conf).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#

"""Basic definition for the entire package that can be used across all modules.
"""

from abc import abstractmethod
from os.path import isfile
from typing import TextIO


class ConfigurationError(Exception):
    """A configuration error that occurs while reading the source.
    """

    def __init__(self, source: str) -> None:
        """Creates a new instance of the configuration error.

        Args:
            source (str): The source describing the error.
        """
        super().__init__(
            "Error while reading configuration from source %s" % source
        )


class ConfigurationProvidedError(Exception):
    """A basic error for the configuration provider.
    """


class ConfigurationSource:
    """Basic definition of an arbitrary configuration source.
    """

    @abstractmethod
    def read(self) -> dict:
        """Reads the configuration source by creating keys and values.

        Returns:
            dict: The configuration values.
        """


class FileBasedConfigurationSource(ConfigurationSource):
    """Basic definition of a configuration source that is based on files.
    """

    def __init__(self, file_path: str) -> None:
        """Creates a new instance of the FileBaseConfiguration source.

        Args:
            file_path (str): The path of the file.
        """
        super().__init__()
        self.__file_path = file_path

    @property
    def _file_path(self) -> str:
        """Gets the current configuration file path.

        Returns:
            str: The file path.
        """
        return self.__file_path

    def read(self) -> dict:
        """Opens the configuration file and reads the values from it.

        Returns:
            dict: The values of the file.
        """
        if isfile(self.__file_path):
            with open(self.__file_path, "r") as handle:
                return self._load_stream(handle)
        return dict()

    @abstractmethod
    def _load_stream(self, stream: TextIO) -> dict:
        """Loads the specified text stream and creates a key-value
            list from it.

        Args:
            stream (TextIO): The text stream to read.

        Returns:
            dict: The configuration values.
        """
