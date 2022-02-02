import couchdb
import json

couch = couchdb.Server('http://admin:1234@localhost:5984/')
for dbname in couch:
    print(dbname)

db = couch['doko']
game = {
    "timestamp": 234,
    "spieler": [
        {
            "name": "Till",
            "id": 3
        },
        {
            "name": "Malte",
            "id": 5
        },
        {
            "name": "Alex",
            "id": 4
        },
        {
            "name": "Thibaud",
            "id": 2
        }
    ],
    "runden": [
        {
            "roundeNr": 0,
            "result": [
                {
                    "spieler_id": 5,
                    "partei": "re",
                    "punkte": 2,
                    "hochzeit": 0,
                    "schweine": 0,
                    "armut": 0,
                    "ausgesetzt": 0,
                    "ansagen": {
                        "keine_120": 0,
                        "keine_90": 0,
                        "keine_60": 0,
                        "keine_30": 0,
                        "keine_0": 0
                    }
                },
                {
                    "spieler_id": 3,
                    "partei": "re",
                    "punkte": 2,
                    "hochzeit": 0,
                    "schweine": 0,
                    "armut": 0,
                    "ausgesetzt": 0,
                    "ansagen": {
                        "keine_120": 0,
                        "keine_90": 0,
                        "keine_60": 0,
                        "keine_30": 0,
                        "keine_0": 1
                    }
                }
            ]
        }
    ]
}
db["1"] = game
print(db)
