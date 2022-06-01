from sqlalchemy import or_

from doppelkopf.database_constructors import Game


def player_stats(user_id):
    for game in Game.filter_by(or_(Game.player1_id == user_id,
                                   Game.player2_id == user_id,
                                   Game.player3_id == user_id,
                                   Game.player4_id == user_id,
                                   Game.player5_id == user_id)).all():
        print(game)
