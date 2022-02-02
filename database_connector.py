import couchdb

couch = couchdb.Server('http://admin:1234@localhost:5984/')
db = couch['doko']