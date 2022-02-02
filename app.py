import flask
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_api import status

import append_round
import create_round
import game_state

PO = []
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
CORS(app)


@app.route('/new', methods=["POST"])
def create_game():
    players = request.json
    return jsonify(create_round.create(players))


@app.route('/game/<gameId>', methods=["GET", "POST"])
def game(gameId):
    if flask.request.method == 'POST':
        content = request.json
        if not append_round.append(content, gameId):
            return "gameID not found", status.HTTP_400_BAD_REQUEST

    return jsonify(game_state.game_state(gameId))


if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True)
