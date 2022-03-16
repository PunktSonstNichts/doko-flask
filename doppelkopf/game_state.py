from doppelkopf.database_constructors import Game, Rounds, RoundsXPlayer, User
import json


def game_state(game_id):
    game = Game.query.filter_by(game_id=game_id).first()

    gamestate = {
        "_id": game_id,
        "runden": [],
        "spieler": [],
        "timestamp": game.timestamp}

    # this section is for player related information
    players = [game.player1_id, game.player2_id,
               game.player3_id, game.player4_id]
    aus = False
    if game.player5_id != None:
        players.append(game.player5_id)
        aus = len((Rounds.query.filter_by(
            game_id=game_id).all())-1) % len(players)

    raus = len(Rounds.query.filter_by(game_id=game_id).all()) % len(players)

    for i, player in enumerate(players):
        pl = User.query.filter_by(user_id=player).first()
        name = pl.username

        if i == raus:
            outi = True
        else:
            outi = False
        spielerer = {
            "aussetzen": aus,
            "id": player,
            "kommt_raus": outi,
            "name": name
        }

        gamestate["spieler"].append(spielerer)
    zs = [0, 0, 0, 0]
    for round in Rounds.query.filter_by(game_id=game_id).all():

        roundstate = {
            "punkte": 0,
            "solo": None,
            "spielerArray": []
        }

        for i, data in enumerate(RoundsXPlayer.query.filter_by(round_id=round.round_id).all()):
            zs[i] += data.punkte
            player_state = {
                "id": data.user_id,
                "partei": data.partei,
                "punkte": data.punkte,
                "zwischenstand": zs[i]
            }
            if data.solotyp == "yes":
                roundstate["solo"] = data.user_id
            roundstate["punkte"] = abs(data.punkte)
            roundstate["spielerArray"].append(player_state)
        gamestate["runden"].append(roundstate)

    return gamestate
