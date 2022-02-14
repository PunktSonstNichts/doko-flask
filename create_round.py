from datetime import date, datetime
import uuid
#import database_connector as db
import couchdb


def create(playerArray):
    couch = couchdb.Server('http://admin:1234@localhost:5984/')
    db = couch['doko']

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    data = {'_id': uuid.uuid4().__str__(), 'timestamp': dt_string, 'spieler': []}
    for player in playerArray:
        if playerArray[player] is not None:
            data['spieler'].append({
                'name': playerArray[player],
                'id': uuid.uuid4().__str__()
            })

    data['runden'] = []
    db.save(data)
    return data
