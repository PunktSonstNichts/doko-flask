from argparse import ArgumentError, ArgumentTypeError
from doppelkopf import db
from doppelkopf.database_constructors import Game, Rounds, RoundsXPlayer
from datetime import datetime


def append(json, gameId):
    for game in Game.query.all():

        if game.game_id == int(gameId):
            # welches format hat json???
            now = datetime.now()

            timestamp = now.strftime("%d/%m/%Y %H:%M:%S")

            round = Rounds(game_id=gameId, timestamp=timestamp)
            db.session.add(round)
            db.session.commit()
            for user in json["spielerArray"]:
                # schweine
                # hcohezeit
                # Armut
                try:
                    schweine = user["schweine"]
                except:
                    schweine = False
                try:
                    hochzeit = user["hochzeit"]
                except:
                    hochzeit = False
                try:
                    armut = user["armut"]
                except:
                    armut = False

                if user["id"] == json["solo"]:
                    solo = "yes"
                else:
                    solo = "no"

                playerxround = RoundsXPlayer(
                    round_id=round.round_id, user_id=user["id"], punkte=user["punkte"], partei=user["partei"], solotyp=solo, schweine=schweine, hochzeit=hochzeit, armut=armut)

                db.session.add(playerxround)
                db.session.commit()
            return True

    return False
