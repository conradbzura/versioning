# Versioning

Versioning is a Python package for managing version strings according to PEP 440 and SemVer 2.0 specifications. It includes support for parsing, comparing, rendering, and incrementing version strings.

## Installation

To install the package from GitHub, use the following command:

```sh
pip install git+https://github.com/conradbzura/versioning.git
```

## Usage

### Basic Usage

```python
from versioning import PythonicVersion, SemanticVersion

# Create a pythonic version
py_version = PythonicVersion(major_release=1, minor_release=0, patch_release=0, release_cycle=".", post_release=1, local_identifier="deadbeef")
print(py_version)  # Output: 1.0.0.post1+deadbeef

# Create a semantic version
sem_version = SemanticVersion(major_release=1, minor_release=0, patch_release=0, pre_release=("alpha", 1), build="deadbeef")
print(sem_version)  # Output: 1.0.0-alpha.1+deadbeef
```

### Using Custom Parsers

You can define custom parsers using the `@parser` decorator:

```python
from versioning import parser, PythonicVersion

@parser("custom")
def custom() -> str:
    return "1.0.0"

version = PythonicVersion.parse.custom()
```

### Running Tests

To run the unit tests, use the following command:

```sh
make tests
```

To run the tests in debug mode, use:

```sh
make debug-tests
```

To run the tests and update expected results, use:

```sh
make update-tests
```

## License

This project is licensed under the MIT License.
