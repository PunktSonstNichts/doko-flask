from datetime import date, datetime
import uuid
from doppelkopf import db

from doppelkopf.database_constructors import User, Game


def create(playerArray):

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    player1_id = playerArray["player1"]["user_id"]
    player2_id = playerArray["player2"]["user_id"]
    player3_id = playerArray["player3"]["user_id"]
    player4_id = playerArray["player4"]["user_id"]


    game = Game(timestamp=dt_string, player1_id=player1_id,
                player2_id=player2_id, player3_id=player3_id, player4_id=player4_id)
    db.session.add(game)
    db.session.commit()
    
   
    return {"_id":game.game_id}
