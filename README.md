minecraft-player-stats
======================

A web application for displaying player stats from a Minecraft server. An app with a sterile name but hopefully a sterling presentation.


Disclaimer
----------

This project is currently in its infancy. Don't expect a whole lot of functionality just yet!


Overview
--------

Minecraft servers automatically generate statistics about player activities and periodically save those stats to disk (roughly every five minutes). These stats for each user include her achievements, the number and types of blocks broken, distance traveled by various methods, etc. However, Minecraft itself doesn't come with a visualizer for this captured data. The minecraft-player-stats app reads that data and serves it to visitors in a friendly, consumable format.

Because minecraft-player-stats reads player stats from disk instead of interfacing directly with the running Minecraft server, the minecraft-player-stats app can be run separately from the Minecraft server itself. This sets up some interesting possibilities from a server management perspective. If you run a private Minecraft server (perhaps on a LAN), you could publicly expose your stats on the web through this app. If you're security-conscious, you could set up a job to sync player stats from your game server to your web server so Minecraft's binaries and data are never potentially exposed by the web server. If your Minecraft server is under heavy load (as many tend to be), running the stats on a separate server potentially relieves strain from the game.


Installation
------------

Your system must have a reasonably modern version of Python (successfully tested in 2.6, 2.7, and 3.4) and virtualenv available. The setup script uses the default "virtualenv" in your path to create and manage a virtual evironment in the local "webappenv" directory. You can override these locations by exporting VIRTUALENV_BIN and ENV_DIR respectively before running the setup script.

Running setup with defaults is as simple as:
```bash
./setup.sh
```

If you want to override the default virtualenv binary and webappenv directory, you might do something like:
```bash
export VIRTUALENV_BIN=/usr/bin/virtualenv-2.6
export ENV_DIR=~/.virtualenvs/minecraft-player-stats
./setup.sh
```

Running
-------

To run using the built-in Python webserver, activate your virtual environment and exectue the run script. Using the default local "webappenv" directory for the virtual environment, for example:

```bash
. ./webappenv/bin/activate
./run.sh
```

Be aware that the run.sh script uses the built-in Python webserver in the foreground of your shell and is only advisable for testing. Deployments for public traffic should run behind a proper WSGI server like Gunicorn or mod_wsgi.
