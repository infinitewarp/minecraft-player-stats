#!/usr/bin/env bash

# If "virtualenv" is not in your $PATH or you wish to override it, run:
# export VIRTUALENV_BIN="/path/to/your/virtualenv"

# If you wish to set a custom directory to hold the virtual environment, run:
# export ENV_DIR="/path/to/your/virtual/environment/directory"

if [ -z "${VIRTUALENV_BIN}" ]; then
    VIRTUALENV_BIN=$(which virtualenv)
fi

if [ -z "${ENV_DIR}" ]; then
    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    ENV_DIR="$DIR/webappenv"
fi

echo "Using ${VIRTUALENV_BIN} to manage environment in ${ENV_DIR}"

${VIRTUALENV_BIN} ${ENV_DIR} || exit 1
source ${ENV_DIR}/bin/activate || exit 1

pip install flask
pip install beaker
pip install requests
