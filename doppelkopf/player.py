import random

from doppelkopf import db
from doppelkopf.database_constructors import User


# dev purpose only!
def random_user():
    user = random.choice(User.query.all())
    return {"username": user.username, "user_id": user.user_id, "added_from": user.added_from, "email": user.email}


def check_name(name, namesWithoutAccount=False):
    player_list = []
    for user in User.query.all():
        if user.username.casefold().startswith(name.casefold()):
            if not (namesWithoutAccount and user.password):
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
