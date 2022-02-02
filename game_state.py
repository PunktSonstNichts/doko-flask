import couchdb


def game_state(gameid):
    couch = couchdb.Server('http://admin:1234@localhost:5984/')
    db = couch['doko']
    game = db[gameid]

    # this section is for player related information
    players = game["spieler"]

    # whos turn it is (kommt_raus)
    spieler_rauskommen = players[ len(game["runden"]) % len(players) ]
    for player in players:
        player["kommt_raus"] = (player["id"] == spieler_rauskommen["id"])

    spieler_aussetzen = players[ (len(game["runden"]) - 1) % len(players) ]
    # who is ignored this round (aussetzen) [only needed for > 4 players]
    for player in players:
        player["aussetzen"] = ( len(players) != 4 ) and ( player["id"] == spieler_aussetzen["id"] )


    # this section is for "zwischenergebnisse"
    # each round, every played round needs to be summed up to per player
    points = {player["id"]:0 for player in players}

    for round in game["runden"]:
        print("Round: ", round)
        for player in players:
            for player_ in round["spielerArray"]:
                if player["id"] == player_["id"]:
                    print("Player: ", player, player_)
                    points[player["id"]] += player_["punkte"]
                    player_["zwischenstand"] = points[player["id"]]  
    
    print("Game: ", game)
    return game
