from datetime import date, datetime
import uuid
from doppelkopf import db

from doppelkopf.database_constructors import User, Game


def create(playerArray):

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    player1_id = playerArray[0]
    player2_id = playerArray[1]
    player3_id = playerArray[2]
    player4_id = playerArray[3]


    game = Game(timestamp=dt_string, player1_id=player1_id,
                player2_id=player2_id, player3_id=player3_id, player4_id=player4_id)
    db.session.add(game)
    db.session.commit()
    
    
    return game.game_id
