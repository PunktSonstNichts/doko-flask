from datetime import datetime

from doppelkopf import db
from doppelkopf.database_constructors import Game, Rounds, RoundsXPlayer


def append(json, gameId):
    for game in Game.query.all():

        if game.game_id == int(gameId):
            if (game.locked):
                # only un-locked games can be manipulated
                return False
            # welches format hat json???
            now = datetime.now()

            timestamp = now.strftime("%d/%m/%Y %H:%M:%S")

            round = Rounds(game_id=gameId, timestamp=timestamp)
            db.session.add(round)
            db.session.commit()
            for user in json["spielerArray"]:

                if user["id"] == json["solo"]:
                    solo = "yes"
                else:
                    solo = "no"

                playerxround = RoundsXPlayer(
                    round_id=round.round_id, user_id=user["id"], punkte=user["punkte"], partei=user["partei"],
                    solotyp=solo, schweine=json["schweine"], hochzeit=json["hochzeit"], armut=json["armut"])

                db.session.add(playerxround)
                db.session.commit()
            return True

    return False


def lock(gameId):
    for game in Game.query.all():
        if game.game_id == int(gameId):
            now = datetime.now()
            game.locked = now.strftime("%d/%m/%Y %H:%M:%S")
            db.session.commit()
            return True
    return False
