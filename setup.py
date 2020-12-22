#!/usr/bin/env python
#
# Copyright (c) 2020 Carsten Igel.
#
# This file is part of merge-conf
# (see https://github.com/carstencodes/merge-conf).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#

from setuptools import setup, find_packages

__VERSION__ = "0.9.0"

long_description: str = ""
with open("README.md", "r") as read_me_file:
    long_description = read_me_file.read()

setup(
    name="merge-conf",
    version=__VERSION__,
    license="BSD-3-Clause",
    author="Carsten Igel",
    author_email="cig@bite-that-bit.de",
    description="Combine multiple configuration sources to a single configuration object.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    url="https://github.com/carstencodes/merge-conf",
    install_requires=["xdg"],
    extras_require={
        "yaml": ["pyyaml"],
        "dotenv": ["python-dotenv"],
        "toml": ["toml"],
    },
    package_dir={"": "src"},
    keywords="configuration, environment, dotenv, arguments, development",
    python_requires=">=3.7, < 4",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System",
        "Typing :: Typed",
    ],
)
