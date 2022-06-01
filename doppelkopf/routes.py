import os

from flask import jsonify, request, send_file, send_from_directory
from flask_api import status
from flask_jwt_extended import get_jwt_identity, jwt_required

from doppelkopf import create_game, endergebniss, jwt_login, player, app, append_round, game_state, delete_last_round, \
    player_stats
from doppelkopf.jwt_login import create_token_for_player, find_player_from_token, upgrade_player_to_user


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    return jwt_login.login_user(username, password)

@app.route('/new', methods=["POST"])
@jwt_required()
def create_games():
    players = request.json
    create_game.create(players)
    return jsonify(create_game.create(players))


@app.route('/game/<gameId>', methods=["GET", "POST", "DELETE"])
@jwt_required()
def game(gameId):
    if request.method == 'POST':
        content = request.json
        if not append_round.append(content, gameId):
            return "gameID not found", status.HTTP_400_BAD_REQUEST
    elif request.method == 'DELETE':
        delete_last_round.delete(gameId)

    return jsonify(game_state.game_state(gameId))


@app.route('/game/<gameId>/lock', methods=["POST"])
@jwt_required()
def lockGame(gameId):
    if not append_round.lock(gameId):
        return "gameID not found", status.HTTP_400_BAD_REQUEST
    endergebniss.chart(gameId)
    return jsonify(game_state.game_state(gameId))


@app.route('/namelist/<name>', methods=["GET"])
@jwt_required()
def name_list(name):
    userHasAccount = request.args.get("userHasAccount", type=lambda v: v.lower() == 'true', default=False)
    return {"player": player.check_name(name, userHasAccount)}


@app.route('/new_player', methods=["POST"])
@jwt_required()
def new_player():
    username = request.json.get("username", None)
    added_from = get_jwt_identity()
    return player.add_new_player(added_from, username)


@app.route('/get_token', methods=["GET"])
@jwt_required()
def get_token():
    if request.args.get("user_id") is None:
        return "user_id is missing", status.HTTP_400_BAD_REQUEST
    print(request.args.get("user_id"))
    added_from = get_jwt_identity()
    token = create_token_for_player(request.args.get("user_id"), added_from)
    # todo generate random and somewhat secure token
    # request body contains user_id
    # todo store token in passworld field of corresponding user (see request body)
    # and make sure created field of user is null
    # return token (jwt or something similar?) in payload: make sure it's URL-valid!
    return token


@app.route('/get_token_info/<token>', methods=["GET"])
def get_token_info(token):
    return find_player_from_token(token)


@app.route('/create_user/<token>', methods=["POST"])
def create_user(token):
    print(token)
    # added_from = get_jwt_identity()
    # todo request body contains user_id, token, e-mail and password
    # todo 1. check if token matches the stored token
    # todo 2. set user created to current timestamp
    # todo 3. encrypt user password and store it and e-mail in db
    # todo maybe directly return jwt token so user is already locked in
    return upgrade_player_to_user(request.json["user_id"],
                                  token,
                                  request.json["password"],
                                  request.json.get("email", None))


@app.route('/result_plot/<path>')
def send_report(path):
    root_dir = os.path.dirname(os.getcwd())
    print(root_dir)
    print(send_from_directory(os.path.join(root_dir, 'doko-flask', 'Graphs'), path))
    return send_from_directory(os.path.join(root_dir, 'Graphs'), path)


@app.route('/get_player_stats', methods=["GET"])
@jwt_required()
def get_player_stats():
    print(get_jwt_identity())
    return player_stats(1)


@app.route('/download')
# @jwt_required()
def downloadFile():
    # For windows you need to use drive name [ex: F:/Example.pdf]
    path = "doko.db"
    return send_file(path, as_attachment=True)


@app.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/")
@jwt_required()
def jwt_works():
    return "<p>Hello, World!</p>"
