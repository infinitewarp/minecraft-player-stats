from functools import wraps

from flask import abort, render_template

from mcstats import app, config
from mcstats.util import pretty_time, pretty_count
from mcstats.world import World


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

    activity_overview = [
        (pretty_time(world.total_minutes_played, units_count=2), 'Time Played', 'fa fa-clock-o'),
        (pretty_count(world.total_mob_kills), 'Mobs Killed', 'fa fa-shield'),
        (pretty_count(world.total_player_deaths), 'Player Deaths', 'fa fa-frown-o'),
        (pretty_count(world.total_blocks_broken), 'Blocks Mined', 'fa fa-chain-broken')
    ]

    # get the top 10 players for each category
    most_online = world.players_most_online(10)
    most_broken = world.players_most_broken_blocks(10)
    most_crafted = world.players_most_crafted_items(10)
    greatest_distance = world.players_greatest_distance(10)
    most_kills = world.players_most_kills(10)
    most_deaths = world.players_most_deaths(10)
    usernames = world.usernames()

    return render_template(
        'world.html', config=config, usernames=usernames,
        activity_overview=activity_overview,
        most_online=most_online,
        most_broken=most_broken,
        most_crafted=most_crafted,
        greatest_distance=greatest_distance,
        most_kills=most_kills,
        most_deaths=most_deaths,
    )


@app.route('/player/<username>', methods=['GET'])
@wrap_data_access
def player_html(username):
    world = World()

    if username not in world.players:
        abort(404)

    usernames = world.usernames()
    player = world.players[username]

    return render_template(
        'player.html', config=config, usernames=usernames,
        player=player,
    )
