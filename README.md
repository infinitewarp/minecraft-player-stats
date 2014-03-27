minecraft-player-stats
======================

A web application for displaying player stats from a Minecraft server. An app with a sterile name but hopefully a sterling presentation.

Minecraft servers automatically generate statistics about player activities and periodically save those stats to disk (roughly every five minutes). These stats for each user include her achievements, the number and types of blocks broken, distance traveled by various methods, etc. However, Minecraft itself doesn't come with a visualizer for this captured data. The minecraft-player-stats app reads that data and serves it to visitors in a friendly, consumable format.

Because minecraft-player-stats reads player stats from disk instead of interfacing directly with the running Minecraft server, the minecraft-player-stats app can be run separately from the Minecraft server itself. This sets up some interesting possibilities from a server management perspective. If you run a private Minecraft server (perhaps on a LAN), you could publicly expose your stats on the web through this app. If you're security-conscious, you could set up a job to sync player stats from your game server to your web server so Minecraft's binaries and data are never potentially exposed by the web server. If your Minecraft server is under heavy load (as many tend to be), running the stats on a separate server potentially relieves strain from the game.
