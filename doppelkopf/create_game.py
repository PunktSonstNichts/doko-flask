from datetime import datetime

from doppelkopf import db
from doppelkopf.database_constructors import Game


def create(playerArray, maxBock, soloKommtRaus):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    player1_id = playerArray["player1"]["user_id"]
    player2_id = playerArray["player2"]["user_id"]
    player3_id = playerArray["player3"]["user_id"]
    player4_id = playerArray["player4"]["user_id"]
    if (playerArray["player5"]):
        player5_id = playerArray["player5"]["user_id"]
    else:
        player5_id = None

    game = Game(timestamp=dt_string,
                player1_id=player1_id,
                player2_id=player2_id,
                player3_id=player3_id,
                player4_id=player4_id,
                player5_id=player5_id,
                maxBock=maxBock,
                soloKommtRaus=soloKommtRaus)
    db.session.add(game)
    db.session.commit()

    return {"_id": game.game_id}
