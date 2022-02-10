import couchdb

def get_database():
    couch = couchdb.Server('http://admin:1234@localhost:5984/')
    db = couch['doko']
    return db