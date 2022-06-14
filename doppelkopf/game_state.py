from doppelkopf.database_constructors import Game, Rounds, RoundsXPlayer, User
import collections


def game_state(game_id):
    MAXBOCK = 2

    game = Game.query.filter_by(game_id=game_id).first()
    gamestate = {
        "_id": game_id,
        "runden": [],
        "spieler": [],
        "remainingBock": [],
        "gesperrt": game.locked,
        "timestamp": game.timestamp}

    # this section is for player related information
    players = [game.player1_id, game.player2_id,
               game.player3_id, game.player4_id]
    
    aus = 6
    zs = [0, 0, 0, 0]
    bockIndex = []
    if game.player5_id != None:
        players.append(game.player5_id)
        aus = len(Rounds.query.filter_by(game_id=game_id).all()) % len(players)
        zs.append(0)
        
        # bock.append(0) #here was the 500 error msg
    remBock = [0] * len(players)
    raus = (len(Rounds.query.filter_by(game_id=game_id).all()) + 1) % len(players)

    
    
    for n, round in enumerate(Rounds.query.filter_by(game_id=game_id).all()):
        bock = remBock[0]
        remBock.pop(0)
        remBock.append(0)
        
        bock_counter = len(players)
        if round.bock == 1:
            for ind, el in enumerate(remBock):
                if bock_counter == 0:
                    break
                if el < MAXBOCK:
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
        zs_set=[]
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
            roundstate["punkte"] = abs(data.punkte)
            roundstate["spielerArray"].append(player_state)
        gamestate["runden"].append(roundstate)

    remBock = [i for i in remBock if i != 0]
    
    gamestate["remainingBock"] = remBock
    
    
        

    zs_set= list(set(zs))
    zs_set.sort(reverse=True)
    
    
    for i, player in enumerate(players):
        
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
        spieler = {
            "aussetzen": auss,
            "id": player,
            "kommt_raus": outi,
            "name": name
        }
        spieler["position"]=0

        
        if len(Rounds.query.filter_by(game_id=game_id).all())>0:
            spieler["position"]=zs_set.index(zs[i])+1

        gamestate["spieler"].append(spieler)

    


    return gamestate
