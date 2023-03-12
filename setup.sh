set -e

PYTHON_VERSION=3.8

VIRTUALENV_NAME=local

# install homebrew
command -v brew || ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

# install python
command -v python$PYTHON_VERSION || brew install python@$PYTHON_VERSION

# install poetry
command -v poetry || brew install poetry

# activate poetry env
poetry env use $PYTHON_VERSION

poetry shell

poetry install

poetry export -o requirements.txt --without-hashes

export PYTHONPATH=$PYTHONPATH:$(pwd)

set +e