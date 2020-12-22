#
# Copyright (c) 2020 Carsten Igel.
#
# This file is part of merge-conf
# (see https://github.com/carstencodes/merge-conf).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#

"""Reads an arbitrary python module file as configuration files.
    All variables declared in this module will be used as configuration entry.
"""

from importlib.machinery import ModuleSpec
from importlib.abc import Loader
from importlib.util import (
    spec_from_file_location as create_module_spec,
    module_from_spec as load_module,
)
from types import ModuleType
from os.path import isfile, basename, splitext

from typing import TextIO
from sys import modules

from .base import ConfigurationError, FileBasedConfigurationSource


class ModuleConfigurationSource(FileBasedConfigurationSource):
    """Configuration source using an arbitrary python module file.
    """

    def read(self) -> dict:
        """Loads an arbitrary python module and reads
            it variables as configuration source.

        Raises:
            merge_conf.base.ConfigurationError: If the module
                cannot be loaded properly.

        Returns:
            dict: The key-value list of configuration values.
        """
        if isfile(self._file_path):
            base_name = basename(self.__file_path)
            file_name, _ = splitext(base_name)
            try:
                spec: ModuleSpec = create_module_spec(
                    file_name, self._file_path
                )
                module: ModuleType = load_module(spec)
                modules[file_name] = module
                if isinstance(spec.loader, Loader):
                    loader: Loader = spec.loader
                    loader.exec_module(module)

                    return vars(module)
            except Exception as error:
                raise ConfigurationError(self._file_path) from error
        return dict()

    def _load_stream(self, stream: TextIO) -> dict:
        """Empty overload. Is never called.

        Args:
            stream (TextIO): The text stream to load. Ignored.

        Returns:
            dict: An empty dictionary.
        """
        _ = stream
        return dict()
