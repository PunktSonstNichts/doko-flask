import matplotlib.pyplot as plt

from doppelkopf.database_constructors import Game, Rounds, RoundsXPlayer, User


def chart(game_id, request_player_id=20):
    game = Game.query.filter_by(game_id=game_id).first()

    players = [game.player1_id, game.player2_id,
               game.player3_id, game.player4_id]

    if game.player5_id != None:
        players.append(game.player5_id)

    names = []
    for i, player in enumerate(players):
        pl = User.query.filter_by(user_id=player).first()
        names.append(pl.username)

    points = []
    for i in range(len(names)):
        points.append([])
    x = []
    for n, round in enumerate(Rounds.query.filter_by(game_id=game_id).all()):
        for i, playerId in enumerate(players):
            eintrag = RoundsXPlayer.query.filter_by(round_id=round.round_id, user_id=playerId).first()
            if (eintrag):
                points[i].append(eintrag.punkte)
            else:
                points[i].append(0)
        # String for x axis enables only Integers instead of float
        x += [str(1 + n)]

    for n, user_points in enumerate(points):
        for i in range(1, len(user_points)):
            user_points[i] = user_points[i] + user_points[i - 1]

        if players[n] == request_player_id:
            width = 4
        else:
            width = 1
        plt.plot(x, user_points, label=names[n], linewidth=width)

    plt.xlabel('Runden')
    plt.ylabel('Punkte')
    plt.title("Doko Punkteübersicht vom Spiel am " + game.timestamp)

    plt.legend()

    return plt
