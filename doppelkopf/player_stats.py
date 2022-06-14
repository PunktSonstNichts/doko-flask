from flask import jsonify
from sqlalchemy import or_

from doppelkopf.database_constructors import Game
from doppelkopf.game_state import game_state


def games_for_player(user_id):
    games_list = []
    for game in Game.query.filter(or_(Game.player1_id == user_id,
                                      Game.player2_id == user_id,
                                      Game.player3_id == user_id,
                                      Game.player4_id == user_id,
                                      Game.player5_id == user_id)).all():
        games_list.append(game_state(game.game_id))

    return jsonify(games_list)
