# CITS4403-Project

## Setup Instructions

1. Ensure the current working directory is the root of this project.
2. Create a virtual environment: `python3 -m venv .venv`
3. Activate the virtual environment: `source .venv/bin/activate`
4. Install the package requirements: `pip install -r requirements.txt`

## Usage Guide

1. Ensure the current working directory is the root of this project.
2. Run main with: `python3 -m src.main`

## Development

1. Complete the setup instructions above.
2. Install git hooks for pre-commit: `pre-commit install`
    - This will format and sort imports of `.py` files with [black](https://github.com/psf/black) and [isort](https://github.com/PyCQA/isort) respectively.
