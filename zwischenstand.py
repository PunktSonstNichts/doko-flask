from doppelkopf.database_constructors import Game, Rounds, RoundsXPlayer, User
from doppelkopf import db
import json
import matplotlib.pyplot as plt


def chart(game_id):
    game = Game.query.filter_by(game_id=game_id).first()

    players = [game.player1_id, game.player2_id,
               game.player3_id, game.player4_id]

    if game.player5_id != None:
        players.append(game.player5_id)
    names = []
    for i, player in enumerate(players):
        pl = User.query.filter_by(user_id=player).first()
        names.append(pl.username)
    print(names)
    points = []
    for i in range(len(names)):
        points.append([])
    x = []
    for n, round in enumerate(Rounds.query.filter_by(game_id=game_id).all()):
        for i, data in enumerate(RoundsXPlayer.query.filter_by(round_id=round.round_id).all()):
            points[i].append(data.punkte)
        x.append(n+1)

    for n, user_points in enumerate(points):
        for i in range(1, len(user_points)):
            user_points[i] = user_points[i]+user_points[i-1]

        plt.plot(x, user_points, label=names[n])

    print(points)
    plt.xlabel('Runden')
    plt.ylabel('Punkte')

    plt.title("Simple Plot")

    plt.legend()

    plt.show()
