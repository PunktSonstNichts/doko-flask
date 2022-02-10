from game import Game

def game_state(game_id):
    game = Game(game_id)
    
    # this section is for player related information
    players = game["spieler"]

    # whos turn it is (kommt_raus)
    spieler_rauskommen = players[ len(game["runden"]) % len(players) ]
    for player in players:
        player["kommt_raus"] = (player["id"] == spieler_rauskommen["id"])

    # who is ignored this round (aussetzen) [only needed for > 4 players]
    spieler_aussetzen = players[ (len(game["runden"]) - 1) % len(players) ]
    for player in players:
        player["aussetzen"] = ( len(players) != 4 ) and ( player["id"] == spieler_aussetzen["id"] )

    # this section is for "zwischenergebnisse"
    # each round, every played round needs to be summed up to per player
    stats = { player["id"]: {   "points":0,
                                "solo":0,
                                "armut":0,
                                "schweine":0
            } for player in players }
    
    for round in game["runden"]:
        for player in round["spielerArray"]:
            stats[player["id"]]["points"] += player["punkte"]
            player["zwischenstand"] = stats[player["id"]]["points"]
    
    print("Game: ", game)
    return game
