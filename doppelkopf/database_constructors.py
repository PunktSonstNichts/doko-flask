import json

from sqlalchemy import ForeignKey

from doppelkopf import db


class User(db.Model):
    user_id = db.Column("user_id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(100), nullable=False)
    password = db.Column("password", db.String(100), nullable=True)
    email = db.Column("email", db.String(100), nullable=True)
    added_from = db.Column("added_from", db.Integer, ForeignKey("user.user_id"), nullable=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Game(db.Model):
    game_id = db.Column("game_id", db.Integer, primary_key=True)
    timestamp = db.Column("timestamp", db.String(100), nullable=False)
    player1_id = db.Column(
        "player1_id", db.Integer, ForeignKey("user.user_id"), nullable=False
    )
    player2_id = db.Column(
        "player2_id", db.Integer, ForeignKey("user.user_id"), nullable=False
    )
    player3_id = db.Column(
        "player3_id", db.Integer, ForeignKey("user.user_id"), nullable=False
    )
    player4_id = db.Column(
        "player4_id", db.Integer, ForeignKey("user.user_id"), nullable=False
    )
    player5_id = db.Column(
        "player5_id", db.Integer, ForeignKey("user.user_id"), nullable=True
    )
    locked = db.Column(
        "locked", db.String(100), nullable=True
    )


class Rounds(db.Model):
    game_id = db.Column("game_id", db.Integer, ForeignKey("game.game_id"))
    round_id = db.Column("round_id", db.Integer, primary_key=True)
    timestamp = db.Column("timestamp", db.String(100), nullable=False)
    bock = db.Column("bock", db.BOOLEAN, nullable=False, default=False)


class RoundsXPlayer(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    round_id = db.Column("round_id", db.Integer, ForeignKey("rounds.round_id"))
    user_id = db.Column("user_id", db.Integer, ForeignKey("user.user_id"))
    punkte = db.Column("punkte", db.Integer)
    partei = db.Column("partei", db.String)
    hochzeit = db.Column("hochzeit", db.String, nullable=True)
    schweine = db.Column("schweine", db.String, nullable=True)
    armut = db.Column("armut", db.Integer, nullable=True)
    solotyp = db.Column("solotyp", db.String, nullable=True)


# only creates db if not existing
db.create_all()
