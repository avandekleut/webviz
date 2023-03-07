set -e

PYTHON_VERSION=3.8

VIRTUALENV_NAME=local

curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh

brew install python@$PYTHON_VERSION poetry

virtualenv $VIRTUALENV_NAME --python=$PYTHON_VERSION

source $VIRTUALENV_NAME/bin/activate

poetry env use $(which python)

poetry install