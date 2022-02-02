import couchdb
import create_round


def append(json, gameId):
    couch = couchdb.Server('http://admin:1234@localhost:5984/')
    db = couch['doko']

    if gameId not in db:
        return False

    # todo this is dirty af as with 5 players, the first player might have 0 points
    # punkte = abs(json[0]["punkte"])
    cur = db[gameId]
    cur['runden'].append(json)
    db[gameId] = cur
    return True
