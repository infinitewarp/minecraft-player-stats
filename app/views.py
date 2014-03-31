from app import app, config
from flask import abort, jsonify, render_template
from functools import wraps
from player import Player
from profile import Profile, ProfileNotFound
from world import World


def wrap_data_access(func):
    @wraps(func)
    def wrapped(*args, **kwds):
        try:
            return func(*args, **kwds)
        except IOError:
            abort(404)
    return wrapped


@app.route('/', methods=['GET'])
@wrap_data_access
def world_html():
    world = World()

    # get the top 10 players for each category
    most_online = world.players_most_online(10)
    most_broken = world.players_most_broken_blocks(10)
    most_crafted = world.players_most_crafted_items(10)
    greatest_distance = world.players_greatest_distance(10)
    most_kills = world.players_most_kills(10)
    most_deaths = world.players_most_deaths(10)
    usernames = world.usernames()

    return render_template('world.html', config=config, usernames=usernames,
                           most_online=most_online,
                           most_broken=most_broken,
                           most_crafted=most_crafted,
                           greatest_distance=greatest_distance,
                           most_kills=most_kills,
                           most_deaths=most_deaths,
                           )


@app.route('/player/<username>.json', methods=['GET'])
@wrap_data_access
def player_json(username):
    player = Player(username)
    return jsonify(player.data)


@app.route('/player/<username>', methods=['GET'])
@wrap_data_access
def player_html(username):
    world = World()

    if username not in world.players:
        abort(404)

    usernames = world.usernames()
    player = world.players[username]

    return render_template('player.html', config=config, usernames=usernames,
                           player=player,
                           )


@app.route('/player/<username>/profile.json', methods=['GET'])
@wrap_data_access
def player_profile_json(username):
    try:
        profile = Profile(username=username)
    except ProfileNotFound:
        abort(404)
    return jsonify(profile.data)


@app.route('/profile/<uuid>.json', methods=['GET'])
@wrap_data_access
def profile_json_from_uuid(uuid):
    try:
        profile = Profile(uuid=uuid)
    except ProfileNotFound:
        abort(404)
    return jsonify(profile.data)
