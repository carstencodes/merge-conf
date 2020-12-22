#
# Copyright (c) 2020 Carsten Igel.
#
# This file is part of merge-conf
# (see https://github.com/carstencodes/merge-conf).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#

"""Provides the implementation of the Configuration source for
   an argument parser result.
"""

from argparse import Namespace

from .base import ConfigurationSource


class ArgParseSource(ConfigurationSource):
    """Configuration source for argument parsing results.
    """

    def __init__(self, arguments: Namespace) -> None:
        """Creates a new instance from the specified
             argument parsing result namespace.

        Args:
            arguments (Namespace): The argument parser result.
        """
        self.__namespace = arguments

    def read(self) -> dict:
        """Reads the underlying configuration.

        Returns:
            dict: The dictionary of parsed configuration values.
        """
        return self.__namespace.__dict__
