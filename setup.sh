set -e

PYTHON_VERSION=3.8

VIRTUALENV_NAME=local

which -s brew
if [[ $? != 0 ]] ; then
    # Install Homebrew
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
else
    brew update
fi

brew install python@$PYTHON_VERSION poetry graphviz

virtualenv $VIRTUALENV_NAME --python=$PYTHON_VERSION

source $VIRTUALENV_NAME/bin/activate

poetry env use $(which python)

poetry install