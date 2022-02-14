import flask
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_api import status
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required, get_jwt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import decode_token
import jwt_login
import datetime
import append_round
import create_round
import game_state


PO = []
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
CORS(app)
app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)


@app.route("/login", methods=["POST"])
def login():
    # username = request.form.get("username")
    # password = request.form.get("password")
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    # überprüfen ob Passwort korrekt ist
    if not jwt_login.password_check(username, password):
        return jsonify({"msg": "Bad username or password"}), 401

    # bei erfolgreicehr anmeldung Tokenübermittelung an Client
    access_token = create_access_token(identity=username, expires_delta=datetime.timedelta(hours=24))
    print(decode_token(access_token, allow_expired=False))
    return jsonify(access_token=access_token)

@app.route('/new', methods=["POST"])
@jwt_required()
def create_game():
    players = request.json
    return jsonify(create_round.create(players))


@app.route('/game/<gameId>', methods=["GET", "POST"])
@jwt_required()
def game(gameId):
    if flask.request.method == 'POST':
        content = request.json
        if not append_round.append(content, gameId):
            return "gameID not found", status.HTTP_400_BAD_REQUEST

    return jsonify(game_state.game_state(gameId))

@app.route('/namelist/<name>', methods=["GET"])
@jwt_required()
def name_list(name):
    return player.check_name(name)


@app.route('/new_player', methods=["POST"])
@jwt_required()
def new_player():
    username = request.json.get("username", None)
    added_from = get_jwt_identity()
    return player.add_new_player(added_from, username)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
