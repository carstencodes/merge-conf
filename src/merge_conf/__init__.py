#
# Copyright (c) 2020 Carsten Igel.
#
# This file is part of merge-conf
# (see https://github.com/carstencodes/merge-conf).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#
"""
The multi-conf module is intended to create a configuration object from
various sources. The basic idea is to use dictionaries and namespace objects.

The following sources are supported:
* ArgParse Namespaces
* ConfigParser Configuration objects
* Environment variables
. Via direct environments
. Via .env files
* JSON files
* YAML files
* TOML files
* Python module files

It enforces a generic way of programming.

For each source, a namespace can be defined. Namespaces are inherited from
the parent namespace. A namespace itself should only contain alphabetical
characters, since it can be automatically mapped to environment variables.
"""

from abc import abstractmethod
from os import PathLike
from os.path import isfile, realpath, basename, splitext, dirname, join
from pathlib import Path
from typing import Any, Iterable, List, Dict, Optional, Type, Union
from argparse import Namespace as CommandLineArguments
from sys import argv as command_line, platform as operating_system

from xdg import xdg_config_home, xdg_config_dirs

from .base import (
    ConfigurationProvidedError,
    ConfigurationSource,
    ConfigurationError,
    FileBasedConfigurationSource,
)

# Announce only python built-in readers. The rest must be considered as extras.
from .argparse import ArgParseSource
from .configparser import ConfigFileConfigurationSource
from .json import JsonFileConfigurationSource
from .module import ModuleConfigurationSource
from .osenv import EnvironmentVariableSource

__all__ = [
    "ConfigurationSource",
    "Namespace",
    "MultiConfigurationSource",
    "ArgParseSource",
    "ConfigFileConfigurationSource",
    "JsonFileConfigurationSource",
    "ModuleConfigurationSource",
    "EnvironmentVariableSource",
    "ConfigurationProvider",
    "ConfigurationError",
    "ConfigurationProvidedError",
    "Environment",
]


class Namespace:
    """An anonymous object serving as namespace carrier for the options.
       Only to be used, if no object is given.
    """


class _NamespaceMerger:
    """Simple instance used to merge dictionary objects into an existing
    object.
    """

    def __init__(self, namespace: Any = None) -> None:
        """Create a new instance of the namespace merger instance using
           the specified namespace object.

        Args:
            namespace (Any, optional): The namespace to use. If not set,
            a new Namespace instance will be created. Defaults to None.
        """
        self.__namespace = namespace or Namespace()

    def merge(self, values: Dict[str, Any]) -> Any:
        """Merges the specified values to the current instance
           namespace instance.

        Args:
            values (Dict[str, Any]): The values ot merge in.

        Returns:
            Any: The modified namespace stored in this instance.
        """
        target = self.__namespace
        if values is not None:
            for key, value in values.items():
                if not isinstance(value, dict):
                    setattr(target, key, value)
                else:
                    values_as_dict: dict = value.__dict__
                    inner_target: Namespace = Namespace()
                    merger: _NamespaceMerger = _NamespaceMerger(inner_target)
                    inner_target = merger.merge(values_as_dict)
                    setattr(target, key, inner_target)

        return target


class MultiConfigurationSource:
    """An object aggregating multiple sources to one single configuration object.
       The initial configuration can be added on object construction.
       Multiple configuration sources can be added before the
       read_configuration method is called.
    """

    def __init__(self, config: Any = None) -> None:
        """Creates a new instance using the specified configuration object as
           namespace carrier for options.

        Args:
            config (Any, optional): The existing configuration. If no
            configuration is specified, a new Namespace instance will
            be used. Defaults to None.
        """
        self.__target = config or Namespace()
        self.__sources: List[ConfigurationSource] = []

    def add_source(self, source: ConfigurationSource) -> None:
        """Adds the specified source object to the internal processing list.
           The instance will not be processed immediately but delayed.

        Args:
            source (ConfigurationSource): The source to process.
        """
        if source is not None:
            self.__sources.append(source)

    def add_sources(self, sources: Iterable[ConfigurationSource]) -> None:
        """Adds multiple sources to the internal processing list of this
           instance. The sources will be processed delayed on read.

        Args:
            sources (Iterable[ConfigurationSource]): The sources to add.
        """
        if sources is not None:
            for source in sources:
                self.add_source(source)

    def read_configuration(self) -> Any:
        """Reads the sources stored in the internal processing list to
           update the internal configuration object, which is returned
           after the last source has been read.

        Returns:
            Any: The configuration object. This is optional, if a
            configuration object has been provided on the construction
            of this instance.
        """
        result = self.__target
        merger: _NamespaceMerger = _NamespaceMerger(result)
        for source in self.__sources:
            items: dict = source.read()
            result = merger.merge(items)

        return result


class ConfigurationProvider:
    """The configuration provider is intended to provide a fluent
       interface on the construction of a MultiConfigurationSource object.
    """

    def __init__(self, existing_object: Optional[Any] = None) -> None:
        """Creates a new instance of the ConfigurationProvider class.

        Args:
            existing_object (Optional[Any], optional): The existing
                configuration object to re-use, if present. Defaults to None.
        """
        self.__source: Optional[
            MultiConfigurationSource
        ] = MultiConfigurationSource(existing_object)

    def from_configuration_files(
        self,
        *,
        factory: Type = ConfigFileConfigurationSource,
        files: Iterable[Union[str, PathLike]],
    ) -> "ConfigurationProvider":
        """Adds multiple configuration file sources, each in
           order of the files specified.

           e.g. from_configration_files(
                JsonFileConfigurationSource,
                get_json_files())

        Raises:
            ConfigurationProvidedError: If a configuration
                cannot be created, because it was already built.

        Returns:
            ConfigurationProvider: The modified instance.
        """
        self.__check_source()

        assert issubclass(factory, FileBasedConfigurationSource)

        for file in files:
            self.__source.add_source(factory(file))

        return self

    def from_os_environment(
        self, prefix: str, *, item_splitter: str = "_", list_splitter=","
    ) -> "ConfigurationProvider":
        """Appends a configuration source using OS
           environment variables.

        Raises:
            ConfigurationProvidedError: If a configuration
                cannot be created, because it was already built.

        Returns:
            ConfigurationProvider: The modified instance.
        """
        self.__check_source()

        self.__source.add_source(
            EnvironmentVariableSource(prefix, item_splitter, list_splitter)
        )

        return self

    def from_command_line(
        self, arguments: CommandLineArguments
    ) -> "ConfigurationProvider":
        """Appends the commend arguments as configuration source.

        Raises:
            ConfigurationProvidedError: If a configuration
                cannot be created, because it was already built.

        Returns:
            ConfigurationProvider: The modified instance.
        """
        self.__check_source()

        self.__source.add_source(ArgParseSource(arguments))

        return self

    def build(self) -> MultiConfigurationSource:
        """Builds MultiConfigurationSource resulting from this
           instance, invalidating this instance so that no further
           instances can be created from this instance.

        Raises:
            ConfigurationProvidedError: If a configuration
                cannot be created, because it was already built.

        Returns:
            MultiConfigurationSource: The configuration source to use.
        """
        self.__check_source()

        source: ModuleConfigurationSource = self.__source
        self.__source = None
        return source

    def __check_source(self) -> None:
        """Checks whether this instance has a source to modify.

        Raises:
            ConfigurationProvidedError: If a configuration
                cannot be created, because it was already built.
        """
        if self.__source is None:
            raise ConfigurationProvidedError()


class Environment:
    """An environment is used to provide certain information about
       the current application. It will also provide a list of
       possible configuration file locations.
    """

    def __init__(
        self, entry_point: Optional[Union[str, PathLike]] = None
    ) -> None:
        """Creates a new instance of the environment using the
           specified entry point.

        Args:
            entry_point (Optional[Union[str, PathLike]], optional): The
                path to the entry point starting this application.
                Defaults to None.
        """
        self.__entry_point = entry_point or realpath(command_line[0])

    @staticmethod
    def create(
        entry_point: Optional[Union[str, PathLike]] = None
    ) -> "Environment":
        """Creates a new instance of the environment
           matching the current operating system.

        Raises:
            NotImplementedError: If no implementation
            for the current operating system can be found.

        Returns:
            Environment: The environment for the current application
        """
        if operating_system in ["linux", "linux2"]:
            return _LinuxEnvironment(entry_point)

        raise NotImplementedError

    @property
    def app_name(self) -> str:
        """Gets the name of the current application.

        Returns:
            str: The name of the starting script.
        """
        app, _ = splitext(basename(self.__entry_point))
        return app

    @property
    def app_path(self) -> str:
        """Gets the location of the application.

        Returns:
            str: The path of the current application.
        """
        return dirname(self.__entry_point)

    @abstractmethod
    def get_config_files_candidates(
        self, config_file_ext=".conf", default_config_file_name: str = "config"
    ) -> Iterable[str]:
        """Creates a list of possible configuration files for the current application.

        Args:
            config_file_ext (str, optional): The extension of the configuration
                files to search. Defaults to ".conf".
            default_config_file_name (str, optional): The name of the
                configuration  file without extension. Defaults to "config".

        Returns:
            Iterable[str]: A list of paths for possible configuration files.
        """

    def get_existing_config_files(
        self, config_file_ext=".conf", default_config_file_name: str = "config"
    ) -> Iterable[str]:
        """Gets a list of configuration files. In contrast to the
           get_config_files_candidates method, which is merely a generator for
           file paths, this method filters the generated result and will only
           return the existing files.

        Args:
            config_file_ext (str, optional): The file extension to
                    search. Defaults to ".conf".
            default_config_file_name (str, optional): The file name
                    without extension. Defaults to "config".

        Returns:
            Iterable[str]: The configuration files matching the
                specified parameters.

        Yields:
            Iterator[Iterable[str]]: A configuration file.
        """
        for candidate in self.get_config_files_candidates(
            config_file_ext, default_config_file_name
        ):
            if isfile(candidate):
                yield candidate

    def get_settings_module(self, module_name="settings") -> Optional[str]:
        """Searches for a python file using the specified name
            next to the current application.

        Args:
            module_name (str, optional): The base name of the file.
                Defaults to "settings".

        Returns:
            Optional[str]: The full path of the settings file.
        """
        path: str = join(self.app_path, module_name + ".py")

        return path if isfile(path) else None


class _LinuxEnvironment(Environment):
    """Represents an environment implementation for linux like environments.
    """

    def __init__(
        self, entry_point: Optional[Union[str, PathLike]] = None
    ) -> None:
        """Creates a new instance of the _LinuxEnvironment class using
            the specified entry point.

        Args:
            entry_point (Optional[Union[str, PathLike]], optional):
                The entry point starting this app. Defaults to None.
        """
        super().__init__(entry_point=entry_point)

    def get_config_files_candidates(
        self, config_file_ext=".conf", default_config_file_name: str = "config"
    ) -> Iterable[str]:
        """Creates a list of file paths using the file system (Linux File
              Hierarchy Standard), the XDG standard and the current app_name
              to generate the files.

        Args:
            config_file_ext (str, optional): The file extension to
                search. Defaults to ".conf".
            default_config_file_name (str, optional): The configuration
                file base name.. Defaults to "config".

        Returns:
            Iterable[str]: The list of possible files

        Yields:
            Iterator[Iterable[str]]: A file path that
                might be used for configuration.
        """
        yield join("etc", self.app_name, self.app_name + config_file_ext)
        yield join(
            "etc", self.app_name, default_config_file_name + config_file_ext
        )

        try:
            global_dirs: List[Path] = xdg_config_dirs()
            local_dir: Path = xdg_config_home()

            for global_dir in global_dirs:
                yield join(
                    global_dir, self.app_name, self.app_name + config_file_ext
                )
                yield join(
                    global_dir,
                    self.app_name,
                    default_config_file_name + config_file_ext,
                )

            yield join(
                local_dir, self.app_name, self.app_name + config_file_ext
            )
            yield join(
                local_dir,
                self.app_name,
                default_config_file_name + config_file_ext,
            )
        except ImportError:
            pass

        yield join(
            Path.home(), "." + self.app_name, self.app_name + config_file_ext
        )
        yield join(
            Path.home(),
            "." + self.app_name,
            default_config_file_name + config_file_ext,
        )

        yield join(self.app_path, self.app_name + config_file_ext)
        yield join(self.app_path, default_config_file_name + config_file_ext)
