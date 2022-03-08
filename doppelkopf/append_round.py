import couchdb
import create_round
from doppelkopf import db
from doppelkopf.database_constructors import Game, Rounds, RoundsXPlayer


def append(json, gameId):
    for game in Game.query.all():
        if game.game_id == gameId:
            #welches format hat json???

            round= Rounds(game_id="test",timestamp="test")
            playerxround=RoundsXPlayer(round_id, user_id, punkte, partei, hochzeit, schweine, armut, solotyp)


            db.session.add(round)
            db.session.add(playerxround)
            db.session.commit()
            return True
            

    return False


#id runden spieler timestamp
def append(json, gameId):
