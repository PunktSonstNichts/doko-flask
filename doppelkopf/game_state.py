from doppelkopf.database_constructors import Game, Rounds, RoundsXPlayer, User


def game_state(game_id):
    game = Game.query.filter_by(game_id=game_id).first()
    gamestate = {
        "_id": game_id,
        "runden": [],
        "spieler": [],
        "remainingBock": [],
        "gesperrt": game.locked,
        "withoutBock": game.maxBock == 0,
        "timestamp": game.timestamp}
    # this section is for player related information
    players = [game.player1_id, game.player2_id,
               game.player3_id, game.player4_id]

    # and this section is for options
    maxbock = game.maxBock

    aus = 6
    zs = [0, 0, 0, 0]
    bockIndex = []
    if game.player5_id is not None:
        players.append(game.player5_id)
        zs.append(0)
        aus = len(Rounds.query.filter_by(game_id=game_id).all()) % len(players)

    remBock = [0] * len(players)

    solo_count = 0

    for n, round in enumerate(Rounds.query.filter_by(game_id=game_id).all()):
        bock = remBock[0]
        remBock.pop(0)
        remBock.append(0)

        bock_counter = len(players)
        if round.bock == 1:
            for ind, el in enumerate(remBock):
                if bock_counter == 0:
                    break
                if el < maxbock:
                    bock_counter -= 1
                    remBock[ind] += 1
            for i in range(bock_counter):
                remBock.append(1)

        if round.bock:
            bockIndex.append(n)

        aussetzen = 6
        if len(players) == 5:
            aussetzen = n % len(players)

        roundstate = {
            "punkte": 0,
            "solo": None,
            "spielerArray": [],
            "bock": bock
        }
        zs_set = []
        for i, data in enumerate(RoundsXPlayer.query.filter_by(round_id=round.round_id).all()):

            if i >= aussetzen:
                i += 1

            zs[i] += data.punkte
            zs_set.append(zs[i])
            player_state = {
                "id": data.user_id,
                "partei": data.partei,
                "punkte": data.punkte,
                "zwischenstand": zs[i]
            }

            if data.solotyp == "yes":
                roundstate["solo"] = data.user_id
                # keep track of Solos if they are "eingereit",
                # meaning if the same person has to shuffle cards again
                if game.soloKommtRaus:
                    solo_count = solo_count + 1

            roundstate["punkte"] = abs(data.punkte)
            roundstate["spielerArray"].append(player_state)
        # calculate spieler position each round for better endresult graph
        zs_set = list(set(zs))
        zs_set.sort(reverse=True)
        for index in range(len(roundstate["spielerArray"])):
            roundstate["spielerArray"][index]["position"] = zs_set.index(zs[index]) + 1
        gamestate["runden"].append(roundstate)

    remBock = [i for i in remBock if i != 0]

    gamestate["remainingBock"] = remBock

    zs_set = list(set(zs))
    zs_set.sort(reverse=True)

    raus = (len(Rounds.query.filter_by(game_id=game_id).all()) + 1 - solo_count) % len(players)
    for i, player in enumerate(players):
        print(player)
        pl = User.query.filter_by(user_id=player).first()
        name = pl.username

        if i == raus:
            outi = True
        else:
            outi = False
        if i == aus and aus != 6:
            auss = True
        else:
            auss = False
        spieler = {"aussetzen": auss, "id": player, "kommt_raus": outi, "name": name, "position": 0}

        if len(Rounds.query.filter_by(game_id=game_id).all()) > 0:
            spieler["position"] = zs_set.index(zs[i]) + 1

        gamestate["spieler"].append(spieler)

    return gamestate
