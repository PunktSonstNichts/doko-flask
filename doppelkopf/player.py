import datetime
import uuid
from doppelkopf.database_constructors import User
from doppelkopf import db


def check_name(name):

    player_list = []
    for user in User.query.all():
        if user.username.startswith(name):
            player_list.append(
                {"username": user.username, "user_id": user.user_id})

    return player_list


def add_new_player(added_from, new_user):
    

    if user_already_exist(new_user):
        return "user already exists"
    test = User(username=new_user, added_from=added_from)
         

    db.session.add(test)
    db.session.commit()

    return {"username": test.username, "user_id": test.user_id, "added_from": added_from}


def user_already_exist(username):
    for user in User.query.all():
        if user.username == username:
            return True
    return False
