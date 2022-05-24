import uuid
from datetime import timedelta

import bcrypt
from flask import jsonify
from flask_jwt_extended import create_access_token, decode_token
from sqlalchemy import func

from doppelkopf import db
from doppelkopf.database_constructors import User


def upgrade_player_to_user(user_id, token, password, email):
    user = User.query.filter_by(user_id=user_id).first()
    if not user or not user.password == "token:" + token or not password:
        return "Bad request", 400
    password = password.encode('UTF-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    hashed = hashed.decode("utf-8")

    user.password = hashed
    user.last_login = func.now()
    if email:
        user.email = email
    db.session.commit()
    access_token = create_access_token(
        identity=user.username, expires_delta=timedelta(hours=24))
    return jsonify(access_token=access_token)


def create_token_for_player(user_id, added_from):
    token = uuid.uuid4().__str__()

    player = User.query.filter_by(user_id=user_id).first()
    player.added_from = added_from
    player.password = "token:" + token
    db.session.commit()
    return token


def find_player_from_token(token):
    user = User.query.filter_by(password="token:" + token, last_login=None).first()
    if not user:
        return "Bad token", 400
    return {"username": user.username, "user_id": user.user_id, "added_from": user.added_from}


def user_already_exist(username):
    for user in User.query.all():
        print(user.username)
        if user.username == username:
            return True
    return False


def password_check(name, password):
    player = User.query.filter_by(username=name).first()
    if player:
        if bcrypt.checkpw(password.encode('UTF-8'), player.password.encode('UTF-8')):
            return player
    return False


def login_user(username, password):
    # überprüfen ob Passwort korrekt ist
    user = password_check(username, password)
    print(user)
    if not user:
        return jsonify({"msg": "Bad username or password"}), 401

    # bei erfolgreicehr anmeldung Tokenübermittelung an Client
    access_token = create_access_token(
        identity=username, expires_delta=timedelta(hours=24))
    print(decode_token(access_token, allow_expired=False))

    # speichere den letzten login
    user.last_login = func.now()
    db.session.commit()
    return jsonify(access_token=access_token)
