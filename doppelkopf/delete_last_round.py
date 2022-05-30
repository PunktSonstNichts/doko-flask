from doppelkopf import db
from doppelkopf.database_constructors import Rounds, RoundsXPlayer


def delete(game_id):
    rounds = Rounds.query.filter_by(game_id=game_id).all()
    id = rounds[-1].round_id

    for rxp in RoundsXPlayer.query.filter_by(round_id=id):
        db.session.delete(rxp)
        db.session.commit()

    db.session.delete(rounds[-1])
    db.session.commit()
