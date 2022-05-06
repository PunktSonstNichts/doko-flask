import datetime

from flask import jsonify, request
from flask_api import status
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, decode_token

from doppelkopf import create_game, jwt_login, player, app, append_round, game_state


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    # überprüfen ob Passwort korrekt ist
    if not jwt_login.password_check(username, password):
        return jsonify({"msg": "Bad username or password"}), 401

    # bei erfolgreicehr anmeldung Tokenübermittelung an Client
    access_token = create_access_token(
        identity=username, expires_delta=datetime.timedelta(hours=24))
    print(decode_token(access_token, allow_expired=False))
    return jsonify(access_token=access_token)

@app.route('/new', methods=["POST"])
@jwt_required()
def create_games():
    players = request.json
    create_game.create(players)
    return jsonify(create_game.create(players))


@app.route('/game/<gameId>', methods=["GET", "POST"])
@jwt_required()
def game(gameId):
    if request.method == 'POST':
        content = request.json
        if not append_round.append(content, gameId):
            return "gameID not found", status.HTTP_400_BAD_REQUEST

    return jsonify(game_state.game_state(gameId))


@app.route('/game/<gameId>/lock', methods=["POST"])
@jwt_required()
def lockGame(gameId):
    if not append_round.lock(gameId):
        return "gameID not found", status.HTTP_400_BAD_REQUEST

    return jsonify(game_state.game_state(gameId))


@app.route('/namelist/<name>', methods=["GET"])
@jwt_required()
def name_list(name):
    return ({"player": player.check_name(name)})


@app.route('/new_player', methods=["POST"])
@jwt_required()
def new_player():
    username = request.json.get("username", None)
    added_from = get_jwt_identity()
    return player.add_new_player(added_from, username)


@app.route('/get_token', methods=["GET"])
@jwt_required()
def get_token():
    print(request)
    added_from = get_jwt_identity()
    # todo generate random and somewhat secure token
    # request body contains user_id
    # todo store token in passworld field of corresponding user (see request body)
    # and make sure created field of user is null
    # return token (jwt or something similar?) in payload
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwidG9rZW4iOiIxMjMzMjEiLCJ1c2VybmFtZSI6IlRpbGwiLCJpYXQiOjE1MTYyMzkwMjJ9.lZyhVS01TiWIRY5t18XOuAC0MlKBISJutq40mIsrVxs"


@app.route('/get_token_info/<token>', methods=["GET"])
def get_token_info(token):
    print(request.json)
    print(decode_token(token))
    added_from = get_jwt_identity()
    # todo nothing
    # i really dont know if we need this method as the frontend could just decode the jwt
    # only becomes necessary if we switch to a token which doesn't store "cleartext" information
    return ""


@app.route('/create_user/<token>', methods=["POST"])
def create_user(token):
    print(request.json)
    print(token)
    added_from = get_jwt_identity()
    # todo request body contains user_id, token, e-mail and password
    # todo 1. check if token matches the stored token
    # todo 2. set user created to current timestamp
    # todo 3. encrypt user password and store it and e-mail in db
    # todo maybe directly return jwt token so user is already locked in
    return ""


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
