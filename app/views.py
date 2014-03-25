from app import app
from flask import abort, jsonify, render_template
from functools import wraps
from player import Player, IllegalAccessException


def wrap_data_access(func):
    @wraps(func)
    def wrapped(*args, **kwds):
        try:
            return func(*args, **kwds)
        except IllegalAccessException as e:
            app.logger.info(e.message)
        except IOError:
            abort(404)
    return wrapped


@app.route('/player/<username>.json', methods=['GET'])
@wrap_data_access
def player_json(username):
    player = Player(username)
    return jsonify(player.data)


@app.route('/player/<username>', methods=['GET'])
@wrap_data_access
def player_html(username):
    player = Player(username)
    return render_template('player.html', player_name=player.username, data=player.data)
