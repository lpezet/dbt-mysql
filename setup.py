#!/usr/bin/env python
import sys

if sys.version_info < (3, 7):
    print("Error: dbt does not support this version of Python.")
    print("Please upgrade to Python 3.7 or higher.")
    sys.exit(1)


try:
    from setuptools import find_namespace_packages
except ImportError:
    print("Error: dbt requires setuptools v40.1.0 or higher.")
    print(
        'Please upgrade setuptools with '
        '"pip install --upgrade setuptools" and try again'
    )
    sys.exit(1)


from pathlib import Path
from setuptools import setup


# pull the long description from the README
README = Path(__file__).parent / "README.md"


# used for this adapter's version and in determining
# the compatible dbt-core version
VERSION = Path(__file__).parent / "dbt/adapters/mysql/__version__.py"


def _plugin_version() -> str:
    """
    Pull the package version from the main package version file
    """
    attributes = {}
    exec(VERSION.read_text(), attributes)
    return attributes["version"]


def _core_patch(plugin_patch: str):
    """
    Determines the compatible dbt-core patch given this plugin's patch

    Args:
        plugin_patch: the version patch of this plugin
    """
    pre_release_phase = "".join([i for i in plugin_patch if not i.isdigit()])
    if pre_release_phase:
        if pre_release_phase not in ["a", "b", "rc"]:
            raise ValueError(f"Invalid prerelease patch: {plugin_patch}")
        return f"0{pre_release_phase}1"
    return "0"


# require a compatible minor version (~=)
# and prerelease if this is a prerelease
def _core_version(plugin_version: str = _plugin_version()) -> str:
    """
    Determine the compatible dbt-core version give this plugin's version.

    We assume that the plugin must agree with `dbt-core`
    down to the minor version.

    Args:
        plugin_version: the version of this plugin, this is an argument
        in case we ever want to unit test this
    """
    try:
        major, minor, plugin_patch = plugin_version.split(".")
    except ValueError:
        raise ValueError(f"Invalid version: {plugin_version}")

    return f"{major}.{minor}.{_core_patch(plugin_patch)}"


setup(
    name="@lpezet/dbt-mysql",
    version=_plugin_version(),
    description="A MySQL adapter for dbt [by https://github.com/lpezet]",
    long_description=README.read_text(),
    long_description_content_type="text/markdown",
    author="Doug Beatty",
    author_email="doug.beatty@gmail.com",
    url="https://github.com/dbeatty10/dbt-mysql",
    packages=find_namespace_packages(include=["dbt", "dbt.*"]),
    include_package_data=True,
    install_requires=[
        f"dbt-core~={_core_version()}",
        "mysql-connector-python>=8.0.0,<8.1",
    ],
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
)
