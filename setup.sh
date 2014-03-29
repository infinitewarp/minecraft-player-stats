# If you're on a system with multiple Python installations, you may
# need to change "virtualenv" to something like "virtualenv-2.6".
virtualenv flaskenv
PIP=flaskenv/bin/pip
$PIP install flask
$PIP install beaker
