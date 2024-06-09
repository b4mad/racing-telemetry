# Telemetry

This repository contains Jupyter notebooks for analyzing racing data and a Python library for telemetry data analysis.

## Directory Structure

- `notebooks/`: Jupyter notebooks for data analysis.
- `telemetry/`: Python library for telemetry data analysis.
- `tests/`: Unit tests for the library.
- `setup.py`: Packaging and distribution configuration.
- `README.md`: Project overview.
- `.gitignore`: Git ignore file.

## Installation with Pipenv

To install the library using Pipenv, run:

```bash
pipenv install
```

To activate the virtual environment, use:

```bash
pipenv shell
```

## Installation with pip

To install the library, run:

```bash
pip install .
```

## Running Tests

To run the tests, use:

```bash
pipenv run pytest
```

## Usage

You can use the library in your notebooks as follows:

```python
from telemetry import Telemetry

# Example usage
telemetry = Telemetry()
```
