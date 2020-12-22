# Multiconf-py

A configuration aggregator for multiple configuration sources.

Using this library, it is easy to combine multiple configuration or settings sources. The following items can be combined:

- a fixed object with default settings
- command-line arguments
- environment variables
- configuration files like
  - .env files
  - python files
  - ConfigParser style ini files
  - toml files
  - yaml files
  - json files

The basic entry point is the so called `MultiConfigurationSource`. It can be initialized with an optional, existing configuration object. Multiple `ConfigurationSource` objects can be added. These objects will be traversed in order of insertion. Each of these instances create a dictionary of configuration entries that will be used to extend or override the previous ones. The resulting object can be received using the `read_configuration` method.

## Example

```python

import multiconf

config = None # Create existing object
arguments = None # Argument parser result namespace

source = multiconf.MultiConfigurationSource(config)
source.add(multiconf.ConfigFileConfigurationSource(
    # Configuration file path
))
source.add(multiconf.EnvironmentVariableSource("MY_APP"))
source.add(multiconf.ArgParseSource(arguments))

config = source.read_configuration()
```

In this example, the configuration object will be created first. Then, the configuration file will be created. Afterwards, all environment variables starting with `MY_APP_` will be used for configuration. The final configuration item will be fetched from the `argparse` module.

The trick is to created the configuration namespaces with a little sure instinct, so that items can be overridden.

## Installing

The package can be installed using pip. Most support comes out of the box, but for the following features an extra must be activated:

.env file support (dotenv)
yaml file support (yaml)
toml file support (toml)

## Licensing

This library is published under BSD-3-Clause license.
