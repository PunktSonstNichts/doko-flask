from database_connector import get_database

class Game:
    def __init__(self, game_id):
        self.db = get_database()[game_id]
    
    def __str__(self) -> str:
        game_str = ""
        game_str += str(self.db)
        return game_str

    def __repr__(self) -> str:
        game_str = ""
        game_str += repr(self.db)
        return game_str

    def __getitem__(self, arg):
        return self.db[arg]

def get_games():
    games = get_database()
    for g in games:
        print(g)
    return [Game(game_id) for game_id in games]

print(get_games())