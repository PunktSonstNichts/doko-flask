import couchdb


def game_state(gameid):
    couch = couchdb.Server('http://admin:1234@localhost:5984/')
    db = couch['doko']
    game = db[gameid]

    # this section is for player related information
    spieler_count = len(game["spieler"])
    # whos turn it is (kommt_raus)
    player_rauskommen_index = len(game["runden"]) % spieler_count
    rauskommen_map = [False] * spieler_count
    rauskommen_map[player_rauskommen_index] = True
    # who is ignored this round (aussetzen) [only needed for > 4 players]
    aussetzen_map = [False] * spieler_count
    if spieler_count == 5:
        # player before rauskommen setzt aus
        aussetzen_map[(player_rauskommen_index + 4) % 5] = True
    # putting everything together
    for index in range(spieler_count):
        game["spieler"][index]["kommt_raus"] = rauskommen_map[index]
        game["spieler"][index]["aussetzen"] = aussetzen_map[index]

    # this section is for "zwischenergebnisse"
    # each round, every played round needs to be summed up to per player

    zwischenstand_map = [0] * spieler_count
    for round_index in range(len(game["runden"])):
        for spieler_index in range(spieler_count):
            spieler = game["runden"][round_index]["spielerArray"][spieler_index]
            zwischenstand_map[spieler_index] += spieler["punkte"]
            spieler["zwischenstand"] = zwischenstand_map[spieler_index]

    print(game)
    return game
